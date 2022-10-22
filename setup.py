from setuptools import find_packages, setup

VERSION = "1.1.0"

setup(
    name="gothic-lexer",
    description="Pygments lexer for the Daedalus scripting language used in Piranha Bytes Gothic series.",
    version=VERSION,
    url="https://github.com/KamilKrzyskow/Gothic-Lexer",
    author="Kamil 'HRY' Krzyśków",
    keywords="pygments daedalus gothic lexer highlight",
    install_requires=[
        "Pygments>=2.12.0",
    ],
    test_suite="tests",
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    entry_points={
        "pygments.lexers": [
            "dae=gothic_lexer:DaedalusLexer",
        ],
    },
)
