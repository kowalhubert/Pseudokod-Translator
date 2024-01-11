import ply.lex as lex
import ply.yacc as yacc

# Lista tokenów
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'EQ',
    'LPAREN',
    'RPAREN',
    'EXECUTE',
    'ID',
    'INT',
    'SHOW',
    'WHILE',
    'FOR',
    'COLON',
    'LESSER',
    'GREATER',
    'EQUALS',
    'GTE',
    'LTE',
    'NEQ',
    'SEMICOLON',
)

# Definicje tokenów
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQ = r'='
t_COLON = r':'
t_LESSER = r'<'
t_GREATER = r'>'
t_EQUALS = r'=='
t_GTE = r'>='
t_LTE = r'<='
t_NEQ = r'!='
t_SEMICOLON = r';'


def t_INT(t):
    r'LICZBA'
    t.value = 'int'
    return t

def t_WHILE(t):
    r'DOPOKI'
    return t

def t_FOR(t):
    r'PETLA'
    return t

def t_EXECUTE(t):
    r'->'
    t.value = ';'
    return t

def t_SHOW(t):
    r'POKAZ'
    return t

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Obsługa błędów
def t_error(t):
    print(f'Nieprawidłowy znak: {t.value[0]}')
    t.lexer.skip(1)

# Budowanie leksera
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
)

# Reguły gramatyczne
def p_statements(p):
    '''
    statements : statements statement
               | statement
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]

def p_statement(p):
    '''
    statement : INT ID EQ NUMBER EXECUTE
              | ID EQ expression EXECUTE
              | expression EXECUTE
              | ID comparison NUMBER EXECUTE
              | LPAREN ID comparison NUMBER RPAREN EXECUTE
              | WHILE ID comparison NUMBER COLON expression EXECUTE statements
              | FOR ID NUMBER NUMBER COLON expression EXECUTE statements
    '''
    if len(p) > 2:
        p[0] = ' '.join(map(str, p[1:]))
    if p[1] == "DOPOKI":
        p[0] = f"while({p[2]} {p[3]} {p[4]}){{\n{p[6]}{p[7]}\n{p[8]}\n}}"
    if p[1] == "PETLA":
        p[0] = f"for(int {p[2]} = {p[3]}; {p[2]} < {p[4]}; {p[2]}++){{\n{p[6]}{p[7]}\n {p[8]}\n}}"


def p_comp_op(p):
    '''comparison : LESSER
               | GREATER
               | EQUALS
               | GTE
               | LTE
               | NEQ'''

    p[0] = p[1]

def p_expression_arithmetic(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term
                  | expression POWER term
                  | term'''
    if len(p) > 2:
        p[0] = f"({p[1]} {p[2]} {p[3]})"
    else:
        p[0] = p[1]

def p_term(p):
    '''term : NUMBER
            | LPAREN expression RPAREN
            | ID'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_expression_show(p):
    '''expression : SHOW LPAREN ID RPAREN
                    | SHOW LPAREN NUMBER RPAREN'''
    p[0] = f"System.out.print({p[3]})"

def p_error(p):
    print("Błąd składni")

# Budowanie parsera
parser = yacc.yacc()

# Przykładowy pseudokod wejściowy
pseudocode_input = " LICZBA a = 0 -> LICZBA b = 1 -> LICZBA c = 0 -> PETLA i 0 20: POKAZ(a) -> c = a + b -> a = b -> b = c ->"

# Parsowanie pseudokodu
parsed_code = parser.parse(pseudocode_input)

# Wygenerowanie kodu w Javie na podstawie pseudokodu
java_code = f'''public class Test {{
    public static void main(String[] args) {{
        {parsed_code}
    }}
}}'''

print("Wygenerowany kod w Javie:")
print(java_code)

"""
start
liczba a = 0 ->
liczba b = 1 ->
liczba c = a + b ->
dla liczba i = 0 do 20 krok 1:
pokaz(a) ->
c = a + b ->
a = b ->
b = c ->
koniec
"""