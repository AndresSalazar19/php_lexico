# ------------------------------------------------------------
# Analizador Sintáctico para PHP
# Proyecto de Lenguajes de Programación - Avance 2
# Integrantes: Andrés Salazar (AndresSalazar19), Yadira Suarez (YadiSuarez)
#              Zahid Díaz (LockHurb)
# ------------------------------------------------------------

import ply.yacc as yacc
from lexico import tokens

# ============================================================
# PRECEDENCIA DE OPERADORES
# Operadores lógicos y aritméticos
# ============================================================
precedence = (
    ('left', 'OR_OP'),
    ('left', 'XOR_OP'),
    ('left', 'AND_OP'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'IDENTICAL'),
    ('left', 'PLUS', 'MINUS', 'DOT'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'NOT_OP'),
    ('right', 'POW'),
)

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def p_programa(p):
    '''programa : programa sentencia
                | sentencia'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + [p[2]] if p[2] else p[1]

# ============================================================
# SENTENCIAS PRINCIPALES
# ============================================================
def p_sentencia(p):
    '''sentencia : asigReferencia
                 | varBoolean
                 | expressBol SEMICOLON
                 | varArrayAsociativo
                 | arrayAsociativo SEMICOLON
                 | sentenciaForeach
                 | sentenciaWhile
                 | sentenciaFor
                 | sentenciaIf
                 | funcSinRet
                 | funcConRet
                 | varSuperGlobal
                 | lecturaDatos
                 | impresion
                 | declaracionVariable
                 | asignacionExpresion
                 | RETURN expresion SEMICOLON
                 | BREAK SEMICOLON
                 | CONTINUE SEMICOLON'''
    p[0] = p[1]

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Asignación por referencia
# ============================================================
def p_asigReferencia(p):
    'asigReferencia : VARIABLE ASSIGN AMPERSAND VARIABLE SEMICOLON'
    p[0] = ('asignacion_referencia', p[1], ('referencia', p[4]))

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Variables superglobales
# ============================================================
def p_varSuperGlobal(p):
    'varSuperGlobal : SUPERGLOBALS LBRACKET STRING RBRACKET ASSIGN valor SEMICOLON'
    p[0] = ('asignacion_superGlobal', p[1], p[3], p[6])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Variables booleanas
# ============================================================
def p_varBoolean(p):
    '''varBoolean : VARIABLE ASSIGN expressBol SEMICOLON
                  | VARIABLE ASSIGN VARIABLE SEMICOLON'''
    p[0] = ('asignacion_booleana', p[1], p[3])

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# DECLARACIÓN DE VARIABLES (SIMPLE Y MÚLTIPLE)
# ============================================================
def p_declaracionVariable(p):
    '''declaracionVariable : VARIABLE ASSIGN expresion SEMICOLON
                           | listaDeclaraciones SEMICOLON'''
    if len(p) == 5:
        p[0] = ('declaracion', p[1], p[3])
    else:
        p[0] = ('declaraciones_multiples', p[1])

def p_listaDeclaraciones(p):
    '''listaDeclaraciones : VARIABLE ASSIGN expresion COMMA listaDeclaraciones
                          | VARIABLE ASSIGN expresion'''
    if len(p) == 6:
        p[0] = [(p[1], p[3])] + p[5]
    else:
        p[0] = [(p[1], p[3])]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# ASIGNACIÓN CON EXPRESIONES O CONDICIONALES
# ============================================================
def p_asignacionExpresion(p):
    '''asignacionExpresion : VARIABLE ASSIGN expresion SEMICOLON
                           | VARIABLE ASSIGN expresionCondicional SEMICOLON'''
    p[0] = ('asignacion', p[1], p[3])

def p_expresionCondicional(p):
    '''expresionCondicional : expressBol'''
    p[0] = p[1]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# EXPRESIONES ARITMÉTICAS CON PRECEDENCIA
# ============================================================
def p_expresion(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MOD expresion
                 | expresion POW expresion
                 | expresion DOT expresion
                 | LPAREN expresion RPAREN
                 | MINUS expresion %prec UMINUS
                 | valor'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('uminus', p[2])
    else:
        p[0] = p[1]

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Arrays asociativos
# ============================================================
def p_varArrayAsociativo(p):
    'varArrayAsociativo : VARIABLE ASSIGN arrayAsociativo SEMICOLON' 
    p[0] = ('asignacion_array', p[1], p[3])

def p_arrayAsociativo(p):
    '''arrayAsociativo : LBRACKET contenidoArray RBRACKET
                        | LBRACKET RBRACKET'''   
    if len(p) == 3:
        p[0] = {} 
    else:
        p[0] = p[2]

def p_contenidoArray(p):
    '''contenidoArray : valor ARROW valorArray
                        | valor ARROW valorArray COMMA contenidoArray'''    
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[5][p[1]] = p[3]
        p[0] = p[5]

def p_valorArray(p):
    '''valorArray : valor
                  | arrayAsociativo'''
    p[0] = p[1]

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Expresiones booleanas
# ============================================================
def p_expressBol(p):
    '''expressBol : operacionComparacion
                  | expressBol operadorLogico expressBol
                  | LPAREN expressBol RPAREN
                  | NOT_OP expressBol'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('not', p[2])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])

def p_operacionComparacion(p):
    '''operacionComparacion : valor operadorCom valor
                            | expresion operadorCom expresion
                            | BOOL_TRUE
                            | BOOL_FALSE'''
    if len(p) == 2:
        p[0] = p[1]  
    else:
        p[0] = (p[2], p[1], p[3])

def p_operadorCom(p):
    '''operadorCom : EQ
                   | NE
                   | LT
                   | GE
                   | LE
                   | GT
                   | IDENTICAL'''
    p[0] = p[1]

def p_operadorLogico(p):
    '''operadorLogico : AND_OP
                      | OR_OP
                      | XOR_OP'''
    p[0] = p[1]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# ESTRUCTURA CONDICIONAL IF-ELSEIF-ELSE
# ============================================================
def p_sentenciaIf(p):
    '''sentenciaIf : IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE ELSE LBRACE cuerpo RBRACE
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif
                   | IF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif ELSE LBRACE cuerpo RBRACE'''
    if len(p) == 8:
        # if simple
        p[0] = ('if', p[3], p[6], None, None)
    elif len(p) == 9:
        # if con elseif
        p[0] = ('if', p[3], p[6], p[8], None)
    elif len(p) == 12:
        # if con else
        p[0] = ('if', p[3], p[6], None, p[10])
    else:
        # if con elseif y else
        p[0] = ('if', p[3], p[6], p[8], p[11])

def p_cadenaElseif(p):
    '''cadenaElseif : ELSEIF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE
                    | ELSEIF LPAREN expressBol RPAREN LBRACE cuerpo RBRACE cadenaElseif'''
    if len(p) == 8:
        p[0] = [('elseif', p[3], p[6])]
    else:
        p[0] = [('elseif', p[3], p[6])] + p[8]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# BUCLE FOR
# ============================================================
def p_sentenciaFor(p):
    '''sentenciaFor : FOR LPAREN inicializacion SEMICOLON expressBol SEMICOLON incremento RPAREN LBRACE cuerpo RBRACE'''
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_inicializacion(p):
    '''inicializacion : VARIABLE ASSIGN expresion
                      | VARIABLE ASSIGN valor
                      | '''
    if len(p) > 1:
        p[0] = ('init', p[1], p[3])
    else:
        p[0] = None

def p_incremento(p):
    '''incremento : VARIABLE INCREMENT
                  | VARIABLE DECREMENT
                  | VARIABLE ASSIGN expresion
                  | VARIABLE ASSIGN valor
                  | VARIABLE PLUS_ASSIGN expresion
                  | VARIABLE MINUS_ASSIGN expresion
                  | '''
    if len(p) == 1:
        p[0] = None
    elif len(p) == 3:
        p[0] = ('inc', p[1], p[2])
    else:
        p[0] = ('asig', p[1], p[2], p[3])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Bucle While
# ============================================================
def p_sentenciaWhile(p):
    'sentenciaWhile : WHILE LPAREN expressBol RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('while', p[3], p[6])

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Bucle Foreach
# ============================================================
def p_sentenciaForeach(p):
    '''sentenciaForeach : FOREACH LPAREN VARIABLE AS VARIABLE RPAREN LBRACE cuerpo RBRACE
                        | FOREACH LPAREN VARIABLE AS VARIABLE ARROW VARIABLE RPAREN LBRACE cuerpo RBRACE'''
    if len(p) == 10:
        # foreach ($array as $valor)
        p[0] = ('foreach', p[3], None, p[5], p[8])
    else:
        # foreach ($array as $clave => $valor)
        p[0] = ('foreach', p[3], p[5], p[7], p[10])

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# IMPRESIÓN POR PANTALLA (echo)
# ============================================================
def p_impresion(p):
    '''impresion : ECHO expresion SEMICOLON
                 | ECHO STRING SEMICOLON
                 | ECHO listaExpresiones SEMICOLON'''
    if len(p) == 4:
        p[0] = ('echo', p[2])

def p_listaExpresiones(p):
    '''listaExpresiones : expresion COMMA listaExpresiones
                        | expresion'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# ============================================================
# APORTE: Andrés Salazar (AndresSalazar19)
# FUNCIONES CON RETORNO Y PARÁMETROS OBLIGATORIOS
# ============================================================
def p_funcSinRet(p):
    'funcSinRet : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpo RBRACE'
    p[0] = ('funcion_sin_retorno', p[2], p[4], p[7])

def p_funcConRet(p):
    'funcConRet : FUNCTION ID LPAREN parametros RPAREN LBRACE cuerpoConRetorno RBRACE'
    p[0] = ('funcion_con_retorno', p[2], p[4], p[7])

def p_cuerpoConRetorno(p):
    '''cuerpoConRetorno : sentencia
                        | sentencia cuerpoConRetorno
                        | RETURN expresion SEMICOLON'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [('return', p[2])]

def p_parametros(p):
    '''parametros : VARIABLE
                  | VARIABLE COMMA parametros
                  | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# ============================================================
# APORTE: Yadira Suarez (YadiSuarez)
# Lectura de datos
# ============================================================
def p_lecturaDatos(p):
    '''lecturaDatos : VARIABLE ASSIGN funcionLectura SEMICOLON'''
    p[0] = ('lectura_datos', p[1], p[3])

def p_funcionLectura(p):
    '''funcionLectura : READLINE LPAREN STRING RPAREN
                      | FGETS LPAREN STDIN RPAREN'''
    if p[1].lower() == 'readline':
        p[0] = ('readline', p[3])   # Ej: readline("Ingresa tu nombre: ")
    else:
        p[0] = ('fgets', 'STDIN')   # Ej: fgets(STDIN)

# ============================================================
# VALORES Y CUERPO
# ============================================================
def p_valor(p):
    '''valor : INTEGER
             | FLOAT
             | VARIABLE
             | SUPERGLOBALS
             | STRING
             | BOOL_TRUE
             | BOOL_FALSE
             | NULL'''
    p[0] = p[1]

def p_cuerpo(p):
    '''cuerpo : sentencia
              | sentencia cuerpo
              | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = [p[1]] + p[2]

# ============================================================
# MANEJO DE ERRORES
# ============================================================
errores_sintacticos = []

def p_error(p):
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (tipo {p.type}) en línea {p.lineno}"
        errores_sintacticos.append(mensaje)
        print(mensaje)
    else:
        mensaje = "Error de sintaxis: fin inesperado del archivo"
        errores_sintacticos.append(mensaje)
        print(mensaje)

# ============================================================
# CONSTRUCCIÓN DEL PARSER
# ============================================================
parser = yacc.yacc()

# ============================================================
# FUNCIÓN DE ANÁLISIS
# ============================================================
def analizar_sintactico(codigo, debug=False):
    """
    Analiza sintácticamente un código PHP
    """
    global errores_sintacticos
    errores_sintacticos = []
    
    resultado = parser.parse(codigo, debug=debug)
    
    if errores_sintacticos:
        print(f"\n❌ Se encontraron {len(errores_sintacticos)} errores sintácticos:")
        for error in errores_sintacticos:
            print(f"  • {error}")
        return None
    else:
        print("\n✓ Análisis sintáctico completado sin errores")
        return resultado

if __name__ == '__main__':
    codigo_prueba = '''
    $x = 10;
    $y = 20, $z = 30;
    $resultado = $x + $y * 2;
    $condicion = $x > 5 && $y < 10;
    
    $_POST["nombre"] = "Juan";
    
    $array = ["a" => 1, "b" => 2];
    
    if ($x > 5) {
        echo "Mayor que 5";
    } elseif ($x == 5) {
        echo "Igual a 5";
    } else {
        echo "Menor que 5";
    }
    
    for ($i = 0; $i < 10; $i++) {
        echo $i;
    }
    
    while ($x > 0) {
        $x = $x - 1;
    }
    
    foreach ($array as $key => $value) {
        echo $key, $value;
    }
    
    function sumar($a, $b) {
        return $a + $b;
    }
    '''
    
    resultado = analizar_sintactico(codigo_prueba)
    if resultado:
        print("\n✓ Análisis completado exitosamente")