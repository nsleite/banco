
menu = """

    [d]Depositar
    [s]Sacar
    [e]Extrato
    [q]Sair
    
=>"""

saldo = 0
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3
SAQUE_MAXIMO = 500
operacao = []

def depositar(saldo, extrato):
    try:
        deposito = float(input("insira o valor a ser depositado: "))
    except: 
        print("valor inválido!")
        return saldo
    if deposito < 0:
        print("valor inválido!")
        return saldo
    saldo += deposito
    extrato.append(['Depósito', deposito, saldo])
    print(f'Deposito: R${deposito:.2f}, saldo atual: R${saldo:.2f}')
    return saldo

def sacar(saldo, extrato):
    global numero_saques
    try:
        saque = float(input("insira o valor a ser sacado: "))
    except: 
        print("valor inválido!")
        return saldo
    if saque < 0:
        print("valor inválido!")
        return saldo
    if saque > saldo:
        print("saque excede o saldo em conta")
        return saldo
    if saque > SAQUE_MAXIMO:
        print("valor excede o saque máximo de R$ 500.00")
        return saldo
    if numero_saques >= 3:
        print("limite de saques 3 diários excedido")
        return saldo
    saldo -= saque
    numero_saques += 1
    extrato.append(['Saque', saque, saldo])
    print(f'Saque: R${saque:.2f}, saldo atual: R${saldo:.2f}')
    return saldo
    
def mostra_extrato(extrato):
    if len(extrato) == 0:
        print("Não foram realizadas movimentações.")
        return
    for op, val, sal in extrato:
        print(f'operação: {op}, Valor: R${val:.2f}, saldo: R${sal:.2f}')
    return


while True:
    opcao = input(menu)
    if opcao == "d":
        saldo = depositar(saldo, extrato)
    elif opcao == "s":
        saldo = sacar(saldo, extrato)
    elif opcao == "e":
        mostra_extrato(extrato)
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


