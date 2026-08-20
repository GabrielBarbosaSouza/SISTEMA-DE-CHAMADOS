from rich import print
from rich.table import Table
from banco.conexao import cursor

def dashboard():
    cursor.execute("SELECT COUNT(id) FROM usuarios;")
    tot_usuarios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(id) FROM chamados;")
    tot_chamados = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(id)
        FROM chamados
        WHERE status IN ('Aberto', 'Em andamento');
    """)
    chamados_abertos = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(id)
        FROM chamados
        WHERE status = 'Fechado';
    """)
    chamados_fechados = cursor.fetchone()[0]

    
    tabela = Table(title="Dashboard", title_justify="center")
    tabela.add_column("Total de usuários", justify="right")
    tabela.add_column("Total de chamados", justify="right")
    tabela.add_column("Chamados abertos", justify="right")
    tabela.add_column("Chamados fechados", justify="right")
    
    
    tabela.add_row(
            str(tot_usuarios),
            str(tot_chamados),
            str(chamados_abertos),
            str(chamados_fechados)
        )
    
    print(tabela)