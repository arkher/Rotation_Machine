import random as rd
import string
import pickle as pkl

class Cilinder:
    def __init__(self, alphabet):
        '''
            Construtor da classe do cilindro. Possui:
            número de rotaçoes;
            conexões que é uma lista de tuplas indicando
            o número identificador de entrada e saída do cilindro;
            alfabeto utilizado;
        '''
        self.rotations = 0
        self.connections = []
        self.alphabet = alphabet

    def build_cilinder(self):
        '''
            Cria uma lista de tuplas (x,y) que representam
            respectivamente o número na entrada e de saída
            do cilindro.
        '''
        alpha_size = len(self.alphabet)
        indexes = [i for i in range(alpha_size)]
        out = indexes.copy()
        rd.shuffle(out)
        for i in range(alpha_size):
            self.connections.append(tuple([indexes[i],out[i]]))

    def rotate(self, direction = 1):
        '''
            realiza a rotação do cilindro (lista circular).
        '''
        if(direction==1):
            # retira o primeiro elemento e o coloca no fim
            self.connections.insert(0,self.connections.pop(len(self.connections)-1))
        else:
            self.connections.insert(len(self.connections)-1,self.connections.pop(0))
            # retira o último elemento e o coloca no início
        
class Maquina_Rotacao:
    '''
        Abstração da máquina de rotação. Objeto que possuirá os cilindros
        e o alfabeto, responsáveis pela crifra do texto claro.
    '''
    def __init__(self):
        '''
            Contrutor da Máquina de rotação e possui:
            alfabeto utilizado;
            uma lista de objetos cilindros;
            tamanho do alfabeto
        '''
        self.alphabet = []
        self.cilinders = []
        self.alphabet_size = 0

    def init_cilinders(self, n_cilinders=3):
        for i in range(n_cilinders):
            cil = Cilinder(self.alphabet)
            cil.build_cilinder()
            self.cilinders.append(cil)

    # abre o arquivo desejado
    def open_arq(self, path):
        try:
            arq = open(path, 'r', encoding='utf8')
            texto = arq.read()
            arq.close()
            return texto
        except:
            print("erro na leitura do arquivo")
            quit()

    # Salva o arquivo desejado
    def save_arq(self, path, text):
        arq = open(path,'w', encoding='utf8')
        arq.write(text)
        arq.close()

    def set_alphabet(self, text=''):
        '''
            Criação do alfabeto:
            o atributo printable da biblioteca string
            retorna uma string com todos os caracteres
        '''
        self.alphabet = list(string.ascii_letters+string.digits+string.punctuation+' \n\táàâãéêèóôòõíìúùçÇÁÀÂÃÉÈÊÍÌÓÒÔÕÙÚ')
        self.alphabet_size = len(self.alphabet)
        print('alfabeto:', self.alphabet)

    def do_it(self, symbol):
        '''
            procura o index do caractere passado
            e passa pelos cilindros
            por meio da indexação 
            e retorna uma saída com o caractere cifrado
            Busca realizada da esquerda para a direita
        '''
        index_symbol = self.alphabet.index(symbol)
        for i in range(len(self.cilinders)):
            t = self.cilinders[i].connections[index_symbol]

            for tup in self.cilinders[i].connections:
                if(tup[1]==t[0]):
                    out = self.cilinders[i].connections.index(tup)
                    break
            index_symbol = out

        return self.alphabet[out]

    def undo_it(self, symbol):
        '''
            Oposto da função do_it.
            Busca por índice realizada da 
            direita para a esquerda.
        '''
        index_symbol = self.alphabet.index(symbol)
        for i in range(len(self.cilinders)-1,-1,-1):
            t = self.cilinders[i].connections[index_symbol]

            for tup in self.cilinders[i].connections:
                if(tup[0]==t[1]):
                    out = self.cilinders[i].connections.index(tup)
                    break
            index_symbol = out

        return self.alphabet[out]

    def encryp(self, path='texto_teste.txt', path_out = 'texto_criptografado.txt'):
        '''
            Criptografia: a função abre o arquivo do caminho passado por parâmetro
            e concatena na variável de saída encrypted_text a saída do algoritmo de
            criptografia que utiliza a função do_it para realizar a passagem por 
            índices de um caractere e realiza a rotação dos cilindros por meio do 
            método rotate do objeto cilindro.
        '''
        text_arq = self.open_arq(path)
        
        encrypted_text = ''

        for i in range(len(text_arq)):
            encrypted_text += self.do_it(text_arq[i])
            
            self.cilinders[0].rotations += 1
            self.cilinders[0].rotate()
            if(self.cilinders[0].rotations%self.alphabet_size==0 and 
                                    self.cilinders[0].rotations!=0):
                self.cilinders[0].rotations = 0
                self.cilinders[1].rotations += 1   
                self.cilinders[1].rotate()
            if(self.cilinders[1].rotations%self.alphabet_size==0 and 
                                    self.cilinders[1].rotations!=0):
                self.cilinders[1].rotations = 0
                self.cilinders[2].rotations += 1   
                self.cilinders[2].rotate()
                
            if(self.cilinders[2].rotations%self.alphabet_size==0 and 
                                    self.cilinders[2].rotations!=0):
                self.cilinders[2].rotations = 0
            
        self.save_arq(path_out, encrypted_text)
      
    def decryp(self, path = 'texto_criptografado.txt', path_out = 'texto_descriptografado.txt'):
        '''
            Descriptografia: a função abre o arquivo criptografado do caminho 
            passado por parâmetro e concatena na variável de saída decrypted_text 
            a saída do algoritmo de descriptografia que utiliza a função undo_it para
            realizar a passagem pelos índices de um caractere nos cilindros na
            ordem contrária à de criptografia e realiza a rotação dos cilindros também
            contrária por meio do método rotate do objeto cilindro.
        '''        
        text_arq = self.open_arq(path)

        decrypted_text = ''
        for c in self.cilinders:
            c.rotations = self.alphabet_size - c.rotations - 1

        for i in range(len(text_arq)-1,-1,-1):
            
            self.cilinders[0].rotations += 1
            self.cilinders[0].rotate(0)
            if(self.cilinders[0].rotations%self.alphabet_size==0 and 
                                    self.cilinders[0].rotations!=0):
                self.cilinders[0].rotations = 0
                self.cilinders[1].rotations += 1   
                self.cilinders[1].rotate(0)
            if(self.cilinders[1].rotations%self.alphabet_size==0 and 
                                    self.cilinders[1].rotations!=0):
                self.cilinders[1].rotations = 0
                self.cilinders[2].rotations += 1   
                self.cilinders[2].rotate(0)
                
            if(self.cilinders[2].rotations%self.alphabet_size==0 and 
                                    self.cilinders[2].rotations!=0):
                self.cilinders[2].rotations = 0
            
            decrypted_text += self.undo_it(text_arq[i])
            
        final_text = ''
        text_list_char = list(decrypted_text)
        text_list_char.reverse()
        for c in text_list_char:
            final_text += c 

        self.save_arq(path_out, final_text)

def clear(n=300):
    for i in range(n):
        print()          
        
if __name__ == '__main__':

    print(' (1) - Criptografar | (2) Descriptografar | (3) Sair ')
    escolha = int(input())
    while(escolha>0 and escolha<3):
        if(escolha==1):
            maquina = Maquina_Rotacao()
            print('digite a localização do arquivo de entrada e saída.') 
            print('ex.:\n./arq_para_criptografar.txt\n./arq_criptografado.txt')
            path = input()
            path_out = input()
            text = maquina.open_arq(path)
            maquina.set_alphabet(text)
            maquina.init_cilinders()
            
            maquina.encryp(path, path_out)
            print('deseja salvar o estado da máquina ? (s)/(n)')
            save = input()
            if(save == 's'):
                with open('maquina.pickle', 'wb') as f:
                    pkl.dump(maquina, f, pkl.HIGHEST_PROTOCOL)
                clear()
                print('arquivo de saída salvo!')
        elif(escolha==2):
            print('digite a localização do arquivo de entrada e saída. ex../arq.txt')
            print('ex.:\n./arq_para_criptografar.txt\n./arq_descriptografado.txt')
            path = input()
            path_out = input()
            with open('maquina.pickle', 'rb') as f:
                maquina = pkl.load(f)
            maquina.decryp(path, path_out)
            clear()
            print('arquivo de saída salvo!')
        elif(escolha==3):
            clear()
            quit()
        else:
            clear()
            print('opção inválida')
        
        print(' (1) - Criptografar | (2) Descriptografar | (3) Sair ')
        escolha = int(input())
        
