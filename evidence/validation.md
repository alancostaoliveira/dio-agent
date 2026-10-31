# Evidências da demonstração

## Escopo

O laboratório usa SQLite em memória e dados sintéticos. Ele compara
[`app-vulnerable.py`](app-vulnerable.py), que concatena valores na consulta, com
[`app-fixed.py`](app-fixed.py), que usa parâmetros e hash de senha.

## Resultados observados

Execute na raiz do repositório:

```powershell
python -m unittest discover -s evidence -p "test_*.py" -v
```

O conjunto deve terminar com `OK` e quatro testes aprovados:

- a versão vulnerável lança `sqlite3.OperationalError` quando um nome legítimo contém apóstrofo;
- a versão corrigida trata o mesmo nome como dado;
- a versão corrigida autentica uma credencial válida;
- uma entrada de login com sintaxe SQL não altera a consulta parametrizada.

Esses resultados devem ser atualizados somente após a execução local do comando.

## Resultados esperados

A consulta parametrizada mantém a gramática SQL separada dos valores recebidos.
Por isso, apóstrofos e textos que parecem SQL não mudam a estrutura da consulta.
O hash com salt também evita comparar senhas em texto puro no exemplo corrigido.

## Testes não executados

Esta demonstração não cobre:

- testes de carga ou exaustão de recursos;
- análise dinâmica de uma aplicação HTTP;
- configuração de WAF, firewall ou Security Group;
- auditoria de dependências e pipeline CI/CD;
- validação de produção.

## Classificação didática

O padrão vulnerável corresponde a **CWE-89 (SQL Injection)** e a **OWASP
Injection**. O mapeamento MITRE ATT&CK **T1190** só deve ser usado se o
componente estiver efetivamente exposto a uma aplicação pública. Neste
laboratório local, a presença da fraqueza técnica não implica automaticamente
risco crítico.
