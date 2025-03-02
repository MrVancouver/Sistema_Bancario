from abc import ABC, classmethod, abstractmethod
from datetime import datetime
import re
import textwrap

class Cliente:

    def __init__(self, endereco):
        self._endereco = endereco 
        contas = [] #inicializa vazio, pois não recebe conta a princípio
    
    def realizar_transacao(self, conta,transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta) #nesse caso, é adicionado a conta nova na lista de contas


class PessoaF(Cliente):
    def __init__(self, endereco,nome,cpf,data_nasc):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nasc = data_nasc

    @property
    def nome(self):
        return self._nome
    @property
    def cpf(self):
        return self._cpf
    @property
    def data_nasc(self):
        return self._data_nasc


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor>saldo:
            print("Valor de saque, maior do que disponível em conta")
            return False
        elif valor<=0:
            print("Informe um valor maior que Zero")
            return False
        else:
            saldo -= valor
            print("Saque realizado com sucesso")
            return True
    
    def depositar(self, valor):
        saldo = self.saldo

        if valor<=0:
            print("Informe um valor maior que 0")
            return False
        else:
            saldo += valor
            return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente,limite_x=3,limite_v=500):
        super().__init__(numero, cliente)
        self._limite_v = limite_v
        self._limite_x = limite_x

    def sacar(self,valor):
        
        vezes_sacadas = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        if vezes_sacadas>self._limite_x:
            print("Não é possível sacar mais hoje, volte amanhã")
            return False

        elif valor>self._limite_v:
            print("O valor do saque não pode ultrapassar R$500!")
            return False
        
        else:
            return super().sacar(valor)
    
    def __str__(self):
        return f'''
                Agência: {self.agencia}\n
                Número da Conta: {self.numero}\n
                Titular: {self.cliente.nome}
        '''
    

class Historico:
    def __init__(self):
        self._transacoes = [] #iniciamos a lista que será acessada pela função abaixo
    
    @property
    def transacoes(self):
        return self._transacoes #criamos esse método para garantir uma leitura segura e para acessar a lista
    
    def adicionar_transacao(self,transacao):

        self.transacoes.append(#aqui em baixo a lista será acessada pela função property
            {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y às %H:%M")
            }
        )


class Transacao(ABC): #ABC pois vai servir como modelo para as classes filhas, os métodos serão obrigatórios em suas classes filhas
    
    @property
    @abstractmethod
    def valor(self):
        pass #mesmo que nada seja passado, as classes que herdarão Transacao(ABC) poderão modificar. O Importante é que elas tenham esse métodos


    @abstractmethod
    def registrar(self,conta):
        pass


class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    @abstractmethod
    def valor(self):
        return self._valor


    @abstractmethod
    def registrar(self,conta):
        
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    @abstractmethod
    def valor(self):
        return self._valor
    
    @abstractmethod
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [lu]\tListar Usuários
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def listar_usuarios(clientes):
    print("==================================")
    for cliente in clientes:
        print(
            f"""
            Nome: {cliente.nome}\n
            CPF: {cliente.cpf}\n
            Data de Nascimento: {cliente.data_nasc}
            """
            )
        print("==================================")

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def filtrar_clientes(cpf, clientes): #função auxiliar para verificar a existencia de clientes nas demais operações usando o CPF
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes):
    cpf = input("Informe o CPF do novo cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if cliente:
        print("Cliente Já Existe, informe outro CPF")
        return 
    nome = input("Informe o Nome do novo Cliente: ")
    
    padrao = r"\d{2}/\d{2}/\d{4}"
    while True:
        data_nasc = input("Informe a Data de Nascimento no formato DD/MM/AAAA: ")
        if re.fullmatch(padrao,data_nasc):
            print("Data válida: ",data_nasc)
            break
        else:
            print("Formato inválido. Tente novamente!")
    endereco = input("Informe o seu Endereço Completo: ")
    cliente = PessoaF(endereco,nome,cpf,data_nasc)
    clientes.append(cliente)

    print("Cliente Criado com Sucesso!")

def criar_conta(numero_conta,clientes,contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    conta = ContaCorrente.nova_conta(cliente=clientes,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta) 
    print("Conta Criada com Sucesso!")
     
def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))     

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "lu":
            listar_usuarios(clientes)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()



