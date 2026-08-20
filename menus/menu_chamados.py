from InquirerPy import inquirer
from funcoes.chamados import listar_chamados_abertos, fechar_chamado, listar_chamados_fechados, reabrir_chamado, iniciar_atendimento, listar_chamados


def menu_chamados():
    while True:
        opcao = inquirer.select(
            message="Gerenciamento de chamados:",
            choices=[
                "Chamados abertos",
                "Chamados fechados",
                "Colocar chamado em atendimento",
                "Todos os chamados",
                "Voltar"
            ]
        ).execute()

        match opcao:

            case "Chamados abertos":
                listar_chamados_abertos()

                fechar = inquirer.confirm(message="Deseja fechar algum chamado?").execute()

                if fechar:
                    fechar_chamado()

            case "Chamados fechados":
                listar_chamados_fechados()

                reabrir = inquirer.confirm(message="Deseja reabrir algum chamado?").execute()

                if reabrir:
                    reabrir_chamado()

            case "Colocar chamado em atendimento":
                iniciar_atendimento()

            case "Todos os chamados":
                listar_chamados()

            case "Voltar":
                break
