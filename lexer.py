import functools
from enum import Enum, auto
from typing import List


class TokenType(Enum):
    """词法单元类型"""

    # 关键字
    VAR = auto()
    FUNC = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # 数据类型关键字
    TYPE_INT = auto()
    TYPE_FLOAT = auto()
    TYPE_BOOL = auto()
    TYPE_STRING = auto()
    TYPE_VOID = auto()
    TYPE_BYTES = auto()
    TYPE_FILE = auto()

    # 字面量
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # 运算符
    PLUS = auto()  # +
    MINUS = auto()  # -
    STAR = auto()  # *
    SLASH = auto()  # /
    PERCENT = auto()  # %
    EQUAL = auto()  # =
    EQUAL_EQUAL = auto()  # ==
    NOT_EQUAL = auto()  # !=
    LESS = auto()  # <
    LESS_EQUAL = auto()  # <=
    GREATER = auto()  # >
    GREATER_EQUAL = auto()  # >=
    AND = auto()  # &&
    OR = auto()  # ||
    NOT = auto()  # !
    BIT_AND = auto()  # &
    BIT_OR = auto()  # |

    # 分隔符
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COMMA = auto()  # ,
    DOT = auto()  # .
    SEMICOLON = auto()  # ;
    COLON = auto()  # :
    ARROW = auto()  # ->

    # 特殊
    EOF = auto()


class Token:

    def __init__(self, token_type: TokenType, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme  # 词素，源文件中的字符串形式
        self.line = line
        self.column = column
        self._value = None  # 实际值，比如"123"对应int类型123

    def __str__(self):
        return f"<{self.token_type} - ({self.line}, {self.column}) - `{self.lexeme}`>"

    def __repr__(self):
        return self.__str__()

    @property
    def value(self):
        if self._value is not None:
            return self._value
        if self.token_type == TokenType.IDENTIFIER:
            self._value = self.lexeme
        elif self.token_type == TokenType.INTEGER:
            self._value = int(self.lexeme)
        elif self.token_type == TokenType.FLOAT:
            self._value = float(self.lexeme)
        elif self.token_type == TokenType.STRING:
            self._value = self.__decode_string(self.lexeme)
        elif self.token_type == TokenType.TRUE:
            self._value = True
        elif self.token_type == TokenType.FALSE:
            self._value = False
        elif self.token_type == TokenType.NULL:
            self._value = None
        else:
            self._value = self.lexeme
        return self._value

    @staticmethod
    def __decode_string(s: str) -> str:
        """解码字符串，转义转义字符，去掉左右引号"""
        ans = s[1:-1]  # 去掉左右引号
        ans = ans.replace("\\\\", "\\")
        ans = ans.replace("\\n", "\n")
        ans = ans.replace("\\t", "\t")
        ans = ans.replace("\\r", "\r")
        ans = ans.replace('\\"', '"')
        return ans


def reset_lexeme(func):
    @functools.wraps(func)
    def wrapper(obj, *args, **kwargs):
        obj.token_start_pos = obj.pos
        obj.token_start_line = obj.current_line
        obj.token_start_column = obj.current_column
        return func(obj, *args, **kwargs)

    return wrapper


class Lexer:
    KEYWORD_TOKENS = {
        "var": TokenType.VAR,
        "func": TokenType.FUNC,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "break": TokenType.BREAK,
        "continue": TokenType.CONTINUE,
        "return": TokenType.RETURN,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "null": TokenType.NULL,
        # 类型关键字
        "int": TokenType.TYPE_INT,
        "float": TokenType.TYPE_FLOAT,
        "bool": TokenType.TYPE_BOOL,
        "str": TokenType.TYPE_STRING,
        "void": TokenType.TYPE_VOID,
        "bytes": TokenType.TYPE_BYTES,
        "file": TokenType.TYPE_FILE,
    }

    # 单字符词法单元映射
    SINGLE_CHAR_TOKENS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,
        "&": TokenType.BIT_AND,
        "|": TokenType.BIT_OR,
        "=": TokenType.EQUAL,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        ";": TokenType.SEMICOLON,
        ":": TokenType.COLON,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
        "!": TokenType.NOT,
    }

    # 双字符词法单元
    TWO_CHAR_TOKENS = {
        "==": TokenType.EQUAL_EQUAL,
        "!=": TokenType.NOT_EQUAL,
        "<=": TokenType.LESS_EQUAL,
        ">=": TokenType.GREATER_EQUAL,
        "&&": TokenType.AND,
        "||": TokenType.OR,
        "->": TokenType.ARROW,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.pos = 0

        self.token_start_line = 1
        self.token_start_column = 1
        self.token_start_pos = 0

        self.current_line = 1
        self.current_column = 1

    @property
    def current_char(self) -> str:
        """当前指向字符"""
        return self.source[self.pos] if self.pos < len(self.source) else ""

    @property
    def next_char(self) -> str:
        """下一个字符"""
        return self.source[self.pos + 1] if self.pos < len(self.source) - 1 else ""

    @property
    def prev_char(self) -> str:
        """上一个字符"""
        return self.source[self.pos - 1] if self.pos > 0 else ""

    @property
    def next_next_char(self) -> str:
        """下下个字符"""
        return self.source[self.pos + 2] if self.pos < len(self.source) - 2 else ""

    @property
    def current_lexeme(self) -> str:
        return self.source[self.token_start_pos : self.pos]

    def run(self):
        while self.current_char != "":
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                self.handle_number()
            elif self.current_char.isalpha() or self.current_char == "_":
                self.handle_alpha()
            elif self.current_char in self.SINGLE_CHAR_TOKENS:
                self.handle_symbol()
            elif self.current_char == '"':
                self.handle_string()
            else:
                self.raise_error(f"Unexpected character: {self.current_char}")
        self.token_start_pos = self.pos + 1
        self.token_start_column += 1
        self.add_token(TokenType.EOF)
        print("The lexical analysis is completed")
        self.log_tokens()

    def log_tokens(self):
        for i in self.tokens:
            print(i)

    def raise_error(self, message: str):

        self.log_tokens()

        raise SyntaxError(
            f"{message}\nline: {self.current_line}\ncolumn: {self.current_column}"
        )

    def advance(self):
        """指针前进"""
        self.pos += 1
        if self.prev_char == "\n":
            self.current_line += 1
            self.current_column = 1
        else:
            self.current_column += 1

    def add_token(self, token_type: TokenType):
        """在token列表中添加一个token"""
        tk = Token(
            token_type,
            self.current_lexeme,
            self.token_start_line,
            self.token_start_column,
        )
        self.tokens.append(tk)

    @reset_lexeme
    def handle_number(self):
        """从当前字符开始，读取一个数字"""

        while self.current_char.isdigit():
            self.advance()
        is_float = self.current_char == "."
        if is_float:
            self.advance()
            while self.current_char.isdigit():
                self.advance()
        if self.current_lexeme.endswith("."):
            self.raise_error(f"There should not be end of '.'")
        if self.current_char.isalpha() or self.current_char in "_.":
            # 数字后不允许紧接字母或下划线；小数点已处理，此时再出现为错误
            self.raise_error(f"Unexpected character: {self.current_char}")
        self.add_token(TokenType.FLOAT if is_float else TokenType.INTEGER)

    @reset_lexeme
    def handle_alpha(self):
        """从当前字符开始，读取一个关键字或变量"""

        self.advance()  # 第一个字符直接读取，后续字符可以为数字需要处理
        while self.current_char.isalnum() or self.current_char == "_":
            self.advance()

        self.add_token(
            self.KEYWORD_TOKENS.get(self.current_lexeme, TokenType.IDENTIFIER)
        )

    @reset_lexeme
    def handle_symbol(self):
        """从当前字符开始去读一个单字符或双字符"""

        two_chars = self.current_char + self.next_char

        if two_chars == "//":
            # 单行注释，跳过一行
            while self.current_char != "\n" and self.current_char != "":
                self.advance()
            return

        if two_chars == "/*":
            while self.current_char != "" and (
                self.current_char + self.next_char != "*/"
            ):
                self.advance()
            if self.current_char == "":
                self.raise_error(f"Unterminated comment")
            self.advance()
            self.advance()
            return

        if two_chars in self.TWO_CHAR_TOKENS:
            token_type = self.TWO_CHAR_TOKENS[two_chars]
            self.advance()
            self.advance()
        elif self.current_char in self.SINGLE_CHAR_TOKENS:

            token_type = self.SINGLE_CHAR_TOKENS[self.current_char]
            self.advance()
        else:
            self.raise_error(f"Unexpected character: {self.current_char}")
            return
        self.add_token(token_type)

    @reset_lexeme
    def handle_string(self):
        """从当前字符开始，读取一个字符串，实际值不包含双引号，并执行转义"""
        self.advance()  # 第一个引号
        while self.current_char != "" and self.current_char != '"':
            if self.current_char == "\n":
                self.raise_error(
                    f"Unterminated string literal: newline is not allowed in a string"
                )

            if self.current_char == "\\":
                if self.next_char == "\n":
                    self.raise_error(
                        f"Unterminated string literal: newline is not allowed in a string"
                    )
                self.advance()
            self.advance()
        if self.current_char == "":
            self.raise_error(
                f"Unterminated string literal: reached EOF before closing quote"
            )
        self.advance()  # 末尾引号
        self.add_token(TokenType.STRING)
