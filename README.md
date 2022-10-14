# Pygments lexer for Gothic scripts

## Intro
Pygments lexer for Daedalus, from Piranha Bytes Gothic 1, 2, Addon games.  
It was made to be used primarily in the https://github.com/auronen/gmc/ project to highlight code examples. 
To highlight code during development and get suggestions better use https://github.com/kirides/vscode-daedalus 

Regex patterns are partially based on:  
https://github.com/kirides/vscode-daedalus/blob/master/syntaxes/daedalus.tmLanguage.json

Project structure and setup partially based on:  
https://github.com/fcurella/jsx-lexer  
https://github.com/testdrivenio/vue-lexer  
https://github.com/tremor-rs/tremor-mkdocs-lexer  

## Installation

```shell
pip install git+https://github.com/kamilkrzyskow/gothic-lexer.git
```

## Commands

To create an example html file with the lexers, use the commands below inside the `gothic_lexer` directory:

```shell
# DaedalusLexer
pygmentize -l daedalus.py:DaedalusLexer -x -f html -o result_dae.html -O full,debug_token_types .\example_file.d
```

Compare with the `cpp` lexer:

```shell
# CppLexer
pygmentize -l cpp -f html -o result_cpp.html -O full,debug_token_types .\example_file.d
```
