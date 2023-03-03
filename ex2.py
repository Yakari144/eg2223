from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark import Transformer
from lark import Discard



grammar1 = '''
//Regras Sintaticas
start: PE elementos PD
elementos : 
          | elemento (VIR elemento)*
elemento : NUMERO 
//Regras Lexicográficas
NUMERO:"0".."9"+ // [0-9]+
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''
grammar2 = '''
//Regras Sintaticas
start: PE elementos PD
elementos: elemento VIR elementos
        |
elemento : NUMERO 
//Regras Lexicograficas
NUMERO:"0".."9"+
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

grammar3 = '''
//Regras Sintaticas
start: PE elementos PD
elementos: elementos VIR elemento
        |
elemento : NUMERO 
//Regras Lexicograficas
NUMERO:"0".."9"+
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

grammar4 = '''
//Regras Sintaticas
start: PE ( |elementos) PD
elementos: elemento VIR elementos
//elementos: elemento VIR elementos
         | elemento
elemento : NUMERO 
//Regras Lexicograficas
NUMERO:"0".."9"+
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

grammar = '''
//Regras Sintaticas
start: PE elemento* PD
elemento : NUMERO (VIR NUMERO)*
//Regras Lexicográficas
NUMERO:"0".."9"+ 
PE:"["
PD:"]"
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

class ExemploTransformer(Transformer):
    soma = 0
    max = -1

    def start(self,elementos):
        #print("start")
        print("maximo no self: ",self.max)
        print("soma no self: ",self.soma)
        pass
    
    def elemento(self,elemento):
        #print("elemento")
        #print(elemento)
        max = -1
        sum=0
        for element in elemento:
            if element > max or max == -1:
                max = element
            sum += element
        print("maximo: ",max)
        print("soma: ",sum)

    
    def NUMERO (self,numero):
        self.soma += int(numero)
        if self.max < int(numero) or self.max == -1:
            self.max = int(numero)
        #print("numero")
        #print(numero)
        return int(numero)
    
    def PE(self,pe):
        #print("pe")
        #print(pe)
        return str(pe)

    def PD(self,pd):
        #print("pd")
        #print(pd)
        return str(pd)

    def VIR(self,vir):
        #print("vir")
        #print(vir)
        return Discard

    pass

frase = "[1,23,345]"

p = Lark(grammar)   #não muito bem
#p = Lark(grammar1)  #recomendada
#p = Lark(grammar2)  #incorreta
#p = Lark(grammar3)  #incorreta
#p = Lark(grammar4)   #aceitável

tree = p.parse(frase)
#print(tree.pretty())
#for element in tree.children:
  #print(element)


data = ExemploTransformer().transform(tree) # chamar o transformer para obter
#print(data)
