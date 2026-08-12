from rich import print
from rich.table import Table
from modelos.chamado import Chamado
from banco.conexao import db, cursor

   
def abrir_chamados():
    while True:
        titulo = input("Insira um título: ").strip()

        if titulo:
            break
        print("[yellow]O Título não pode ficar vázio![/]")


    while True:
        descricao = input("Descreva o problema: ").strip()

        if descricao:
            break
        print("[yellow]A Descricao não pode ficar vázia![/]")


    while True:
        categoria = input("Qual a categoria (Hardware/Software/Rede/Impressora): ").strip().title()

        if categoria in ["Hardware", "Software", "Rede", "Impressora"]:
            break
        print("[yellow]Categoria inválida.[/]")


    while True:
        prioridade = input("Qual a prioridade (Baixa/Media/Alta): ").strip().title()

        if prioridade in ["Baixa", "Media", "Alta"]:
            break
        print("[red]Prioridade inválida.[/]")
    
    
    while True:
        matricula = input("Digite o seu ID (4 primeiros dígitos do CPF): ")

        if len(matricula) == 4 and matricula.isdigit():
            break
        print("[red]Digite exatamente 4 números.[/]")
    
    
    cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (matricula,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("[red]Usuário não encontrado.[/]")
        return
    
    id_usuario = resultado[0]

    chamado = Chamado(
        titulo = titulo,
        descricao = descricao,
        categoria = categoria,
        prioridade = prioridade,
        id_usuario = id_usuario
    )
    
    cursor.execute("""
        INSERT INTO chamados
        (titulo, descricao, categoria, prioridade, id_usuario)
        VALUES (%s, %s, %s, %s, %s)
    """, (chamado.titulo, chamado.descricao, chamado.categoria, chamado.prioridade, chamado.id_usuario))

    db.commit()
    print("\n[green]Chamado aberto![/]")


def fechar_chamado():
    listar_chamados_abertos()

    while True:
        try:
            id_chamado = int(input("\nDigite o ID do chamado que deseja fechar: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")

    cursor.execute("""
        SELECT status
        FROM chamados
        WHERE id = %s
    """, (id_chamado,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("[red]Chamado não encontrado.[/]")
        return

    elif resultado[0] == "Fechado":
        print("[yellow]Esse chamado já está fechado.[/]")
        return

    cursor.execute("""
        UPDATE chamados
        SET status = 'Fechado',
            data_fechamento = NOW()
        WHERE id = %s
    """, (id_chamado,))

    db.commit()

    print("\n[green]Chamado fechado com sucesso![/]")
    
    
def reabrir_chamado():
    listar_chamados_fechados()

    while True:
        try:
            id_chamado = int(input("\nDigite o ID do chamado que deseja reabrir: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")

    cursor.execute("""
        SELECT status
        FROM chamados
        WHERE id = %s
    """, (id_chamado,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("[red]Chamado não encontrado.[/]")
        return

    elif resultado[0] != "Fechado":
        print("[yellow]Esse chamado já está aberto.[/]")
        return

    cursor.execute("""
        UPDATE chamados
        SET status = 'Aberto',
            data_fechamento = NULL
        WHERE id = %s
    """, (id_chamado,))

    db.commit()

    print("\n[green]Chamado reaberto com sucesso![/]")


def listar_chamados():    
    cursor.execute("""
        SELECT id, titulo, categoria, prioridade, status
        FROM chamados
        ORDER BY id DESC
    """)
    
    chamados = cursor.fetchall()
    if not chamados:
        print("\n[red]Nenhum chamado encontrado.[/]")
        return
    
    tabela_chamados = Table(title="Lista de Chamados", title_justify="center")
    tabela_chamados.add_column("ID", justify="left")
    tabela_chamados.add_column("Título", justify="left")
    tabela_chamados.add_column("Categoria", justify="left")
    tabela_chamados.add_column("Prioridade", justify="left")
    tabela_chamados.add_column("Status", justify="left")
    
    for id_chamado, titulo, categoria, prioridade, status in chamados:
        tabela_chamados.add_row(str(id_chamado), str(titulo), str(categoria), str(prioridade), str(status))

    print(tabela_chamados)


def listar_chamados_abertos():
    cursor.execute("""
        SELECT id, titulo, categoria, prioridade, status FROM chamados
        WHERE status IN ('Aberto', 'Em andamento')
        ORDER BY id DESC;
    """)
    
    chamados = cursor.fetchall()
    if not chamados:
        print("\n[red]Nenhum chamado encontrado.[/]")
        return

    tabela_chamados = Table(title="Lista de Chamados Abertos", title_justify="center")
    tabela_chamados.add_column("ID", justify="left")
    tabela_chamados.add_column("Título", justify="left")
    tabela_chamados.add_column("Categoria", justify="left")
    tabela_chamados.add_column("Prioridade", justify="left")
    tabela_chamados.add_column("Status", justify="left")
    
    for id_chamado, titulo, categoria, prioridade, status in chamados:
        tabela_chamados.add_row(str(id_chamado), str(titulo), str(categoria), str(prioridade), str(status))

    print(tabela_chamados)


def listar_chamados_fechados():
    cursor.execute("""
        SELECT id, titulo, categoria, prioridade, status FROM chamados
        WHERE status = 'Fechado'
        ORDER BY id DESC;
    """)
    
    chamados = cursor.fetchall()
    if not chamados:
        print("\n[red]Nenhum chamado encontrado.[/]")
        return

    tabela_chamados = Table(title="Lista de Chamados Fechados", title_justify="center")
    tabela_chamados.add_column("ID", justify="left")
    tabela_chamados.add_column("Título", justify="left")
    tabela_chamados.add_column("Categoria", justify="left")
    tabela_chamados.add_column("Prioridade", justify="left")
    tabela_chamados.add_column("Status", justify="left")
    
    for id_chamado, titulo, categoria, prioridade, status in chamados:
        tabela_chamados.add_row(str(id_chamado), str(titulo), str(categoria), str(prioridade), str(status))

    print(tabela_chamados)


def meus_chamados():
    while True:
        matricula = input("Digite o seu ID (4 primeiros dígitos do CPF): ").strip()

        if not (len(matricula) == 4 and matricula.isdigit()):
            print("[yellow]Digite exatamente 4 números.[/]")
            continue
        
        break
    
    cursor.execute("""
       SELECT
        c.id AS id_chamado,
        u.nome AS nome_usuario,
        c.titulo,
        c.descricao,
        c.categoria,
        c.status
        FROM chamados AS c
        JOIN usuarios AS u
            ON c.id_usuario = u.id
        WHERE u.matricula = %s
        ORDER BY c.id DESC;            
    """, (matricula,))

    chamados = cursor.fetchall()
    if not chamados:
        print("[red]Nenhum chamado encontrado.[/]")
        return
    
    tabela_chamados = Table(title="Meus Chamados", title_justify="center")
    tabela_chamados.add_column("ID do Chamado", justify="left")
    tabela_chamados.add_column("Nome", justify="left")
    tabela_chamados.add_column("Título", justify="left")
    tabela_chamados.add_column("Descrição", justify="left")
    tabela_chamados.add_column("Categoria", justify="left")
    tabela_chamados.add_column("Status", justify="left")
    
    for id_chamado, nome, titulo, descricao, categoria, status in chamados:
        tabela_chamados.add_row(
            str(id_chamado),
            str(nome),
            str(titulo),
            str(descricao),
            str(categoria),
            str(status)
        )
        
    print(tabela_chamados)
    
    
def detalhes_chamado():
    while True:
        try:
            id_chamado = int(input("Digite o ID do Chamado: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")
    
    cursor.execute("""
        SELECT
        c.id AS id_chamado,
        u.nome AS nome_usuario,
        u.matricula,
        c.titulo,
        c.descricao,
        c.categoria,
        c.prioridade,
        c.status,
        c.data_abertura,
        c.data_fechamento
        FROM chamados c
        JOIN usuarios u
            ON c.id_usuario = u.id
        WHERE c.id = %s;
        """, (id_chamado,))

    chamados = cursor.fetchone()
    if not chamados:
        print("[red]Nenhum chamado encontrado.[/]")
        return
    
    tabela_chamados = Table(title="Lista de Chamados (detalhados)")
    tabela_chamados.add_column("ID", justify="left")
    tabela_chamados.add_column("Nome", justify="left")
    tabela_chamados.add_column("Matricula", justify="left")
    tabela_chamados.add_column("Título", justify="left")
    tabela_chamados.add_column("Descrição", justify="left")
    tabela_chamados.add_column("Categoria", justify="left")
    tabela_chamados.add_column("Prioridade", justify="left")
    tabela_chamados.add_column("Status", justify="left")
    tabela_chamados.add_column("Data Abertura", justify="left")
    tabela_chamados.add_column("Data Fechamento", justify="left")
    
    tabela_chamados.add_row(
        str(chamados[0]),
        str(chamados[1]),
        str(chamados[2]),
        str(chamados[3]),
        str(chamados[4]),
        str(chamados[5]),
        str(chamados[6]),
        str(chamados[7]),
        str(chamados[8]),
        str(chamados[9])
    )

    print(tabela_chamados)
    

def iniciar_atendimento():
    listar_chamados_abertos()

    while True:
        try:
            id_chamado = int(input("\nDigite o ID do chamado que deseja atender: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")

    cursor.execute("""
        SELECT status
        FROM chamados
        WHERE id = %s
    """, (id_chamado,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("[red]Chamado não encontrado.[/]")
        return

    if resultado[0] == "Em andamento":
        print("[yellow]Esse chamado já está em atendimento.[/]")
        return

    if resultado[0] == "Fechado":
        print("[yellow]Esse chamado já foi fechado.[/]")
        return

    cursor.execute("""
        UPDATE chamados
        SET status = 'Em andamento'
        WHERE id = %s
    """, (id_chamado,))

    db.commit()

    print("\n[green]Chamado colocado em atendimento![/]")