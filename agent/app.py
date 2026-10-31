import sqlite3

def fazer_login(usuario, senha):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    # Usa query parametrizada para prevenir SQL Injection
    query = "SELECT * FROM usuarios WHERE usuario = ? AND password = ?"
    cursor.execute(query, (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return "Acesso concedido"
    else:
        return "Acesso negado"