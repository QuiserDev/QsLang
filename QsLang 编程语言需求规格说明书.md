# QsLang 编程语言需求规格说明书 v1.2

**版本**：1.2  
**作者**：Quiser

---

## 1. 引言

### 1.1 项目概述

QsLang 是一门面向过程的、静态强类型的教学用编程语言。其设计目标是语法简单、易于实现，同时提供足够实用的功能，让使用者能够编写有实际意义的程序。

### 1.2 设计哲学

- **极简语法**：接近 C 语言的子集，易于解析和实现。
- **静态强类型**：所有变量类型编译时确定。
- **Pythonic语义**：在合理的前提下，语义行为参考Python，降低学习成本。
- **未来兼容**：当前版本为面向对象版本预留语法空间。

### 1.3 目标用户

- 编译器实现的学习者。
- 希望快速构建玩具语言的原型开发者。
- 编程语言设计的初学者。

---

## 2. 词法规范

### 2.1 字符集

QsLang 源代码使用 ASCII 字符集，支持以下字符：

- 英文字母：`a-z` `A-Z`
- 数字：`0-9`
- 运算符：`+ - * / % = ! < > & |`
- 分隔符：`( ) { } [ ] , . ; :`
- 箭头：`->`
- 空白符：空格、制表符 `\t`、换行符 `\n`、回车符 `\r`

### 2.2 关键字

```
var         变量声明
func        函数定义
if          条件判断
else        否则分支
while       循环
for         foreach 循环
break       跳出循环
continue    继续下一次循环
return      函数返回
true        布尔真值
false       布尔假值
null        空值（仅用于引用类型）
```

### 2.3 运算符

| 类别 | 运算符               | 结合性 | 描述           |
|----|-------------------|-----|--------------|
| 算术 | `+ - * / % & ｜`   | 左结合 | 加减乘除取模位与位或   |
| 比较 | `== != < > <= >=` | 左结合 | 返回 Bool 类型   |
| 逻辑 | `&&` `\|\|` `!`   | 左结合 | 逻辑与、或、非      |
| 赋值 | `=`               | 右结合 | 赋值运算符        |
| 索引 | `[]`              | 左结合 | 数组索引、字节访问    |
| 成员 | `.`               | 左结合 | 方法调用（仅限内置类型） |

### 2.4 分隔符

| 符号   | 用途            |
|------|---------------|
| `;`  | 语句结束符         |
| `,`  | 分隔参数、变量、数组元素  |
| `()` | 函数调用、表达式分组    |
| `{}` | 代码块           |
| `[]` | 数组字面量、索引、数组类型 |
| `:`  | 变量类型标注        |
| `.`  | 方法调用          |
| `->` | 函数返回值类型标注     |

### 2.5 字面量

#### 整数

- 十进制：`123`, `0`, `-42`
- 十六进制：`0x7F`, `0xFF`

#### 浮点数

- `3.14`, `-0.001`, `5.0`（必须包含小数点前后至少一位数字）

#### 字符串

- 双引号括起：`"hello"`
- 转义序列：
    - `\"` - 双引号
    - `\\` - 反斜杠
    - `\n` - 换行符
    - `\t` - 制表符
    - `\r` - 回车符

#### 布尔

- `true`
- `false`

#### 空值

- `null`（仅用于引用类型）

#### 数组

- `[ expr, expr, ... ]`，元素类型必须一致。
- 空数组 `[]` 必须用于已明确类型的上下文。

### 2.6 标识符

- 正则表达式：`[a-zA-Z_][a-zA-Z0-9_]*`
- 不能与关键字重名。
- 大小写敏感。

### 2.7 注释

```
// 单行注释

/*
   多行注释（不支持嵌套）
*/
```

---

## 3. 数据类型

### 3.1 基本类型

| 类型名      | 描述     | 取值范围               | 默认值     |
|----------|--------|--------------------|---------|
| `Int`    | 有符号整数  | 32位，-2^31 ~ 2^31-1 | 0       |
| `Float`  | 双精度浮点数 | IEEE 754 64位       | 0.0     |
| `Bool`   | 布尔值    | `true` 或 `false`   | `false` |
| `String` | 字符串    | 任意长度               | `""`    |
| `Void`   | 无类型    | 仅用于函数返回值           | 无       |

### 3.2 复合类型

| 类型名      | 描述             | 默认值    |
|----------|----------------|--------|
| `[Type]` | 元素类型为 Type 的数组 | `null` |
| `Bytes`  | 字节序列           | `null` |
| `File`   | 文件对象           | `null` |

**说明**：

- 数组元素类型必须一致，通过 `len` 获取长度，通过索引 `[]` 访问（索引从 0 开始）。
- `Bytes` 为不可变字节序列，与 `[Int]` 是完全不相关的独立类型，无隐式转换。
- `File` 为引用类型，所有操作通过函数或方法调用完成。

### 3.3 类型转换规则

- 所有类型转换必须显式调用内置函数（`int`、`float`、`str`、`bool`）。
- **数值运算例外**：Int 和 Float 混合运算时，Int 隐式转换为 Float。
- 其他情况无隐式类型转换。
- 数值溢出行为：有符号整数溢出时回绕；浮点数溢出时产生平台相关无穷大。

### 3.4 关于方法调用的说明

QsLang v1.x 虽然是面向过程语言，但为了更好的开发体验和为未来版本铺路，支持对**内置类型**
（File、Bytes）进行方法调用。这些调用在编译时会被转换为对应的函数调用：

| 方法调用            | 实际调用                   |
|-----------------|------------------------|
| `f.read()`      | `file_read(f)`         |
| `f.close()`     | `file_close(f)`        |
| `b.hex()`       | `bytes_hex(b)`         |
| `b.slice(0, 2)` | `bytes_slice(b, 0, 2)` |

这种设计确保：

1. 当前版本实现简单（只是语法糖）
2. 开发者体验良好（自然的调用语法）
3. 未来版本可以平滑过渡到真正的面向对象

其他类型（包括未来可能添加的自定义类型）不支持方法调用。

---

## 4. 语法规范

### 4.1 程序结构

```
Program = { FunctionDecl } ;

FunctionDecl = "func", identifier, "(", [ ParameterList ], ")", [ "->", Type ], Block ;
```

执行入口是名为 `main` 的函数：

```python
func main():
# 程序从这里开始执行
    pass
```

### 4.2 语句

```
Statement = VarDecl 
          | IfStmt 
          | WhileStmt 
          | ForStmt
          | BreakStmt
          | ContinueStmt
          | ReturnStmt 
          | ExprStmt 
          | Block ;

VarDecl = "var", identifier, ":", Type, [ "=", Expression ], ";" 
        | "var", identifier, "=", Expression, ";" ;  # 类型推导

IfStmt = "if", "(", Expression, ")", Statement, [ "else", Statement ] ;

WhileStmt = "while", "(", Expression, ")", Statement ;

ForStmt = "for", "(", "var", identifier, "in", Expression, ")", Statement ;

BreakStmt = "break", ";" ;

ContinueStmt = "continue", ";" ;

ReturnStmt = "return", [ Expression ], ";" ;

ExprStmt = Expression, ";" ;

Block = "{", { Statement }, "}" ;
```

### 4.3 表达式

```
Expression = Assignment ;

Assignment = LogicalOr, [ "=", Assignment ] ;

LogicalOr = LogicalAnd, { "||", LogicalAnd } ;

LogicalAnd = Equality, { "&&", Equality } ;

Equality = Comparison, { ("==" | "!="), Comparison } ;

Comparison = Addition, { ("<" | ">" | "<=" | ">="), Addition } ;

Addition = Multiplication, { ("+" | "-"), Multiplication } ;

Multiplication = Unary, { ("*" | "/" | "%"), Unary } ;

Unary = ("!" | "-"), Unary | Call ;

Call = Primary, { "(", [ ArgumentList ], ")" | "[" Expression "]" | "." identifier "(" [ ArgumentList ] ")" } ;

Primary = Literal 
        | identifier 
        | "(", Expression, ")" ;

Literal = IntegerLiteral | FloatLiteral | StringLiteral | BoolLiteral | ArrayLiteral | "null" ;

ArrayLiteral = "[", [ Expression { ",", Expression } ], "]" ;
```

### 4.4 辅助规则

```
ArgumentList = ( PositionalArg | KeywordArg ) { ",", ( PositionalArg | KeywordArg ) } ;
PositionalArg = Expression ;
KeywordArg = identifier "=" Expression ;

Type = "Int" | "Float" | "Bool" | "String" | "Void" | "[" Type "]" | "Bytes" | "File" ;

ParameterList = Parameter { ",", Parameter } ;
Parameter = identifier, ":", Type, [ "=", Expression ] ;
```

---

## 5. 语义规则

### 5.1 作用域规则

1. **块作用域**：每个 `{}` 代码块创建新的作用域。
2. **嵌套作用域**：内部作用域可以访问外部作用域的变量。
3. **变量遮蔽**：内部作用域可以声明与外部同名的变量，**编译器发出警告**。
4. **函数作用域**：函数参数在函数体内可见，属于最外层块作用域。

### 5.2 变量规则

1. 变量必须**先声明后使用**。

2. 同一作用域内不能重复声明同名变量。

3. **变量声明规则**：

   ```python
   var x: Int = 5;      # 显式类型 + 初始化
   var y: Int;          # 显式类型，使用默认值 0
   var z = 5;           # 类型推导为 Int
   var w = "hello";     # 类型推导为 String
   var v = null;        # 错误：无法推导 null 的类型
   var u: File = null;  # 正确：显式指定类型
   ```

4. 赋值时右值类型必须与左值类型一致。

### 5.3 类型规则

1. **算术运算**：
    - 操作数同为 `Int`：返回 `Int`
    - 操作数同为 `Float`：返回 `Float`
    - 混合 `Int` 和 `Float`：`Int` 隐式转 `Float`，返回 `Float`
    - 其他类型组合为类型错误

2. **比较运算**：`== != < > <= >=` 要求操作数类型相同，返回 `Bool`

3. **逻辑运算**：`&& || !` 要求操作数为 `Bool`，返回 `Bool`

4. **条件表达式**：`if` 和 `while` 的条件必须是 `Bool` 类型

5. **数组字面量**：
    - 所有元素类型必须一致
    - 空数组 `[]` 必须用于已明确类型的上下文（如赋值给 `[Int]` 类型变量）

6. **索引运算**：
    - `expr[index]` 要求 `expr` 为 `[Type]` 或 `Bytes`
    - `index` 必须为 `Int`
    - 返回类型：`[Type]` 返回 `Type`，`Bytes` 返回 `Int`（0-255）
    - **索引越界**：访问索引超出 `[0, len-1]` 范围时，产生运行时错误

7. **拼接运算（参考Python）**：
    - `[Type] + [Type]`：返回新的 `[Type]`，元素顺序拼接
    - `String + String`：返回新的 `String`
    - 其他类型组合使用 `+` 为类型错误（需显式转换）

8. **for 循环（参考Python迭代语义）**：
    - 集合表达式必须为 `[Type]` 或 `String`
    - 循环变量类型由编译器推导：
        - 集合为 `[Type]`：变量类型为 `Type`
        - 集合为 `String`：变量类型为 `String`（每个元素是单字符字符串）
    - 循环变量在循环体外不可见

9. **break 和 continue**：
    - 只能在 `while` 或 `for` 循环体内使用
    - 不能跨越函数边界
    - 编译器检查循环嵌套的有效性

### 5.4 函数规则

1. 函数不能嵌套定义。

2. 函数调用可以出现在定义之前（多遍扫描）。

3. 函数参数按值传递。

4. 非 `Void` 函数必须有 `return` 语句。

5. **参数默认值（参考Python）**：默认值表达式在**函数定义时**求值一次，之后每次调用都使用该值。

   ```python
   func test(value: Int = random()):  # random() 在定义时调用一次
       print(value);
   
   test();  # 假设输出 42
   test();  # 也输出 42（相同的值）
   
   func log(msg: String, timestamp: String = getTime()):
       print("[" + timestamp + "] " + msg);
   
   log("start");  # 输出: [1000] start
   sleep(1);
   log("end");    # 输出: [1000] end（相同的时间戳！）
   ```

---

## 6. 标准库

### 6.1 内置函数（参考Python风格）

#### 输出函数

```python
func print(*values: Any, sep: String = " ", end: String = "\n") -> Void:
    # 用法：print("hello", "world", sep=", ")
    ...
```

#### 输入函数

```python
func input(prompt: String = "") -> String:
    # 用法：name = input("请输入姓名：")
    ...
```

#### 类型转换函数

```python
func int(x: Any) -> Int  # 类似 Python 的 int()
func float(x: Any) -> Float  # 类似 Python 的 float()
func str(x: Any) -> String  # 类似 Python 的 str()
func bool(x: Any) -> Bool  # 类似 Python 的 bool()
```

#### 工具函数

```python
func len(s: String) -> Int  # 字符串长度
func len(arr: [Type]) -> Int  # 数组长度
func len(b: Bytes) -> Int  # 字节序列长度
func type(x: Any) -> String  # 返回类型名称
```

### 6.2 文件操作

```python
func open(filename: String, mode: String = "r") -> File
# mode: "r" 读文本, "w" 写文本, "rb" 读二进制, "wb" 写二进制
```

**文件方法**（实际转换为函数调用）：

- `f.read()` → `file_read(f)`  # 读取全部内容
- `f.read(n: Int)` → `file_readn(f, n)`  # 读取 n 个字符
- `f.readline()` → `file_readline(f)`  # 读取一行
- `f.readlines()` → `file_readlines(f)`  # 读取所有行
- `f.read_bytes()` → `file_read_bytes(f)`  # 读取全部字节
- `f.read_bytes(n: Int)` → `file_read_bytes_n(f, n)`  # 读取 n 个字节
- `f.write(s: String)` → `file_write(f, s)`  # 写入字符串
- `f.write_bytes(b: Bytes)` → `file_write_bytes(f, b)`  # 写入字节
- `f.close()` → `file_close(f)`  # 关闭文件
- `f.seek(offset: Int, whence: Int = 0)` → `file_seek(f, offset, whence)`  # 移动指针
- `f.tell()` → `file_tell(f)`  # 获取当前位置

**文件属性函数**：

```python
func file_name(f: File) -> String  # 获取文件名
func file_mode(f: File) -> String  # 获取打开模式
func file_closed(f: File) -> Bool  # 检查文件是否已关闭
```

### 6.3 Bytes 类型

**Bytes 创建函数**：

```python
func bytes(s: String) -> Bytes  # 字符串编码为字节
func bytes_from_int(i: Int) -> Bytes  # 整数转为字节（大端序）
func bytes_from_array(arr: [Int]) -> Bytes  # 数组转为字节（值需在 0-255）
```

**Bytes 方法**（实际转换为函数调用）：

- `b.hex()` → `bytes_hex(b)`  # 转十六进制字符串
- `b.decode(encoding: String = "utf-8")` → `bytes_decode(b, encoding)`  # 解码为字符串
- `b.slice(start: Int, end: Int)` → `bytes_slice(b, start, end)`  # 切片
- `b.len()` → `bytes_len(b)`  # 获取长度
- `b.get(index: Int)` → `bytes_get(b, index)`  # 获取字节（索引运算符 `b[index]` 也可用）

**Bytes 操作函数**：

```python
func bytes_len(b: Bytes) -> Int
func bytes_hex(b: Bytes) -> String
func bytes_decode(b: Bytes, encoding: String = "utf-8") -> String
func bytes_slice(b: Bytes, start: Int, end: Int) -> Bytes
func bytes_get(b: Bytes, index: Int) -> Int
func bytes_concat(a: Bytes, b: Bytes) -> Bytes
```

### 6.4 错误处理

当前版本采用简单的返回值错误处理：

- 文件操作失败时返回 `null`
- 类型转换失败返回默认值
- 对 `null` 对象调用方法将导致运行时错误
- 数组/字节索引越界导致运行时错误

---

## 7. 完整示例

```python
# 计算阶乘
func factorial(n: Int) -> Int:
    if n <= 1:
        return 1

    return n * factorial(n - 1)

# 判断素数
func isPrime(n: Int) -> Bool:
    if n < 2:
        return False

    var i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i = i + 1
   
    return True

# 文件处理示例（使用方法调用语法）
func processFile(filename: String):
    var f = open(filename, "r")
    if f == null:
        print("无法打开文件: ", filename)
        return
    
    var lineNum = 1
    var line = f.readline()
    while line != null:
        print("第 ", str(lineNum), " 行: ", line)
        line = f.readline()
        lineNum = lineNum + 1
    
    f.close()

# 二进制文件复制
func copyFile(src: String, dst: String):
    var srcFile = open(src, "rb")
    var dstFile = open(dst, "wb")
    
    if srcFile == null or dstFile == null:
        print("文件打开失败")
        return
    
    var buffer: Bytes
    var total = 0
    while True:
        buffer = srcFile.read_bytes(4096)
        if buffer.len() == 0:
            break
    
        dstFile.write_bytes(buffer)
        total = total + buffer.len()
    
    srcFile.close()
    dstFile.close()
    print("复制完成，共 ", str(total), " 字节")

# 主函数
func main():
    print("QsLang 程序示例")

    # 数组和 foreach（类型推导）
    var numbers = [2, 3, 5, 7, 11, 13]  # 推导为 [Int]
    for var n in numbers:  # n 推导为 Int
        if isPrime(n):
            print(str(n) + " 是素数")
    
    # 字符串遍历（参考Python：每个字符是字符串）
    var greeting = "Hello"  # 推导为 String
    for var ch in greeting:  # ch 推导为 String（单字符）
        print("字符: " + ch)
    
    # 数值运算（Int 和 Float 混合）
    var a = 5  # Int
    var b = 3.14  # Float
    var c = a + b  # Float: 8.14
    print("c = " + str(c))
    
    # 数组拼接（参考Python）
    var arr1 = [1, 2, 3]
    var arr2 = [4, 5, 6]
    var arr3 = arr1 + arr2  # [1, 2, 3, 4, 5, 6]
    
    # 字符串拼接（参考Python）
    var s1 = "Hello"
    var s2 = "World"
    var s3 = s1 + " " + s2  # "Hello World"
    
    # 变量遮蔽（产生警告）
    var x = 10
    if True:
        var x = "hello"  # 警告：变量 x 遮蔽了外层变量
        print(x)  # 输出 "hello"
    
    # Bytes 示例
    var b1 = bytes("Hello")
    var hex = b1.hex()  # 方法调用语法糖 → "48656c6c6f"
    print("Hex: " + hex)
    
    var b2 = bytes_from_array([72, 101, 108, 108, 111])
    var first = b2[0]  # 索引运算符 → 72
    print("First byte: " + str(first))
    
    var b3 = bytes_concat(b1, b2)
    print("Length: " + str(b3.len()))

# 参数默认值示例（参考Python：定义时求值）
func demo(value: Int = random()):
    print(value)
    
    demo()  # 输出 42
    demo()  # 也输出 42（相同的值）
    
    # null 必须显式类型
    var f: File = null  # 正确
    # var g = null          # 错误：无法推导
```

---

## 8. 编译器实现指南

### 8.1 方法调用的转换实现

```python
# 语义分析阶段
def handleMethodCall(obj, methodName, args):
    type = getType(obj)

    # 只允许内置类型有方法
    if type != "File" and type != "Bytes":
        error("只有内置类型 File 和 Bytes 支持方法调用")

    # 构造实际调用的函数名
    funcName = type.lower() + "_" + methodName  # "file_read"

    # 检查函数是否存在
    if not functionExists(funcName):
        error("类型 " + type + " 没有 '" + methodName + "' 方法")

    # 生成函数调用，obj 作为第一个参数
    call = new
    FunctionCall(funcName)
    call.addArgument(obj)
    for arg in args:
        call.addArgument(arg)

    return call
```

### 8.2 其他检查规则

```python
# 变量遮蔽警告
if currentScope.lookupParent(name) != null:
    warning("变量 '" + name + "' 遮蔽了外层变量")


# for 循环类型推导
def typeCheckForStmt(forNode):
    collectionType = typeCheck(forNode.collection)
    if collectionType instanceof ArrayType:
        forNode.varType = collectionType.elementType
    elif collectionType == StringType:
        forNode.varType = StringType  # 单字符字符串
    else:
        error("foreach 循环的集合必须为数组或字符串")


# break/continue 检查
var loopStack = []


def checkBreak():
    if loopStack.isEmpty():
        error("break 必须在循环体内使用")
    if loopStack.top().function != currentFunction:
        error("break 不能跨越函数边界")


# 参数默认值检查（定义时求值）
def checkDefaultValue(param):
    # 默认值表达式在定义时求值并保存
    defaultValue = evaluate(param.defaultExpr)
    param.cachedDefault = defaultValue
```

### 8.3 标准库函数命名约定

所有标准库函数遵循以下命名规则：

| 前缀               | 含义         | 示例                         |
|------------------|------------|----------------------------|
| `file_`          | 文件操作函数     | `file_read`, `file_close`  |
| `bytes_`         | Bytes 操作函数 | `bytes_hex`, `bytes_slice` |
| `int_`、`float_`等 | 类型转换       | 内置函数直接命名                   |

---

## 9. 后续版本规划

| 版本   | 特性      | 描述                    |
|------|---------|-----------------------|
| v1.x | 面向过程核心  | 当前版本，函数式风格 + 方法调用语法糖  |
| v2.x | 错误处理增强  | Result 类型或异常机制        |
| v2.x | 结构体     | `struct` 类型，但仍然是过程式操作 |
| v3.x | 真正的面向对象 | 类、继承、多态、真正的方法调用       |

**迁移路径**：

- v1.x 的代码在 v3.x 完全兼容
- 方法调用语法糖在 v3.x 自动升级为真正的方法调用
- 开发者无需修改现有代码

---

## 10. 附录

### 10.1 关键字列表

```
var, func, if, else, while, for, break, continue, return, true, false, null
```

### 10.2 内置类型方法映射表

| 类型    | 方法名           | 实际函数                | 描述       |
|-------|---------------|---------------------|----------|
| File  | read          | `file_read`         | 读取全部内容   |
| File  | read(n)       | `file_readn`        | 读取 n 个字符 |
| File  | readline      | `file_readline`     | 读取一行     |
| File  | readlines     | `file_readlines`    | 读取所有行    |
| File  | read_bytes    | `file_read_bytes`   | 读取全部字节   |
| File  | read_bytes(n) | `file_read_bytes_n` | 读取 n 个字节 |
| File  | write         | `file_write`        | 写入字符串    |
| File  | write_bytes   | `file_write_bytes`  | 写入字节     |
| File  | close         | `file_close`        | 关闭文件     |
| File  | seek          | `file_seek`         | 移动指针     |
| File  | tell          | `file_tell`         | 获取位置     |
| Bytes | hex           | `bytes_hex`         | 转十六进制    |
| Bytes | decode        | `bytes_decode`      | 解码为字符串   |
| Bytes | slice         | `bytes_slice`       | 切片       |
| Bytes | len           | `bytes_len`         | 获取长度     |
| Bytes | get           | `bytes_get`         | 获取字节（索引） |

### 10.3 运算符优先级表

| 优先级 | 运算符               | 描述       | 结合性 |
|-----|-------------------|----------|-----|
| 1   | `()` `[]` `.`     | 调用/索引/方法 | 左   |
| 2   | `!` `-`           | 一元运算     | 右   |
| 3   | `*` `/` `%`       | 乘除取模     | 左   |
| 4   | `+` `-`           | 加减       | 左   |
| 5   | `<` `>` `<=` `>=` | 比较       | 左   |
| 6   | `==` `!=`         | 相等性      | 左   |
| 7   | `&&`              | 逻辑与      | 左   |
| 8   | `\|\|`            | 逻辑或      | 左   |
| 9   | `=`               | 赋值       | 右   |