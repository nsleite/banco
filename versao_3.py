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
        # usuario = verifica_usuario(titular.cpf)
        # if not usuario:
        #     print('Usuário não encontrado, fluxo de criação de conta encerrado!')
        #     return
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
        return f"{self.__class__.__name__}:
                {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

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



def valor_valido(valor):
    if not (isinstance(valor, float) or 
            isinstance(valor, int) or valor < 0):
        print('valor inválido!')
        return False
    
def verifica_usuario(cpf):
    usuario_filtrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

usuario = {'nome': 'nivaldo',
           'cpf': 12345}
usuarios.append(usuario)
numero += 1
cc = Conta.cria_conta(12345, numero)
print(cc)
