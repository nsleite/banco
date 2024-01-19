
menu = """

    [d]Depositar
    [s]Sacar
    [e]Extrato
    [q]Sair
    
=>"""

saldo = 0
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3
SAQUE_MAXIMO = 500
operacao = []

def depositar(saldo, operacao):
    global deposito
    try:
        deposito = float(input("insira o valor a ser depositado: "))
    except: 
        print("valor inalido! ")
        return
    saldo += deposito
    operacao.append(['Depósito', deposito, saldo])
    print(f'Deposito: R${deposito}, saldo atual: R${saldo}')
    return saldo, operacao

def sacar():
    pass
def mostra_extrato(operacao):
    for op, val, sal in operacao:
        print(f'operação: {op}, Valor: R${val}, saldo: {sal}')
    return


while True:

    opcao = input(menu)

    if opcao == "d":
        saldo, operacao = depositar(saldo, operacao)

    elif opcao == "s":
        sacar()

    elif opcao == "e":
        mostra_extrato(operacao)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


