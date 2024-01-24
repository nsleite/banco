
menu = """\n
    ================= Menu =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q]\tSair
    
=>"""

saldo = 0
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3
SAQUE_MAXIMO = 500
AGENCIA = '0001'
operacao = []
usuarios = []
contas = []

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
    extrato.append(['Depósito:\t', f'R$ {deposito:.2f}\t', saldo])
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
    extrato.append(['Saque:\t\t', f'R$ {saque:.2f}\t', saldo])
    print(f'Saque: R${saque:.2f}, saldo atual: R${saldo:.2f}')
    return saldo
    
def mostra_extrato(extrato):
    print('==================== EXTRATO =====================')
    if len(extrato) == 0:
        print("Não foram realizadas movimentações.")
        return
    for op, val, sal in extrato:
        print(op, val, f'saldo: R${sal:.2f}')
    print(f'\n-----> Saldo Final: R$ {extrato[-1][-1]:.2f}')
    return

def cria_usuario():
    cpf = input("Informe o cpf (apenas numeros): ")
    if verifica_usuario(cpf):
        print("Já existe usuário cadastrado com esse cpf!")
        return
    nome = input("informe o nome completo: ")
    data = input("informe a data de nascimento no fomato dd-mm-aaaa: ")
    endereco = input("informe o endereço no formato RUA, Nº - CIDADE/UF: ")
    usuarios.append({'nome': nome, 'cpf': cpf, 
                     'data_nascimento': data, 
                     'endereco': endereco})
    print('--------> Usuário criado com sucesso! --------')
    return

def verifica_usuario(cpf):
    usuario_filtrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def cria_conta():
    numero_conta = 1 + (len(contas))
    cpf = input("Informe o CPF do usuário: ")
    usuario = verifica_usuario(cpf)
    if usuario:
        contas.append({'agencia': AGENCIA,
                       'conta': numero_conta,
                       'usuario': usuario['nome'],
                       'cpf_usuario': usuario['cpf']})
        print('--------> Conta criada com Sucesso! ---------')
        return
    print('Usuário não encontrado, fluxo de criação de conta encerrado!')
    return

def lista_contas():
    for conta in contas:
        print(f'''\n =====================================================
                Agência:\t{conta['agencia']}
                Conta:\t\t{conta['conta']}
                Titular:\t{conta['usuario']}\n
            ''')
    return


while True:
    opcao = input(menu)
    if opcao == "d":
        saldo = depositar(saldo, extrato)
    elif opcao == "s":
        saldo = sacar(saldo, extrato)
    elif opcao == "e":
        mostra_extrato(extrato)
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


