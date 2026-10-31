import sqlite3


def fazer_login(conexao, usuario, senha):
    query = (
        "SELECT usuario FROM usuarios "
        f"WHERE usuario = '{usuario}' AND senha = '{senha}'"
    )
    return conexao.execute(query).fetchone() is not None
