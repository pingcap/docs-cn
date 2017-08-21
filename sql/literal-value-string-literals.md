---
title: 字面值
category: user guide
---

# String Literals

string Literals是一个bytes或者characters的序列, 两端被单引号`'`或者双引号`"`包围, 例如:

```
'example string'
"example string"
```

如果字符串是连续的, 会被合并为一个独立的string. 以下表示是一样的:

```
'a string'
'a' ' ' 'string'
"a" ' ' "string"
```

如果 `ANSI_QUOTES` SQL MODE 开启了, 那么只有单引号内的会被认为是String Literals, 对于双引号内的字符串, 会被认为是一个identifier.

binary string 是一串bytes组成的字符串, 每一个binary string有一个叫做`binary`的character set 和 collation. 一个非二进制的字符串是一个由字符组成的字符串, 它有除`binary`外的character set和与之兼容的collation.

对于两种字符串类型, 比较都是基于每个字符的数值. 对于binary string而言, 比较单元就是字节, 对于非二进制的字符串, 那么单元就是字符, 而有的字符集支持多字节字符.

一个String Literal可以拥有一个可选的`character set introducer` 和 `COLLATE clause`, 可以用来指派特定的字符集跟collation(TiDB 对此只是做了语法上的兼容, 并不实质做处理.)

```
[_charset_name]'string' [COLLATE collation_name]
```

例如:

```
SELECT _latin1'string';
SELECT _binary'string';
SELECT _utf8'string' COLLATE utf8_bin;
```

你可以使用 N'literal' 或者 n'literal'来创建使用national character set的字符串, 下列语句是一样的:

```
SELECT N'some text';
SELECT n'some text';
SELECT _utf8'some text';
```

转义字符:

| 专一序列      |  意义  | 
| :-------: | :-------:| 
| \0  | ASCII NUL(X'00') 字符 |
| \'  | 单引号 |
| \"  | 双引号 |
| \b  | 退格符号 |
| \n  | 换行符 |
| \r  | 回车符 |
| \t  | tab符(制表符) |
| \z  | ASCII 26(Ctrl + Z) |
| \\  | 反斜杠\ |
| \%  | % |
| \_  | _ |

如果要在string literal中使用`'`或者`"`, 有以下几种办法:

* 在`'`引用的字符串中, 可以用`''`来表示单引号.
* 在`"`引用的字符串中, 可以用`""`来表示双引号.
* 前面接转义符`\`.
* 在`'`中表示`"`或者在`"`中表示`'`都不需要特别的处理.

更多[细节](https://dev.mysql.com/doc/refman/5.7/en/string-literals.html).


