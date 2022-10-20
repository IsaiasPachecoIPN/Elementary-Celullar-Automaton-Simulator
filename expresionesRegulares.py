from sly import Lexer, Parser
import random
import math

random.seed()

class AnalizadorLexico(Lexer):
    tokens = { CAD } #CAD sera un 1 o 0 ingresados
    ignore = ' \t' #Se ignoran las líneas en blanco 
    literals = { '+', '*', '(', ')', ','}

    #Tokens
    CAD = r'[0|1]+'

    #Operacion realizada cuando encuentre 1 o 0
    def CAD(self,t):
        t.value = str(t.value)
        return t
    
    #Saltos de linea
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    #Errores con la entrada
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class ReParser(Parser):
    tokens = AnalizadorLexico.tokens

    """
    expr : expr *
         | expr + expr
         | expr , expr
         | term
         ;

    term : CAD 
         | ( exr )
         | expr
         ;
    """


    precedence = (
        ('left', '+'),
    )


    @_('expr "*"')
    def expr(self,p):
        times = random.randint(0,10)
        res_cad = p[0] * times
        return res_cad
    
    @_('expr "+" expr')
    def expr(self,p):
        desicion = random.randint(0,1)
        if desicion == 1:
            return p[0]
        else:
            return p[2]
    
    @_('expr "," expr')
    def expr(self,p):
        #print("[",p.expr,",", p.term,"]", end='')
        return p.expr0+p.expr1
    

    @_('term')
    def expr(self,p):
        return p.term

    @_('"(" expr ")"')
    def term(self,p):
        return p[1]

    @_('CAD')
    def term(self,p):
        return p.CAD

def obtnerCadenaRegExpr(RegExpr, longitud_cad):
    lexer = AnalizadorLexico()
    parser = ReParser()
    result = parser.parse(lexer.tokenize(RegExpr))
    tam_res = math.ceil(longitud_cad/len(result))
    print( result )
    return result*tam_res