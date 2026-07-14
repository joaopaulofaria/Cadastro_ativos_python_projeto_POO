import json
from equipamento import Equipamento

class Database:
    """Responsável por salvar e carregar dados em JSON"""

    def __init__(self, filename="ativos.json"):
        self.filename = filename

    def salvar(self, ativos):
        """Salva lista de objetos no JSON"""
        lista = [ativo.to_dict() for ativo in ativos.values()]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=2, ensure_ascii=False)

    def carregar(self):
        """Carrega lista do JSON e reconstrói objetos"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                lista = json.load(f)
                return {item["id"]: Equipamento.from_dict(item) for item in lista}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}