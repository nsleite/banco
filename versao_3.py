from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

numero = 1
usuarios = []
contas = []


class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    _AGENCIA = '0001'

    def __init__(self, titular, numero):
        self._titular = titular
        self._numero = numero
        self._saldo = 0
        self._historico = Historico()

    @classmethod
    def cria_conta(cls, titular, numero):
        return cls(titular, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._AGENCIA
    
    @property
    def titular(self):
        return self._titular
    
    @property 
    def historico(self):
        return self._historico

    def depositar(self, valor):
        self.saldo += valor
        print("--------> Operação realizada com sucesso --------")
        print(f'Depósito: R${valor:.2f}, saldo atual R$ {self.saldo:.2f}')

    def sacar(self, valor):
        if valor > self._saque:
            print("saque excede o saldo em conta")
            return False
        self._saldo -= valor
        print("--------> Operação realizada com sucesso --------")
        print(f'Saque: R${valor:.2f}, saldo atual: R${self.saldo:.2f}')
        return True
    
    def __str__(self):
        return f'''
        Agência:\t\t{self.agencia}
        Conta:\t\t\t{self.numero}
        Titular:\t\t{self.titular.nome}
        '''

class ContaCorrente(Conta):
    def __init__(self, titular, numero, limite=500, limite_saques=3):
        super().__init__(titular, numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao['tipo'] == Saque.__name__])
        
        if numero_saques >= self.limite_saques:
            print("limite de saques 3 diários excedido")
            return False
        if valor > self.limite:
            print(f'valor excede o saque máximo de R$ {self.limite:.2f}')
            return False
        
        return super().sacar(valor)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self.transacoes.append({
            'Tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now()
            })
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.add_transacao(self)

def valor_valido(valor):
    if  valor < 0 or isinstance(valor, str):
        print('valor inválido!')
        return False
    return True

def cria_usuario():
    cpf = input("Informe o cpf (apenas numeros): ")
    if verifica_usuario(cpf):
        print("Já existe usuário cadastrado com esse cpf!")
        return
    nome = input("informe o nome completo: ")
    data = input("informe a data de nascimento no fomato dd-mm-aaaa: ")
    endereco = input("informe o endereço no formato RUA, Nº - CIDADE/UF: ")
    novo_usuario = PessoaFisica(nome, data, cpf, endereco)
    usuarios.append(novo_usuario)
    return

def cria_conta():
    global numero
    numero += 1
    print(numero)
    cpf = input("Informe o CPF do usuário: ")
    usuario = verifica_usuario(cpf)
    if not usuario:
        print('Usuário não encontrado, fluxo de criação de conta encerrado!')
        return
    conta = ContaCorrente(usuario, str(numero))
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print('--------> Conta criada com Sucesso! ---------')
    print(conta)
    return
    
def verifica_usuario(cpf):
    usuario_filtrado = [usuario for usuario in usuarios 
                        if usuario.cpf == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def verifica_conta(numero_conta):
    conta_filtrada = [conta for conta in contas if 
                        conta.numero == numero_conta]
    return conta_filtrada[0] if conta_filtrada else None
    

def verifica_credenciais(usuario, conta):
    if not usuario.cpf == conta.titular.cpf:
        return False
    return True

def depositar():
    cpf = input("informe o cpf do usuario: ")
    titular = verifica_usuario(cpf)
    if not titular:
        print('usuario não cadastrado')
        return
    
    num = input("indique o numero da conta: ")
    conta = verifica_conta(num)
    if not conta:
        print('conta não encontrada')
        return
    if not verifica_credenciais(titular, conta):
        print('conta não pertence ao titular')
        return
    valor = input('insira o valor desejado: ')
    if not valor_valido(valor):
        return
    valor = float(valor)
    deposito = Deposito(valor)
    deposito.registrar(conta)

def sacar():
    pass

def mostra_extrato():
    pass

def lista_contas():
    pass

def menu():
    opcao = input("""\n
    ================= Menu =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q]\tSair
    =>""")
    return opcao

while True:
    opcao = menu()
    if opcao == "d":
        depositar()
    elif opcao == "s":
        saldo = sacar()
    elif opcao == "e":
        mostra_extrato()
    elif opcao =='nu':
        cria_usuario()
    elif opcao == 'nc':
        cria_conta()
    elif opcao == 'lc':
        lista_contas()
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
