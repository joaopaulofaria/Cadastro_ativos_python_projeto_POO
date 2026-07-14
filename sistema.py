from enum import Enum
from equipamento import *
from database import Database

class TipoAtivo(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    SOFTWARE = 4
    APLICACAO_WEB = 5
    BANCO_DE_DADOS = 6
    IMPRESSORA = 7
    ESTACAO_TRABALHO = 8

MAPA_TIPOS = {
    1: Notebook,
    2: Servidor,
    3: Roteador,
    4: Software,
    5: AplicacaoWeb,
    6: BancoDeDados,
    7: Impressora,
    8: EstacaoTrabalho
}

class Sistema:
    """Gerencia os arquivos do projeto"""

    def __init__(self):
        self.db     = Database()
        self.ativos = self.db.carregar()

    def menu_crud(self):
        """Mostra o menu inicial"""
        print ("--------------------------------------------------")
        print ("\tCadastro de Ativos")
        print ("--------------------------------------------------")
        print ("\tEscolha qual operação deseja realizar: ")
        print ("--------------------------------------------------")
        print ("\t1 - Cadastro")
        print ("\t2 - Consulta")
        print ("\t3 - Atualização")
        print ("\t4 - Deletar")
        print ("\t5 - Cadastrar vulnerabilidades")
        print ("\t0 - Sair")
        print ("--------------------------------------------------")

    def menu_case(self):
        while True:
            self.menu_crud()
            operacao = self._ler_inteiro("Digite um número: ", minimo=0, maximo=5)

            match operacao:
                case 1:
                    self.cadastrar_ativo()
                case 2:
                    self.consultar_ativo()
                case 3:
                    self.atualizar_ativo()
                case 4:
                    self.deletar_ativo()
                case 5:
                    self.cadastrar_vulnerabilidade()
                case 0:
                    print("Sair")
                    break

    def cadastrar_ativo(self):
        """Cadastrar ativo"""
        limite = self._ler_inteiro("Digite quantos ativos vai cadastrar: ", minimo=1)

        for i in range(limite):
            id_ativo = self._gerar_id()
            hostname = input("Hostname: ")
            responsavel = input("Responsável: ")
            setor = input("Setor: ")
            self._exibir_tipos()
            tipo_codigo = self._ler_inteiro("Tipo do ativo: ", minimo=1, maximo=8)

            busca = MAPA_TIPOS[tipo_codigo]                          
            ativo  = busca(id_ativo, hostname, responsavel, setor)   

            resposta = input("Deseja cadastrar vulnerabilidades? (S/N): ").strip().upper()
            if resposta == "S":
                self._cadastrar_vulns(ativo)

            self.ativos[id_ativo] = ativo
            print(f"Ativo '{hostname}' cadastrado com ID {id_ativo}.")

        self.db.salvar(self.ativos)

    def consultar_ativo(self):
        """Consulta um ativo pelo ID"""
        id_consulta = self._ler_inteiro("ID do ativo: ")
        try:
            self.ativos[id_consulta].exibir()
        except KeyError:
            print("Ativo não encontrado.")

    def atualizar_ativo(self):
        """Atualiza campos de um ativo existente"""
        id_consulta = self._ler_inteiro("ID do ativo: ")
        try:
            ativo = self.ativos[id_consulta]
        except KeyError:
            print("Ativo não encontrado.")
            return

        ativo.exibir()
        print("\n1 - Hostname\n2 - Responsável\n3 - Setor\n4 - Tipo\n0 - Cancelar")
        opcao = self._ler_inteiro("Escolha: ", minimo=0, maximo=4)

        match opcao:
            case 1:
                ativo.hostname = input("Novo hostname: ")
            case 2:
                ativo.responsavel = input("Novo responsável: ")
            case 3:
                ativo.setor = input("Novo setor: ")
            case 4:
                self._exibir_tipos()
                tipo_codigo = self._ler_inteiro("Novo tipo: ", minimo=1, maximo=8)
                nova_classe = MAPA_TIPOS[tipo_codigo]
                novo = nova_classe(ativo.id, ativo.hostname, ativo.responsavel, ativo.setor)
                novo.vulnerabilidades = ativo.vulnerabilidades
                self.ativos[id_consulta] = novo
                ativo = novo
            case 0:
                print("Cancelado.")
                return

        self.db.salvar(self.ativos)
        print("Ativo atualizado.")
        ativo.exibir()

    def deletar_ativo(self):
        """Deleta um ativo e suas vulnerabilidades"""
        id_consulta = self._ler_inteiro("ID do ativo: ")
        try:
            ativo = self.ativos[id_consulta]
        except KeyError:
            print("Ativo não encontrado.")
            return

        ativo.exibir()
        confirmacao = input("Confirma exclusão? (S/N): ").strip().upper()
        if confirmacao != "S":
            print("Operação cancelada.")
            return

        del self.ativos[id_consulta]
        self.db.salvar(self.ativos)
        print(f"Ativo {id_consulta} deletado.")

    def cadastrar_vulnerabilidade(self):
        """Cadastra vulnerabilidade em ativo já existente"""
        id_consulta = self._ler_inteiro("ID do ativo: ")
        try:
            ativo = self.ativos[id_consulta]
        except KeyError:
            print("Ativo não encontrado.")
            return

        ativo.exibir()
        self._cadastrar_vulns(ativo)
        self.db.salvar(self.ativos)
        print("Vulnerabilidade cadastrada.")

    def _gerar_id(self):
        if not self.ativos:
            return 1
        return max(self.ativos.keys()) + 1

    def _ler_inteiro(self, mensagem, minimo=None, maximo=None):
        while True:
            try:
                valor = int(input(mensagem))
                if minimo is not None and valor < minimo:
                    print(f"Erro: valor mínimo é {minimo}.")
                elif maximo is not None and valor > maximo:
                    print(f"Erro: valor máximo é {maximo}.")
                else:
                    return valor
            except ValueError:
                print("Erro: digite um número inteiro.")

    def _exibir_tipos(self):
        print("\nTipos disponíveis:")
        for tipo in TipoAtivo:
            print(f"  {tipo.value} - {tipo.name}")

    def _cadastrar_vulns(self, ativo):
        while True:
            descricao  = input("Descrição: ")
            categoria  = input("Categoria: ")
            severidade = self._ler_inteiro("Severidade (1-Baixa 2-Média 3-Alta 4-Crítica): ", minimo=1, maximo=4)
            status     = self._ler_inteiro("Status (1-Aberta 2-Em tratamento 3-Corrigida 4-Aceita risco): ", minimo=1, maximo=4)
            ativo.adicionar_vulnerabilidade(descricao, categoria, severidade, status)

            continuar = input("Adicionar outra? (S/N): ").strip().upper()
            if continuar != "S":
                break