from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

numero = 0;
usuarios = []


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
    
    @property
    def numero(self):
        return self._saldo
    
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
        if not valor_valido(valor): return False
        self.saldo += valor
        print("--------> Operação realizada com sucesso --------")
        print(f'Depósito: R${valor:.2f}, saldo atual R$ {self.saldo:.2f}')

    def sacar(self, valor):
        if not valor_valido(valor): return False
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
        Conta:\t\t{self.numero}
        Titular:\t\t{self.titular}
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
    
    def registar(self, conta):
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
    if not (isinstance(valor, float) or 
            isinstance(valor, int) or valor < 0):
        print('valor inválido!')
        return False
    

