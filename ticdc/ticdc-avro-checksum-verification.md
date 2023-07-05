---
title: TiCDC Row Data Checksum Verification Based on Avro
summary: Introduce the detailed implementation of TiCDC row data checksum verification.
---

# TiCDC Row Data Checksum Verification Based on Avro

This document introduces how to consume data sent to Kafka by TiCDC and encoded by Avro protocol using Golang, and how to perform data verification using the [Single-row data checksum feature](/ticdc/ticdc-integrity-check.md).

The source code of this example is available in the [`avro-checksum-verification`](https://github.com/pingcap/tiflow/tree/master/examples/golang/avro-checksum-verification) directory.

The example in this document uses [kafka-go](https://github.com/segmentio/kafka-go) to create a simple Kafka consumer program. This program continuously reads data from a specified topic, calculates the checksum, and verifies its value.

```go
package main

import (
    "context"
    "encoding/binary"
    "encoding/json"
    "hash/crc32"
    "io"
    "math"
    "net/http"
    "strconv"
    "strings"

    "github.com/linkedin/goavro/v2"
    "github.com/pingcap/log"
    "github.com/pingcap/tidb/parser/mysql"
    "github.com/pingcap/tidb/types"
    "github.com/pingcap/tiflow/pkg/errors"
    "github.com/segmentio/kafka-go"
    "go.uber.org/zap"
)

const (
    // The first byte of the Confluent Avro wire format is always 0.
    // For more details, see https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html#wire-format.
    magicByte = uint8(0)
)

func main() {
    var (
        kafkaAddr         = "127.0.0.1:9092"
        schemaRegistryURL = "http://127.0.0.1:8081"

        topic           = "avro-checksum-test"
        consumerGroupID = "avro-checksum-test"
    )

    consumer := kafka.NewReader(kafka.ReaderConfig{
        Brokers:  []string{kafkaAddr},
        GroupID:  consumerGroupID,
        Topic:    topic,
        MaxBytes: 10e6, // 10MB
    })
    defer consumer.Close()

    ctx := context.Background()
    log.Info("start consuming ...", zap.String("kafka", kafkaAddr), zap.String("topic", topic), zap.String("groupID", consumerGroupID))
    for {
        // 1. Fetch the kafka message.
        message, err := consumer.FetchMessage(ctx)
        if err != nil {
            log.Error("read kafka message failed", zap.Error(err))
        }

        value := message.Value
        if len(value) == 0 {
            log.Info("delete event does not have value, skip checksum verification", zap.String("topic", topic))
        }

        // 2. Decode the value to get the corresponding value map and schema map.
        valueMap, valueSchema, err := getValueMapAndSchema(value, schemaRegistryURL)
        if err != nil {
            log.Panic("decode kafka value failed", zap.String("topic", topic), zap.ByteString("value", value), zap.Error(err))
        }

        // 3. Calculate and verify checksum value using the value map and schema map obtained in the previous step.
        err = CalculateAndVerifyChecksum(valueMap, valueSchema)
        if err != nil {
            log.Panic("calculate checksum failed", zap.String("topic", topic), zap.ByteString("value", value), zap.Error(err))
        }

        // 4. Commit offset after the data is successfully consumed.
        if err := consumer.CommitMessages(ctx, message); err != nil {
            log.Error("commit kafka message failed", zap.Error(err))
            break
        }
    }
}
```

The key steps for calculating the checksum value are `getValueMapAndSchema()` and `CalculateAndVerifyChecksum()`. The following sections describe the implementation of these two functions.

## Decode data and get the corresponding schema

The `getValueMapAndSchema()` method decodes data and gets the corresponding schema. This method returns both the data and schema as a `map[string]interface{}` type.

```go
// data is the key or value of the received kafka message, and url is the schema registry url.
// This function returns the decoded value and corresponding schema as map.
func getValueMapAndSchema(data []byte, url string) (map[string]interface{}, map[string]interface{}, error) {
    schemaID, binary, err := extractSchemaIDAndBinaryData(data)
    if err != nil {
        return nil, nil, err
    }

    codec, err := GetSchema(url, schemaID)
    if err != nil {
        return nil, nil, err
    }

    native, _, err := codec.NativeFromBinary(binary)
    if err != nil {
        return nil, nil, err
    }

    result, ok := native.(map[string]interface{})
    if !ok {
        return nil, nil, errors.New("raw avro message is not a map")
    }

    schema := make(map[string]interface{})
    if err := json.Unmarshal([]byte(codec.Schema()), &schema); err != nil {
        return nil, nil, errors.Trace(err)
    }

    return result, schema, nil
}

// extractSchemaIDAndBinaryData 
func extractSchemaIDAndBinaryData(data []byte) (int, []byte, error) {
    if len(data) < 5 {
        return 0, nil, errors.ErrAvroInvalidMessage.FastGenByArgs()
    }
    if data[0] != magicByte {
        return 0, nil, errors.ErrAvroInvalidMessage.FastGenByArgs()
    }
    return int(binary.BigEndian.Uint32(data[1:5])), data[5:], nil
}

// GetSchema fetches the schema from the schema registry by the schema ID.
// This function returns a goavro.Codec that can be used to encode and decode the data.
func GetSchema(url string, schemaID int) (*goavro.Codec, error) {
    requestURI := url + "/schemas/ids/" + strconv.Itoa(schemaID)

    req, err := http.NewRequest("GET", requestURI, nil)
    if err != nil {
        log.Error("Cannot create the request to look up the schema", zap.Error(err))
        return nil, errors.WrapError(errors.ErrAvroSchemaAPIError, err)
    }
    req.Header.Add(
        "Accept",
        "application/vnd.schemaregistry.v1+json, application/vnd.schemaregistry+json, "+
            "application/json",
    )

    httpClient := &http.Client{}
    resp, err := httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Error("Cannot parse the lookup schema response", zap.Error(err))
        return nil, errors.WrapError(errors.ErrAvroSchemaAPIError, err)
    }

    if resp.StatusCode == 404 {
        log.Warn("Specified schema not found in Registry", zap.String("requestURI", requestURI), zap.Int("schemaID", schemaID))
        return nil, errors.ErrAvroSchemaAPIError.GenWithStackByArgs("Schema not found in Registry")
    }

    if resp.StatusCode != 200 {
        log.Error("Failed to query schema from the Registry, HTTP error",
            zap.Int("status", resp.StatusCode), zap.String("uri", requestURI), zap.ByteString("responseBody", body))
        return nil, errors.ErrAvroSchemaAPIError.GenWithStack("Failed to query schema from the Registry, HTTP error")
    }

    var jsonResp lookupResponse
    err = json.Unmarshal(body, &jsonResp)
    if err != nil {
        log.Error("Failed to parse result from Registry", zap.Error(err))
        return nil, errors.WrapError(errors.ErrAvroSchemaAPIError, err)
    }

    codec, err := goavro.NewCodec(jsonResp.Schema)
    if err != nil {
        return nil, errors.WrapError(errors.ErrAvroSchemaAPIError, err)
    }
    return codec, nil
}

type lookupResponse struct {
    Name     string `json:"name"`
    SchemaID int    `json:"id"`
    Schema   string `json:"schema"`
}

```

## Calculate and verify the checksum value

The `valueMap` and `valueSchema` obtained in the previous step contain all the elements used for checksum calculation and verification.

The checksum calculation and verification process on the consumer side includes the following steps:

1. Get the expected checksum value.
2. Iterate over each column, generate a byte slice according to the column value and the corresponding MySQL type, and update the checksum value continuously.
3. Compare the checksum value calculated in the previous step with the checksum value obtained from the received message. If they are not the same, the checksum verification fails and the data might be corrupted.

The sample code is as follows:

```go
func CalculateAndVerifyChecksum(valueMap, valueSchema map[string]interface{}) error {
    // The fields variable stores the column type information for each data change event. The column IDs are used to sort the fields, which is the same as the order in which the checksum is calculated.
    fields, ok := valueSchema["fields"].([]interface{})
    if !ok {
        return errors.New("schema fields should be a map")
    }

    // 1. Get the expected checksum value from valueMap, which is encoded as a string.
    // If the expected checksum value is not found, it means that the checksum feature is not enabled when TiCDC sends the data. In this case, this function returns directly.
    o, ok := valueMap["_tidb_row_level_checksum"]
    if !ok {
        return nil
    }
    expected := o.(string)
    if expected == "" {
        return nil
    }

    // expectedChecksum is the expected checksum value passed from TiCDC.
    expectedChecksum, err := strconv.ParseUint(expected, 10, 64)
    if err != nil {
        return errors.Trace(err)
    }

    // 2. Iterate over each field and calculate the checksum value.
    var actualChecksum uint32
    // buf stores the byte slice used to update the checksum value each time.
    buf := make([]byte, 0)
    for _, item := range fields {
        field, ok := item.(map[string]interface{})
        if !ok {
            return errors.New("schema field should be a map")
        }

        // The tidbOp and subsequent columns are not involved in the checksum calculation, because they are used to assist data consumption and not real TiDB column data.
        colName := field["name"].(string)
        if colName == "_tidb_op" {
            break
        }

        // The holder variable stores the type information of each column.
        var holder map[string]interface{}
        switch ty := field["type"].(type) {
        case []interface{}:
            for _, item := range ty {
                if m, ok := item.(map[string]interface{}); ok {
                    holder = m["connect.parameters"].(map[string]interface{})
                    break
                }
            }
        case map[string]interface{}:
            holder = ty["connect.parameters"].(map[string]interface{})
        default:
            log.Panic("type info is anything else", zap.Any("typeInfo", field["type"]))
        }
        tidbType := holder["tidb_type"].(string)

        mysqlType := mysqlTypeFromTiDBType(tidbType)

        // Get the value of each column from the decoded value map according to the name of each column.
        value, ok := valueMap[colName]
        if !ok {
            return errors.New("value not found")
        }
        value, err := getColumnValue(value, holder, mysqlType)
        if err != nil {
            return errors.Trace(err)
        }

        if len(buf) > 0 {
            buf = buf[:0]
        }

        // Generate a byte slice used to update the checksum according to the value and mysqlType of each column, and then update the checksum value.
        buf, err = buildChecksumBytes(buf, value, mysqlType)
        if err != nil {
            return errors.Trace(err)
        }
        actualChecksum = crc32.Update(actualChecksum, crc32.IEEETable, buf)
    }

    if uint64(actualChecksum) != expectedChecksum {
        log.Error("checksum mismatch",
            zap.Uint64("expected", expectedChecksum),
            zap.Uint64("actual", uint64(actualChecksum)))
        return errors.New("checksum mismatch")
    }

    log.Info("checksum verified", zap.Uint64("checksum", uint64(actualChecksum)))
    return nil
}

func mysqlTypeFromTiDBType(tidbType string) byte {
    var result byte
    switch tidbType {
    case "INT", "INT UNSIGNED":
        result = mysql.TypeLong
    case "BIGINT", "BIGINT UNSIGNED":
        result = mysql.TypeLonglong
    case "FLOAT":
        result = mysql.TypeFloat
    case "DOUBLE":
        result = mysql.TypeDouble
    case "BIT":
        result = mysql.TypeBit
    case "DECIMAL":
        result = mysql.TypeNewDecimal
    case "TEXT":
        result = mysql.TypeVarchar
    case "BLOB":
        result = mysql.TypeLongBlob
    case "ENUM":
        result = mysql.TypeEnum
    case "SET":
        result = mysql.TypeSet
    case "JSON":
        result = mysql.TypeJSON
    case "DATE":
        result = mysql.TypeDate
    case "DATETIME":
        result = mysql.TypeDatetime
    case "TIMESTAMP":
        result = mysql.TypeTimestamp
    case "TIME":
        result = mysql.TypeDuration
    case "YEAR":
        result = mysql.TypeYear
    default:
        log.Panic("this should not happen, unknown TiDB type", zap.String("type", tidbType))
    }
    return result
}

// The value is an interface type, which needs to be converted according to the type information provided by the holder.
func getColumnValue(value interface{}, holder map[string]interface{}, mysqlType byte) (interface{}, error) {
    switch t := value.(type) {
    // The column with nullable is encoded as a map, and there is only one key-value pair. The key is the type, and the value is the real value. Only the real value is concerned here.
    case map[string]interface{}:
        for _, v := range t {
            value = v
        }
    }

    switch mysqlType {
    case mysql.TypeEnum:
        // Enum is encoded as a string, which is converted to the int value corresponding to the Enum definition here.
        allowed := strings.Split(holder["allowed"].(string), ",")
        switch t := value.(type) {
        case string:
            enum, err := types.ParseEnum(allowed, t, "")
            if err != nil {
                return nil, errors.Trace(err)
            }
            value = enum.Value
        case nil:
            value = nil
        }
    case mysql.TypeSet:
        // Set is encoded as a string, which is converted to the int value corresponding to the Set definition here.
        elems := strings.Split(holder["allowed"].(string), ",")
        switch t := value.(type) {
        case string:
            s, err := types.ParseSet(elems, t, "")
            if err != nil {
                return nil, errors.Trace(err)
            }
            value = s.Value
        case nil:
            value = nil
        }
    }
    return value, nil
}

// buildChecksumBytes generates a byte slice used to update the checksum, refer to https://github.com/pingcap/tidb/blob/e3417913f58cdd5a136259b902bf177eaf3aa637/util/rowcodec/common.go#L308
func buildChecksumBytes(buf []byte, value interface{}, mysqlType byte) ([]byte, error) {
    if value == nil {
        return buf, nil
    }

    switch mysqlType {
    // TypeTiny, TypeShort, and TypeInt32 are encoded as int32.
    // TypeLong is encoded as int32 if signed, otherwise, it is encoded as int64.
    // TypeLongLong is encoded as int64 if signed, otherwise, it is encoded as uint64.
    // When the checksum feature is enabled, bigintUnsignedHandlingMode must be set to string, which is encoded as string.
    case mysql.TypeTiny, mysql.TypeShort, mysql.TypeLong, mysql.TypeLonglong, mysql.TypeInt24, mysql.TypeYear:
        switch a := value.(type) {
        case int32:
            buf = binary.LittleEndian.AppendUint64(buf, uint64(a))
        case uint32:
            buf = binary.LittleEndian.AppendUint64(buf, uint64(a))
        case int64:
            buf = binary.LittleEndian.AppendUint64(buf, uint64(a))
        case uint64:
            buf = binary.LittleEndian.AppendUint64(buf, a)
        case string:
            v, err := strconv.ParseUint(a, 10, 64)
            if err != nil {
                return nil, errors.Trace(err)
            }
            buf = binary.LittleEndian.AppendUint64(buf, v)
        default:
            log.Panic("unknown golang type for the integral value",
                zap.Any("value", value), zap.Any("mysqlType", mysqlType))
        }
    // Encode float type as float64 and encode double type as float64.
    case mysql.TypeFloat, mysql.TypeDouble:
        var v float64
        switch a := value.(type) {
        case float32:
            v = float64(a)
        case float64:
            v = a
        }
        if math.IsInf(v, 0) || math.IsNaN(v) {
            v = 0
        }
        buf = binary.LittleEndian.AppendUint64(buf, math.Float64bits(v))
    // getColumnValue encodes Enum and Set to uint64 type.
    case mysql.TypeEnum, mysql.TypeSet:
        buf = binary.LittleEndian.AppendUint64(buf, value.(uint64))
    case mysql.TypeBit:
        // Encode bit type as []byte and convert it to uint64.
        v, err := binaryLiteralToInt(value.([]byte))
        if err != nil {
            return nil, errors.Trace(err)
        }
        buf = binary.LittleEndian.AppendUint64(buf, v)
    // Non-binary types are encoded as string, and binary types are encoded as []byte.
    case mysql.TypeVarchar, mysql.TypeVarString, mysql.TypeString, mysql.TypeTinyBlob, mysql.TypeMediumBlob, mysql.TypeLongBlob, mysql.TypeBlob:
        switch a := value.(type) {
        case string:
            buf = appendLengthValue(buf, []byte(a))
        case []byte:
            buf = appendLengthValue(buf, a)
        default:
            log.Panic("unknown golang type for the string value",
                zap.Any("value", value), zap.Any("mysqlType", mysqlType))
        }
    case mysql.TypeTimestamp, mysql.TypeDatetime, mysql.TypeDate, mysql.TypeDuration, mysql.TypeNewDate:
        v := value.(string)
        buf = appendLengthValue(buf, []byte(v))
    // When the checksum feature is enabled, decimalHandlingMode must be set to string.
    case mysql.TypeNewDecimal:
        buf = appendLengthValue(buf, []byte(value.(string)))
    case mysql.TypeJSON:
        buf = appendLengthValue(buf, []byte(value.(string)))
    // Null and Geometry are not involved in the checksum calculation.
    case mysql.TypeNull, mysql.TypeGeometry:
    // do nothing
    default:
        return buf, errors.New("invalid type for the checksum calculation")
    }
    return buf, nil
}

func appendLengthValue(buf []byte, val []byte) []byte {
    buf = binary.LittleEndian.AppendUint32(buf, uint32(len(val)))
    buf = append(buf, val...)
    return buf
}

// Convert []byte to uint64, refer to https://github.com/pingcap/tidb/blob/e3417913f58cdd5a136259b902bf177eaf3aa637/types/binary_literal.go#L105
func binaryLiteralToInt(bytes []byte) (uint64, error) {
    bytes = trimLeadingZeroBytes(bytes)
    length := len(bytes)

    if length > 8 {
        log.Error("invalid bit value found", zap.ByteString("value", bytes))
        return math.MaxUint64, errors.New("invalid bit value")
    }

    if length == 0 {
        return 0, nil
    }

    val := uint64(bytes[0])
    for i := 1; i < length; i++ {
        val = (val << 8) | uint64(bytes[i])
    }
    return val, nil
}

func trimLeadingZeroBytes(bytes []byte) []byte {
    if len(bytes) == 0 {
        return bytes
    }
    pos, posMax := 0, len(bytes)-1
    for ; pos < posMax; pos++ {
        if bytes[pos] != 0 {
            break
        }
    }
    return bytes[pos:]
}
```
