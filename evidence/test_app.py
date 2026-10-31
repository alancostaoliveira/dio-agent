import importlib.util
import sqlite3
import unittest
from pathlib import Path


EVIDENCE_DIR = Path(__file__).parent


def carregar(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, EVIDENCE_DIR / arquivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


vulnerable = carregar("app_vulnerable", "app-vulnerable.py")
fixed = carregar("app_fixed", "app-fixed.py")


class LoginSecurityTests(unittest.TestCase):
    def setUp(self):
        self.conexao = sqlite3.connect(":memory:")
        self.conexao.execute(
            "CREATE TABLE usuarios (usuario TEXT, senha TEXT, senha_hash TEXT)"
        )
        self.salt = b"laboratorio-dio"
        self.conexao.execute(
            "INSERT INTO usuarios (usuario, senha, senha_hash) VALUES (?, ?, ?)",
            (
                "alice",
                "nao-usado-pelo-codigo-corrigido",
                fixed.gerar_hash_senha("segredo", self.salt),
            ),
        )
        self.conexao.commit()

    def tearDown(self):
        self.conexao.close()

    def test_codigo_vulneravel_quebra_com_apostrofo(self):
        with self.assertRaises(sqlite3.OperationalError):
            vulnerable.fazer_login(self.conexao, "D'Angelo", "qualquer")

    def test_codigo_corrigido_aceita_apostrofo_como_dado(self):
        self.assertFalse(
            fixed.fazer_login(self.conexao, "D'Angelo", "qualquer", self.salt)
        )

    def test_codigo_corrigido_autentica_usuario_legitimo(self):
        self.assertTrue(
            fixed.fazer_login(self.conexao, "alice", "segredo", self.salt)
        )

    def test_codigo_corrigido_rejeita_entrada_de_login_invalida(self):
        self.assertFalse(
            fixed.fazer_login(
                self.conexao,
                "alice' OR '1'='1",
                "qualquer",
                self.salt,
            )
        )


if __name__ == "__main__":
    unittest.main()
