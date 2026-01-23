---
title: Integrate TiDB Vector Search with Amazon Bedrock
summary: Learn how to integrate TiDB Vector Search with Amazon Bedrock to build a Retrieval-Augmented Generation (RAG) Q&A bot.
---

# Integrate TiDB Vector Search with Amazon Bedrock

> **Note:**
>
> This document is applicable to TiDB Cloud only and not applicable to TiDB Self-Managed.

This tutorial demonstrates how to integrate the [vector search](/ai/vector-search-overview.md) feature of TiDB with [Amazon Bedrock](https://aws.amazon.com/bedrock/) to build a Retrieval-Augmented Generation (RAG) Q&A bot.

> **Note:**
>
> - The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - The vector search feature is available on [TiDB Self-Managed](/overview.md), [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter)(/tidb-cloud/select-cluster-tier.md#starter), [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential), and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).

> **Tip**
>
> You can view the complete [sample code](https://github.com/aws-samples/aws-generativeai-partner-samples/blob/main/tidb/samples/tidb-bedrock-boto3-rag.ipynb) in Notebook format.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.11 or later](https://www.python.org/downloads/) installed
- [Pip](https://pypi.org/project/pip/) installed
- [AWS CLI](https://aws.amazon.com/cli/) installed

    Ensure your AWS CLI profile is configured to a supported [Amazon Bedrock](https://aws.amazon.com/bedrock/) region for this tutorial. You can find the list of supported regions at [Amazon Bedrock Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html). To switch to a supported region, run the following command:

    ```shell
    aws configure set region <your-region>
    ```

- A {{{ .starter }}} cluster

    Follow [creating a {{{ .starter }}} cluster](/tidb-cloud/select-cluster-tier.md#starter) to create your own TiDB Cloud cluster if you don't have one.

- An AWS account with the [required permissions for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html) and access to the following models:

    - **Amazon Titan Embeddings** (`amazon.titan-embed-text-v2:0`), used for generating text embeddings
    - **Meta Llama 3** (`us.meta.llama3-2-3b-instruct-v1:0`), used for text generation

  If you don't have access, follow the instructions in [Request access to an Amazon Bedrock foundation model](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html#getting-started-model-access).

## Get started

This section provides step-by-step instructions for integrating TiDB Vector Search with Amazon Bedrock to build a RAG-based Q&A bot.

### Step 1. Set the environment variables

Get the TiDB connection information from the [TiDB Cloud console](https://tidbcloud.com/) and set the environment variables in your development environment as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Run the following commands in your terminal to set the environment variables. You need to replace the placeholders in the commands with the corresponding connection parameters obtained from the connection dialog.

    ```shell
    export TIDB_HOST=<your-tidb-host>
    export TIDB_PORT=4000
    export TIDB_USER=<your-tidb-user>
    export TIDB_PASSWORD=<your-tidb-password>
    export TIDB_DB_NAME=test
    ```

### Step 2. Set up the Python virtual environment

1. Create a Python file named `demo.py`:

    ```shell
    touch demo.py
    ```

2. Create and activate a virtual environment to manage dependencies:

    ```shell
    python3 -m venv env
    source env/bin/activate  # On Windows, use env\Scripts\activate
    ```

3. Install the required dependencies:

    ```shell
    pip install SQLAlchemy==2.0.30 PyMySQL==1.1.0 tidb-vector==0.0.9 pydantic==2.7.1 boto3
    ```

### Step 3. Import required libraries

Add the following code to the beginning of `demo.py` to import the required libraries:

```python
import os
import json
import boto3
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
```

### Step 4. Configure the database connection

In `demo.py`, add the following code to configure the database connection:

```python
# ---- Configuration Setup ----
# Set environment variables: TIDB_HOST, TIDB_PORT, TIDB_USER, TIDB_PASSWORD, TIDB_DB_NAME
TIDB_HOST = os.environ.get("TIDB_HOST")
TIDB_PORT = os.environ.get("TIDB_PORT")
TIDB_USER = os.environ.get("TIDB_USER")
TIDB_PASSWORD = os.environ.get("TIDB_PASSWORD")
TIDB_DB_NAME = os.environ.get("TIDB_DB_NAME")

# ---- Database Setup ----
def get_db_url():
    """Build the database connection URL."""
    return f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DB_NAME}?ssl_verify_cert=True&ssl_verify_identity=True"

# Create engine
engine = create_engine(get_db_url(), pool_recycle=300)
Base = declarative_base()
```

### Step 5. Invoke the Amazon Titan Text Embeddings V2 model using the Bedrock runtime client

The Amazon Bedrock runtime client provides you with an `invoke_model` API that accepts the following parameters:

- `modelId`: the model ID of the foundation model available in Amazon Bedrock.
- `accept`: the type of the input request.
- `contentType`: the content type of the input.
- `body`: a JSON string payload consisting of the prompt and the configurations.

In `demo.py`, add the following code to invoke the `invoke_model` API to generate text embeddings using Amazon Titan Text Embeddings and get responses from Meta Llama 3:

```python
# Bedrock Runtime Client Setup
bedrock_runtime = boto3.client('bedrock-runtime')

# ---- Model Invocation ----
embedding_model_name = "amazon.titan-embed-text-v2:0"
dim_of_embedding_model = 512
llm_name = "us.meta.llama3-2-3b-instruct-v1:0"


def embedding(content):
    """Invoke Amazon Bedrock to get text embeddings."""
    payload = {
        "modelId": embedding_model_name,
        "contentType": "application/json",
        "accept": "*/*",
        "body": {
            "inputText": content,
            "dimensions": dim_of_embedding_model,
            "normalize": True,
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    return result_body.get("embedding")


def generate_result(query: str, info_str: str):
    """Generate answer using Meta Llama 3 model."""
    prompt = f"""
    ONLY use the content below to generate an answer:
    {info_str}

    ----
    Please carefully think about the question: {query}
    """

    payload = {
        "modelId": llm_name,
        "contentType": "application/json",
        "accept": "application/json",
        "body": {
            "prompt": prompt,
            "temperature": 0
        }
    }

    body_bytes = json.dumps(payload['body']).encode('utf-8')

    response = bedrock_runtime.invoke_model(
        body=body_bytes,
        contentType=payload['contentType'],
        accept=payload['accept'],
        modelId=payload['modelId']
    )

    result_body = json.loads(response.get("body").read())
    completion = result_body["generation"]
    return completion
```

### Step 6. Create a vector table

In `demo.py`, add the following code to create a vector table to store text and vector embeddings:

```python
# ---- TiDB Setup and Vector Index Creation ----
class Entity(Base):
    """Define the Entity table with a vector index."""
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    content_vec = Column(VectorType(dim=dim_of_embedding_model), comment="hnsw(distance=l2)")

# Create the table in TiDB
Base.metadata.create_all(engine)
```

### Step 7. Save the vector data to {{{ .starter }}}

In `demo.py`, add the following code to save the vector data to your {{{ .starter }}} cluster:

```python
# ---- Saving Vectors to TiDB ----
def save_entities_with_embedding(session, contents):
    """Save multiple entities with their embeddings to the TiDB database."""
    for content in contents:
        entity = Entity(content=content, content_vec=embedding(content))
        session.add(entity)
    session.commit()
```

### Step 8. Run the application

1. In `demo.py`, add the following code to establish a database session, save embeddings to TiDB, ask an example question (such as "What is TiDB?"), and generate results from the model:

    ```python
    if __name__ == "__main__":
        # Establish a database session
        with Session(engine) as session:
            # Example data
            contents = [
                "TiDB is a distributed SQL database compatible with MySQL.",
                "TiDB supports Hybrid Transactional and Analytical Processing (HTAP).",
                "TiDB can scale horizontally and provides high availability.",
                "Amazon Bedrock allows seamless integration with foundation models.",
                "Meta Llama 3 is a powerful model for text generation."
            ]

            # Save embeddings to TiDB
            save_entities_with_embedding(session, contents)

            # Example query
            query = "What is TiDB?"
            info_str = " ".join(contents)

            # Generate result from Meta Llama 3
            result = generate_result(query, info_str)
            print(f"Generated answer: {result}")
    ```

2. Save all changes to `demo.py` and run the script:

    ```shell
    python3 demo.py
    ```

    The expected output is similar to the following:

    ```
    Generated answer:  What is the main purpose of TiDB?
         What are the key features of TiDB?
         What are the key benefits of TiDB?

        ----
        Based on the provided text, here is the answer to the question:
        What is TiDB?
        TiDB is a distributed SQL database compatible with MySQL.

    ## Step 1: Understand the question
    The question asks for the definition of TiDB.

    ## Step 2: Identify the key information
    The key information provided in the text is that TiDB is a distributed SQL database compatible with MySQL.

    ## Step 3: Provide the answer
    Based on the provided text, TiDB is a distributed SQL database compatible with MySQL.

    The final answer is: TiDB is a distributed SQL database compatible with MySQL.
    ```

## See also

- [Vector Data Types](/ai/vector-search-data-types.md)
- [Vector Search Index](/ai/vector-search-index.md)