"""
Correct tokens for the `general.d` file. Whitespace tokens are included.
"""
from pygments.token import Token

CORRECT_TOKENS = [
    (Token.Comment, "// single line comment"),
    (Token.Text.Whitespace, "\n"),
    (Token.Comment.Multiline, "/*"),
    (Token.Comment.Multiline, "\n    multi "),
    (Token.Comment.Multiline, "*"),
    (Token.Comment.Multiline, "\n    line\n    comment "),
    (Token.Comment.Multiline, "/"),
    (Token.Comment.Multiline, "\n"),
    (Token.Comment.Multiline, "*/"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Declaration, "var"),
    (Token.Text.Whitespace, " "),
    (Token.Keyword.Type, "string"),
    (Token.Text.Whitespace, " "),
    (Token.Name, "a"),
    (Token.Punctuation, ";"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Declaration, "const"),
    (Token.Text.Whitespace, " "),
    (Token.Keyword.Type, "int"),
    (Token.Text.Whitespace, " "),
    (Token.Name, "b"),
    (Token.Text.Whitespace, " "),
    (Token.Operator, "="),
    (Token.Text.Whitespace, " "),
    (Token.Literal.Number.Integer, "7"),
    (Token.Punctuation, ";"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "if"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "else"),
    (Token.Text.Whitespace, " "),
    (Token.Keyword.Reserved, "if"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "else"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "while"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "continue"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "break"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Reserved, "return"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Constant, "true"),
    (Token.Text.Whitespace, "\n"),
    (Token.Keyword.Constant, "false"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "self"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "other"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "item"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "victim"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "hero"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "null"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Builtin.Pseudo, "instance_help"),
    (Token.Text.Whitespace, "\n"),
    (Token.Literal.Number.Float, "123.456"),
    (Token.Text.Whitespace, "\n"),
    (Token.Literal.Number.Integer, "123456"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name.Label, "namespace_label"),
    (Token.Punctuation, ":"),
    (Token.Text.Whitespace, "\n"),
    (Token.Name, "variable_name"),
    (Token.Text.Whitespace, "\n"),
    (Token.Punctuation, "("),
    (Token.Punctuation, ")"),
    (Token.Punctuation, "["),
    (Token.Punctuation, "]"),
    (Token.Punctuation, "{"),
    (Token.Punctuation, "}"),
    (Token.Punctuation, ","),
    (Token.Punctuation, "."),
    (Token.Punctuation, ":"),
    (Token.Punctuation, ";"),
    (Token.Text.Whitespace, "\n"),
    (Token.Operator, "*"),
    (Token.Operator, "-"),
    (Token.Operator, "="),
    (Token.Operator, "+"),
    (Token.Operator, "/"),
    (Token.Operator, "|"),
    (Token.Operator, "&"),
    (Token.Operator, "<"),
    (Token.Operator, ">"),
    (Token.Operator, "!"),
    (Token.Operator, "%"),
    (Token.Operator, "~"),
    (Token.Text.Whitespace, "\n"),
    (Token.Literal.String, '"some text"'),
    (Token.Text.Whitespace, "\n"),
]
