# ------------------------------------------------------------
# Analizador Sintáctico para PHP
# Proyecto de Lenguajes de Programación - Avance 2
# Integrantes: Andrés Salazar (AndresSazalar19, Yadira Suarez (YadiSuarez)
#  Zahid Díaz (LockHurb)
# ------------------------------------------------------------

import ply.yacc as yacc
from lexico import tokens

def p_programa(p):
    '''programa : asigReferencia
               | expressBol'''
# Asignación por referencia
def p_asigReferencia(p):
    'asigReferencia : VARIABLE ASSIGN AMPERSAND VARIABLE SEMICOLON'

# expresiones booleanas
def p_expressBol(p):
    '''expressBol : operacionComparacion 
                    | operacionLogico'''

def p_operacionComparacion(p):
    'operacionComparacion : valor operadorCom valor '

def p_operacionLogico(p):
    'operacionLogico : termLogico operadorLogico termLogico'

def p_termLogico(p):
    '''termLogico : LPAREN operacionComparacion RPAREN 
                | BOOL '''

def p_valor(p):
    '''valor : INTEGER
            | FLOAT
            | VARIABLE'''   

def p_operadorCom(p):
    '''operadorCom : EQ
                 | NE
                 | LT
                 | GE
                 | LE
                 | GT'''
    
def p_operadorLogico(p):
    '''operadorLogico : AND_OP
                       | OR_OP
                       | NOT_OP
                       | XOR_OP'''

def p_error(p):
    print("Error de sintaxix: ")

# BConstrucción del parser
parser = yacc.yacc()

while True:
   try:
       s = input('php> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)