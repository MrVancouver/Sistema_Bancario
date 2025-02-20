import re
usuario = []
conta = []
conta_excluida = []

QTD_LIMITE_SAQUE = 3
VALOR_LIMITE_SAQUE = 500
AGENCIA = "0001"
num_conta = 0

def sacar(*usuario):#funciona
    #receber os argumentos por nome saldo = saldo
    while True: 
        conta = input("Informe o número da conta que deseja fazer o depósito: ")
        if conta.lower() == 'x':
            print("Operação cancelada.")
            return 
        for pessoa in usuario:
            if pessoa['Número da Conta'] == conta:
                while True:
                    try:
                        print(f"Esta conta está associada à(ao) {pessoa['nome']} dono(a) do CPF {pessoa['cpf']}")
                        valor = float(input("Informe o valor que deseja adicionar à sua conta: "))
                        if valor <= 0:
                            print("Informe um valor válido para depósito.")
                        else:
                            pessoa['Saldo'] = pessoa['Saldo'] - valor
                            pessoa['Extrato'].append(f"Saque no valor de: -{valor:.2f}")
                            print("Depósito realizado com sucesso!")
                            return
                    except ValueError:
                        print("Por favor, informe um número válido.")
        print("Essa conta não existe, tente de novo.")

def deposito(usuario, /):#funciona
    while True: 
        conta = input("Informe o número da conta que deseja fazer o depósito: ")
        if conta.lower() == 'x':
            print("Operação cancelada.")
            return 
        for pessoa in usuario:
            if pessoa['Número da Conta'] == conta:
                while True:
                    try:
                        print(f"Esta conta está associada à(ao) {pessoa['nome']} dono(a) do CPF {pessoa['cpf']}")
                        valor = float(input("Informe o valor que deseja adicionar à sua conta: "))
                        if valor <= 0:
                            print("Informe um valor válido para depósito.")
                        else:
                            pessoa['Saldo'] += valor
                            pessoa['Extrato'].append(f"Depósito no valor de: +{valor:.2f}")
                            print("Depósito realizado com sucesso!")
                            return
                    except ValueError:
                        print("Por favor, informe um número válido.")
        print("Essa conta não existe, tente de novo.")

def extrato(saldo,/,*,extrato):
    #receber os argumentos por nome e posição
    print("teste")

def criar_usuario(usuarios): #funciona
#armazenar os usuários em listas - ok
#so pode ter apenas 1 CPF por usuário e não pode repetir entre eles,somente numeros - ok
#endereço = logradouro, numero - bairro - cidade/UF - ok
    while True:
        cpf = input("Digite seu CPF (somente números): ")
        if cpf.lower() == 'x':
            print("Operação cancelada.")
            return
        # Validação: CPF deve ter exatamente 11 números
        if not re.fullmatch(r"\d{11}", cpf):
            print("CPF inválido! Digite exatamente 11 números.")
            continue
        # Verificação: CPF já cadastrado
        if any(usuario["cpf"] == cpf for usuario in usuarios):
            print("CPF já cadastrado! Digite outro.")
            continue
        break
    try:
        print(f"OK! Vamos dar continuidade à criação da conta de cpf {cpf}")
        cpf = cpf
        nome = input("Diga o nome a quem pertence esta conta: ")
        dia = input("Informe seu dia de Nascimento: ")
        mes = input("Informe seu mes de Nascimento: ")
        ano = input("Informe seu ano de nascimento: ")
        print(f"sua data de nascimento ficou assim : {dia}/{mes}/{ano}")
        data_nas = (f"{dia}/{mes}/{ano}")
        rua = input("Informe a rua/lougradoro ao qual vive essa pessoa: ")
        num = input("Informe o número da residência: ")
        bairro = input("A qual bairro pertence esse endereço: ")
        cidade = input("A qual cidade você se refere: ")
        uf = input("Indique a sigla de Estado(UF): ")
        print(f"Aqui como ficou seu endereço: \n {rua},{num} - {bairro} - {cidade}/{uf}")
        endereco = (f"{rua},{num} - {bairro} - {cidade}/{uf}")
        usuarios.append({"cpf":cpf,"nome":nome,"endereco":endereco,"nascimento":data_nas})
        print("usuário cadastrado com sucesso!")
    except ValueError:
        print("Insira valores válidos correspondentes")

def criar_conta(usuarios,contas,contas_ex,agencia):#funciona
#armazenar contas em uma lista - ok
#número da conta é sequencial, começando a partir do 1 - ok
#todos pertencem a agencia 0001 - ok 
#um usuário pode ter mais de uma conta, mas uma conta pertence a apenas um usuário - ok
#lembrando que a conta não pode existir sem um usuário - ok
    global num_conta
    while True:
        cpf = input("Informe o CPF que estará associado essa nova conta: ")
        if cpf.lower() == 'x':  # Se o usuário digitar 'x', encerra a função
            print("Operação cancelada.")
            return
        for pessoa in usuarios:
            if pessoa["cpf"] == cpf:
                print(f"pessoa encontrada = {pessoa['nome']}")
                break
        else:
            print("Você deve digitar um CPF válido ou criar uma conta...")
            continue
        break
    try:
        print("Vamos dar segmento a sua criação da conta...")
        if contas_ex:
            num_conta = min(pessoa['Número da Conta'] for pessoa in contas_ex)
            for conta in contas_ex:
                contas_ex.remove(conta)
        else:
            num_conta +=1
        nova_conta = ({"Nome":pessoa['nome'],'cpf':cpf,"Agência":agencia,'Saldo':0,"Vezes Sacadas":0,"Número da Conta": num_conta,"Extrato":[]})
        contas.append(nova_conta)
        print("conta criada com sucesso")
        print(f"Conta no nome de: {nova_conta["Nome"]}\n de número: {nova_conta["Número da Conta"]}\n da Agência de número: {nova_conta["Agência"]}")
    except ValueError:
        print("Argumentos Inválidos")

def excluir_conta(contas_ex,contas):#funciona
    while True:
        cpf = input("Informe qual o cpf dono da conta que você deseja excluir: ")
        if cpf.lower() == 'x':
            print("Encerrando Processo...")
            return
        contas_cpf = [conta for conta in contas if conta["cpf"] == cpf]
        if not contas_cpf:
            print("CPF sem contas ou Usuário não criado.")
            continue
        print(f"Contas associadas ao CPF {cpf}")
        for conta in contas_cpf:
            print(f"Conta de número: {conta['Número da Conta']}, com o saldo correspondente à: {conta['Saldo']}")
        while True:
            try:
                numero_conta = int(input("Digite o número da conta que deseja excluir: "))
                for conta in contas_cpf:
                    if conta['Número da Conta'] == numero_conta:
                        contas_ex.append(conta)
                        contas.remove(conta)
                        print("Conta removida com sucesso!")
                        break
                else:
                    print("Número de conta inválido. Tente novamente.")
                    continue
            except ValueError:
                print("Por favor digite um número válido.")
                continue
            break
        break           

def listar_usuarios(usuarios):#funciona
    if not usuarios:
        print("Não há usuários cadastrados!")
        return
    print("===Lista de Usuários===")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']} do CPF: {usuario['cpf']}\nque mora no endereço: {usuario['endereco']} que nasceu na data: {usuario['nascimento']}")

def layout():
    while True:
        tela_inicial = """
        -- Escolha suas opções --
        [1] = Criar Usuário
        [2] = Criar Conta Bancária
        [3] = Excluir Conta Bancária
        [4] = Listar Usuários
        [5] = Sacar Dinheiro
        [6] = Depositar Dinheiro
        [7] = Demonstrar Extrato
        [X] = Fechar o Programa
        """
        print(tela_inicial)
        escolha = input("   => ").lower()

        if escolha == '1':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            criar_usuario(usuario)
        elif escolha == '2':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            criar_conta(usuario,conta,conta_excluida,AGENCIA)
        elif escolha == '3':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            excluir_conta(conta_excluida,conta)
        elif escolha == '4':
            listar_usuarios(usuario)
        elif escolha == '5':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            sacar(usuario=usuario)
        elif escolha == '6':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            deposito(usuario)
        elif escolha == '7':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")



        elif escolha == "x":
            print("Encerrando o Sistema...")
            print("Obrigado Pela Escolha!")
            break
        else:
            print("Indique um valor que seja válido")

print("==== Banco Nacional da DIO 2.0 ====")
layout()
