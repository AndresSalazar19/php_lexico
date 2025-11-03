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
reserved = {
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
