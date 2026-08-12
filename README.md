# SISTEMA DE CHAMADOS

Sistema de gerenciamento de chamados desenvolvido em **Python** com **MySQL**, utilizando Programação Orientada a Objetos (POO), controle de acesso por perfil e interface em terminal com **Rich** e **InquirerPy**.

## FUNCIONALIDADES

### USUÁRIO

- Abrir chamados
- Consultar próprios chamados
- Visualizar detalhes de chamados
- Login utilizando matrícula

### TI

- Visualizar todos os chamados
- Listar chamados abertos
- Listar chamados fechados
- Colocar chamados em atendimento
- Fechar chamados
- Reabrir chamados
- Cadastrar usuários
- Visualizar dashboard

---

## DASHBOARD

O sistema disponibiliza um painel com informações gerais:

- Total de usuários cadastrados
- Total de chamados registrados
- Quantidade de chamados abertos
- Quantidade de chamados fechados

---

## TECNOLOGIAS USADAS

- Python 3
- MySQL
- mysql-connector-python
- Rich
- InquirerPy

---

## ESTRUTURA DO PROJETO

```text
SISTEMA-DE-CHAMADOS/

├── banco/
│   └── conexao.py
│
├── funcoes/
│   ├── chamados.py
│   ├── dashboard.py
│   ├── login.py
│   └── usuarios.py
│
├── menus/
│   ├── menu_chamados.py
│   ├── menu_ti.py
│   └── menu_user.py
│
├── modelos/
│   ├── chamado.py
│   └── usuario.py
│
├── main.py
│
└── README.md
```

---

## BANCO DE DADOS

### TABELA `usuarios`

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    matricula VARCHAR(4) UNIQUE NOT NULL,
    perfil ENUM('Usuario', 'TI') NOT NULL DEFAULT 'Usuario'
);
```

### TABELA `chamados`

```sql
CREATE TABLE chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    categoria ENUM(
        'Hardware',
        'Software',
        'Rede',
        'Impressora'
    ) NOT NULL,
    prioridade ENUM(
        'Baixa',
        'Media',
        'Alta'
    ) NOT NULL,
    status ENUM(
        'Aberto',
        'Em andamento',
        'Fechado'
    ) DEFAULT 'Aberto',
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
```

---

## CONTROLE DE ACESSO

O sistema possui autenticação por matrícula e diferenciação de permissões através do campo **perfil**.

### USUÁRIO

Acesso às funcionalidades:

- Abrir chamado
- Meus chamados
- Ver detalhes de chamados
- Sair

### TI

Acesso às funcionalidades:

- Abrir chamado
- Meus chamados
- Ver detalhes de chamados
- Gerenciar chamados
- Dashboard
- Cadastro de usuários
- Sair

---

## COMO EXECUTAR

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/sistema-de-chamados.git
```

### 2. Entre na pasta do projeto

```bash
cd sistema-de-chamados
```

### 3. Instale as dependências

```bash
pip install mysql-connector-python
pip install rich
pip install InquirerPy
```

### 4. Configure a conexão com o banco

Edite o arquivo:

```python
banco/conexao.py
```

E informe os dados do seu ambiente MySQL:

```python
db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="script"
)
```

### 5. Execute o projeto

```bash
python main.py
```

---

## CONCEITOS APLICADOS

- Programação Orientada a Objetos (POO)
- Modularização
- MySQL
- CRUD
- Relacionamento entre tabelas
- JOINs
- Controle de acesso por perfil
- Autenticação simples
- Tratamento de exceções
- Validação de dados
- Estruturas condicionais
- Estruturas de repetição
- Organização de projetos Python

---

## OBJETIVO DO PROJETO

Este projeto foi desenvolvido com o objetivo de poder implementar aonde trabalho (no futuro), melhorar meu portifólio e consolidar conhecimentos em:

- Python
- Banco de Dados MySQL
- Programação Orientada a Objetos
- Modularização de projetos
- Desenvolvimento de sistemas de gerenciamento

Simulando um ambiente real de Service Desk/Help Desk utilizado em empresas.

---

## AUTOR

**Gabriel Souza**

Auxiliar de TI | Estudante de Ciência da Computação

Projeto desenvolvido para fins de estudo, prática e evolução profissional na área de desenvolvimento de software e analise de dados.
