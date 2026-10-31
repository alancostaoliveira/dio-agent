import hashlib
import sqlite3


def gerar_hash_senha(senha, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, 120_000
    ).hex()


def fazer_login(conexao, usuario, senha, salt):
    query = "SELECT senha_hash FROM usuarios WHERE usuario = ?"
    resultado = conexao.execute(query, (usuario,)).fetchone()
    if resultado is None:
        return False
    return resultado[0] == gerar_hash_senha(senha, salt)
