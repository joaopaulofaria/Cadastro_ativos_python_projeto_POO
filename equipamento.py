from enum import Enum

class Severidade(Enum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4

class StatusVuln(Enum):
    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA_RISCO = 4

class Equipamento:
    """Classe base para todos os ativos de TI"""
    def __init__(self, id, hostname, responsavel, setor):
        self.id = id
        self.hostname = hostname
        self.responsavel = responsavel
        self.setor = setor
        self.tipo = None
        self.vulnerabilidades = []

    def adicionar_vulnerabilidade(self, descricao, categoria, severidade, status):
        self.vulnerabilidades.append({
            "descricao" : descricao,
            "categoria" : categoria,
            "severidade": Severidade(severidade).name,
            "status" : StatusVuln(status).name
        })

    def exibir(self):
        print("\n------------------------------------------")
        print(f"ID : {self.id}")
        print(f"Hostname : {self.hostname}")
        print(f"Responsável : {self.responsavel}")
        print(f"Setor : {self.setor}")
        print(f"Tipo : {self.tipo}")
        if self.vulnerabilidades:
            print("Vulnerabilidades:")
            for i, vuln in enumerate(self.vulnerabilidades, start=1):
                print(f"\n  [{i}]")
                print(f" Descrição : {vuln['descricao']}")
                print(f" Categoria : {vuln['categoria']}")
                print(f" Severidade: {vuln['severidade']}")
                print(f" Status : {vuln['status']}")
        else:
            print("Sem vulnerabilidades registradas.")
        print("------------------------------------------")

    def para_dicionario(self):
        """Converte o objeto para dicionário"""
        return {
            "id" : self.id,
            "hostname" : self.hostname,
            "responsavel" : self.responsavel,
            "setor" : self.setor,
            "tipo" : self.tipo,
            "vulnerabilidades" : self.vulnerabilidades
        }

    @staticmethod
    def from_dict(dados):
        """Recria o objeto correto a partir do JSON"""
        mapa = {
            "NOTEBOOK" : Notebook,
            "SERVIDOR" : Servidor,
            "ROTEADOR" : Roteador,
            "SOFTWARE" : Software,
            "APLICACAO_WEB" : AplicacaoWeb,
            "BANCO_DE_DADOS" : BancoDeDados,
            "IMPRESSORA" : Impressora,
            "ESTACAO_TRABALHO" : EstacaoTrabalho
        }
        classe = mapa.get(dados["tipo"], Equipamento)
        obj = classe(dados["id"], dados["hostname"], dados["responsavel"], dados["setor"])
        obj.vulnerabilidades = dados.get("vulnerabilidades", [])
        return obj


class Notebook(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "NOTEBOOK"

class Servidor(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "SERVIDOR"

class Roteador(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "ROTEADOR"

class Software(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "SOFTWARE"

class AplicacaoWeb(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "APLICACAO_WEB"

class BancoDeDados(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "BANCO_DE_DADOS"

class Impressora(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "IMPRESSORA"

class EstacaoTrabalho(Equipamento):
    def __init__(self, id, hostname, responsavel, setor):
        super().__init__(id, hostname, responsavel, setor)
        self.tipo = "ESTACAO_TRABALHO"