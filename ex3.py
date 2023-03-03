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
start: LISTA elementos* P
elementos : elemento (VIR elemento)*
elemento : NUMERO
        | PALAVRA
//Regras Lexicográficas
LISTA:"LISTA"i
NUMERO:"0".."9"+
PALAVRA:"a".."z"+ 
P: "."
VIR:","
//Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

def getIdx(elem,lista):
    for i in range(len(lista)):
        if lista[i] == elem:
            return i
    return -1

class ExemploTransformer(Transformer):
    l = 0
    elems = []
    count = []
    flag = False
    sum = 0
    agora= False
    fim= False
    num= False
    invalid= False
    

    def start(self,elementos):
        #print("start")
        #print("maximo no self: ",self.max)
        #print("soma no self: ",self.soma)
        print("(a) Tamanho da lista: ",self.l)
        maxi = max(self.count)
        i = getIdx(maxi,self.count)
        print("(b) Elemento mais frequente: '",self.elems[i], "' com",maxi,"ocorrencias")
        print("(c) Soma dos elementos: ",self.sum)
        if self.agora and self.num and self.fim and not self.invalid:
            print("(d) A frase é valida")
        else:
            print("(d) A frase é invalida")
        return self.l
    
    def elemento(self,elemento):
        #print("elemento")
        #print(elemento)
        return elemento
        
    
    def NUMERO (self,numero):
        #print("numero")
        #print(numero)
        self.l +=1
        if self.agora:
            self.num = True
        if self.flag:
            self.sum += int(numero)
        if self.l > len(self.elems):
            self.elems.append(str(numero))
            self.count.append(0)
        i = getIdx(str(numero),self.elems)
        self.count[i] += 1
        return int(numero)

    
    def PALAVRA (self,palavra):
        #print("palavra")
        #print(palavra)
        self.l +=1
        if palavra == "fim":
            self.flag = False
            if not self.agora or not self.num:
                self.invalid = True
            self.fim= True
        elif palavra == "agora":
            self.agora= True
            self.flag = True

        if self.l > len(self.elems):
            self.elems.append(str(palavra))
            self.count.append(0)
        i = getIdx(str(palavra),self.elems)
        self.count[i] += 1
        return str(palavra)

    def LISTA(self,lista):
        #print("pe")
        #print(pe)
        return Discard
    
    def P(self,p):
        #print("pe")
        #print(pe)
        return Discard

    def VIR(self,vir):
        #print("vir")
        #print(vir)
        return Discard

    pass

frase = "LISTA agora,1,2,fim,3,agora,3,7,fim ."

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
