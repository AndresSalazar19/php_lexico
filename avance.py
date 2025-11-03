# ------------------------------------------------------------
# Analizador Léxico para PHP
# Proyecto de Lenguajes de Programación - Avance 1
# Integrante: Andrés Salazar (AndresSazalar19)
# ------------------------------------------------------------
import ply.lex as lex
from datetime import datetime
import sys
import os

# ============================================================
# APORTE: Andrés Salazar (AndresSazalar19)
# Componentes: 
# - Variables estándar ($variable)
# - Operadores aritméticos (+, -, *, /, %, **)
# - Operadores de comparación (==, ===, !=, <, >, <=, >=)
# - Palabras reservadas básicas
# - Delimitadores básicos (;, {}, (), [], ,, =)
# - Literales (INTEGER, FLOAT, STRING)
# ============================================================

# Palabras reservadas
reserved_andres = {
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'function': 'FUNCTION',
    'class': 'CLASS',
    'new': 'NEW',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'static': 'STATIC',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'echo': 'ECHO',
    'array': 'ARRAY',
    'define': 'DEFINE',
}

# Lista de tokens
tokens_andres = [
    'VARIABLE',           # Variables estándar: $variable
    'ID',                # Identificadores
    'PLUS',              # +
    'MINUS',             # -
    'TIMES',             # *
    'DIVIDE',            # /
    'MOD',               # %
    'POW',               # **
    'EQ',                # ==
    'IDENTICAL',         # ===
    'NE',                # !=
    'LT',                # <
    'GT',                # >
    'LE',                # <=
    'GE',                # >=
    'SEMICOLON',         # ;
    'LBRACE',            # {
    'RBRACE',            # }
    'LPAREN',            # (
    'RPAREN',            # )
    'LBRACKET',          # [
    'RBRACKET',          # ]
    'COMMA',             # ,
    'ASSIGN',            # =
    'INTEGER',           # 123
    'FLOAT',             # 123.45
    'STRING',            # "texto" o 'texto'
    'PHP_OPEN',          # <?php
    'PHP_CLOSE',         # ?>
    'DOT',               # . (concatenación)
    'COLON',             # :
    'ARROW',             # =>
    'INCREMENT',         # ++
    'DECREMENT',         # --
]

