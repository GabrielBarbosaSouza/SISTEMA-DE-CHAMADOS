class Chamado:
    def __init__(self, titulo: str, descricao: str, categoria: str, prioridade: str, id_usuario: str, status: str ="Aberto"):
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.prioridade = prioridade
        self.status = status
        self.id_usuario = id_usuario