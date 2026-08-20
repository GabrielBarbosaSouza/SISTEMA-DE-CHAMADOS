class Usuario():
    def __init__(self, nome: str, email: str, matricula: str, perfil: str = "Usuario"):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.perfil = perfil