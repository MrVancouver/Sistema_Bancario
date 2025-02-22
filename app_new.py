import re, time
usuario = []
conta = []
conta_excluida = []

QTD_LIMITE_SAQUE = 3
VALOR_LIMITE_SAQUE = 500
AGENCIA = "0001"
num_conta = 0

def sacar(*, usuarios, contas, limite_x, limite_s):#funciona
    #receber os argumentos por nome saldo = saldo
    while True: 
        conta = input("Informe o número da conta que deseja fazer o saque: ")
        if conta.lower() == 'x':
            print("Operação cancelada.")
            return 
        for info_conta in contas:
            if info_conta['Número da Conta'] == int(conta):
                cpf_conta = info_conta['cpf']  # Obtém o CPF da conta encontrada
                for usuario in usuarios:
                    if usuario['cpf'] == cpf_conta:
                        print(f"Esta conta está associada à(ao) {usuario['nome']}, dono(a) do CPF {usuario['cpf']}")
                        while True:
                            try:
                                valor = float(input("Informe o valor que deseja retirar da sua conta: "))
                                if valor <= 0:
                                    print("Informe um valor válido para Saque.")
                                elif valor > limite_s:
                                    print("Saque maior do que o valor estipulado")
                                elif info_conta['Vezes Sacadas'] > limite_x:
                                    print("Limite de saque diário atingido, volte amanhã.")
                                    return
                                elif valor>info_conta['Saldo']:
                                    print("Não possui saldo suficiente para o saque.")
                                else:
                                    info_conta['Saldo'] -= valor
                                    info_conta['Vezes Sacadas'] += 1
                                    info_conta['Extrato'].append(f"Saque no valor de: -{valor:.2f}")
                                    print("Saque realizado com sucesso!")
                                    return
                            except ValueError:
                                print("Por favor, informe um número válido.")        
        print("Essa conta não existe, tente de novo.")

def deposito(contas, usuarios, /): #funciona
    while True: 
        conta = input("Informe o número da conta que deseja fazer o depósito: ")
        if conta.lower() == 'x':
            print("Operação cancelada.")
            return 

        for info_conta in contas:
            if info_conta['Número da Conta'] == int(conta):
                cpf_conta = info_conta['cpf']  # Obtém o CPF da conta encontrada
                
                for usuario in usuarios:
                    if usuario['cpf'] == cpf_conta:
                        print(f"Esta conta está associada à(ao) {usuario['nome']} dono(a) do CPF {usuario['cpf']}")
                        while True:
                            try:
                                valor = int(input("Informe o valor que deseja adicionar à sua conta: "))
                                if valor <= 0:
                                    print("Informe um valor válido para depósito.")
                                else:
                                    info_conta['Saldo'] += valor
                                    info_conta['Extrato'].append(f"Depósito no valor de: +{valor:.2f}")
                                    print("Depósito realizado com sucesso!")
                                    return
                            except ValueError:
                                print("Por favor, informe um número válido.")        
        print("Essa conta não existe, tente de novo.")

def extrato(usuarios,/,*,contas): #funciona
    #receber os argumentos por nome e posição
    while True:
        conta = input("Infomre o número da conta que você deseja ver o extrato: ")
        if conta.lower() == 'x':
            print("Operação Cancelada!")
            return
        
        for info_conta in contas:
            if info_conta['Número da Conta'] == int(conta):
                cpf_conta = info_conta['cpf']
                for usuario in usuarios:
                    if usuario['cpf'] == cpf_conta and info_conta['Extrato']:
                        print(f"Essa conta está associada à(ao) {usuario['nome']} dono(a) do CPF {usuario['cpf']}")
                        print("======= Aqui está o seu Extrato =======\n")
                        for listar in info_conta['Extrato']:
                            print(listar,"\n")
                        print("=========================================")
                        return
                    else:
                        print("Essa conta não possui Extratos")
                        return
        print("Essa conta não existe, tente de novo")
                
def criar_usuario(usuarios): #funciona
#armazenar os usuários em listas - ok
#so pode ter apenas 1 CPF por usuário e não pode repetir entre eles,somente numeros - ok
#endereço = logradouro, numero - bairro - cidade/UF - ok
    while True:
        cpf = input("Digite seu CPF (somente números): ")
        if cpf.lower() == 'x':
            print("Operação cancelada.")
            time.sleep(1)
            return
        # Validação: CPF deve ter exatamente 11 números
        if not re.fullmatch(r"\d{11}", cpf):
            print("CPF inválido! Digite exatamente 11 números.")
            time.sleep(1)
            continue
        # Verificação: CPF já cadastrado
        if any(usuario["cpf"] == cpf for usuario in usuarios):
            print("CPF já cadastrado! Digite outro.")
            time.sleep(1)
            continue
        break
    try:
        print(f"OK! Vamos dar continuidade à criação da conta de cpf {cpf}")
        time.sleep(1)
        cpf = cpf
        nome = input("Diga o nome a quem pertence esta conta: ")
        dia = input("Informe seu dia de Nascimento: ")
        mes = input("Informe seu mes de Nascimento: ")
        ano = input("Informe seu ano de nascimento: ")
        print(f"sua data de nascimento ficou assim : {dia}/{mes}/{ano}")
        time.sleep(1)
        data_nas = (f"{dia}/{mes}/{ano}")
        rua = input("Informe a rua/lougradoro ao qual vive essa pessoa: ")
        num = input("Informe o número da residência: ")
        bairro = input("A qual bairro pertence esse endereço: ")
        cidade = input("A qual cidade você se refere: ")
        uf = input("Indique a sigla de Estado(UF): ")
        print(f"Aqui como ficou seu endereço: \n {rua},{num} - {bairro} - {cidade}/{uf}")
        time.sleep(1)
        endereco = (f"{rua},{num} - {bairro} - {cidade}/{uf}")
        usuarios.append({"cpf":cpf,"nome":nome,"endereco":endereco,"nascimento":data_nas})
        print("usuário cadastrado com sucesso!")
    except ValueError:
        print("Insira valores válidos correspondentes")
        time.sleep(1)

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
                time.sleep(1)
                break
        else:
            print("Você deve digitar um CPF válido ou criar uma conta...")
            continue
        break
    try:
        print("Vamos dar segmento a sua criação da conta...")
        if contas_ex:
            conta_num = min(pessoa['Número da Conta'] for pessoa in contas_ex)
            for conta in contas_ex:
                    if conta['Número da Conta'] == conta_num:
                        contas_ex.remove(conta)
                        break
        else:
            num_conta +=1
            conta_num = num_conta
        nova_conta = ({'Nome':pessoa['nome'],'cpf':cpf,'Agência':agencia,'Saldo':0,'Vezes Sacadas':1,'Número da Conta': conta_num,'Extrato':[]})
        contas.append(nova_conta)
        time.sleep(1)
        print("conta criada com sucesso!")
        time.sleep(1)
        print(f"Conta no nome de: {nova_conta['Nome']}\nde número: {nova_conta['Número da Conta']}\nda Agência de número: {nova_conta['Agência']}")
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

def listar_usuarios(usuarios,contas):#funciona
    if not usuarios:
        print("Não há usuários cadastrados!")
        return
    print("==== Lista de Usuários ====")
    for usuario in usuarios:
        for conta in contas: 
            print(f"Nome: {usuario['nome']} CPF: {usuario['cpf']}\nEndereço: {usuario['endereco']} Nascimento: {usuario['nascimento']}\n")
            print(f"Número da Conta: {conta['Número da Conta']} Número da Agência: {conta['Agência']}\nSaldo: {conta['Saldo']}")
            print("====================================================")

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
            print("No inicio do processo, pressione X para retornar ao menu principal\nao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            time.sleep(1)
            criar_usuario(usuario)
        elif escolha == '2':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            time.sleep(1)
            criar_conta(usuario,conta,conta_excluida,AGENCIA)
        elif escolha == '3':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            time.sleep(1)
            excluir_conta(conta_excluida,conta)
        elif escolha == '4':
            time.sleep(1)
            listar_usuarios(usuario,conta)
        elif escolha == '5':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            sacar(usuarios=usuario,contas=conta,limite_s=VALOR_LIMITE_SAQUE,limite_x=QTD_LIMITE_SAQUE)
        elif escolha == '6':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            deposito(conta,usuario)
        elif escolha == '7':
            print("No inicio do processo, pressione X para retornar ao menu principal\n ao dar continuidade com o processo, o mesmo não poderá ser interrompido.")
            extrato(usuario,contas=conta)



        elif escolha == "x":
            print("Encerrando o Sistema...")
            print("Obrigado Pela Escolha!")
            break
        else:
            print("Indique um valor que seja válido")

print("==== Banco Nacional da DIO 2.0 ====")
layout()
