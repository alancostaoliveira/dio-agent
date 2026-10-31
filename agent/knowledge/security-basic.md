# Fundamentos de Cibersegurança e Segurança Ofensiva vs. Defensiva

Este documento estabelece a base teórica e os padrões de segurança que o **DIO Agent** utiliza para orientar estudantes e desenvolvedores em segurança de aplicações (AppSec), arquitetura defensiva e DevSecOps.

---

## 1. Conceitos Fundamentais: Vulnerabilidade, Ameaça e Risco

Em segurança da informação, esses três termos são distintos e frequentemente confundidos:

- **Vulnerabilidade (Fraqueza):** Uma falha no design, na implementação ou na configuração de um software, hardware ou processo que pode ser explorada. Exemplo: Concatenação direta de strings em comandos SQL (CWE-89).
- **Ameaça (Agente/Vetor):** Qualquer evento ou agente (humano ou automatizado) com potencial de explorar uma vulnerabilidade e causar dano. Exemplo: Um atacante externo ou botnet escaneando parâmetros HTTP para roubo de dados.
- **Risco (Probabilidade $\times$ Impacto):** A probabilidade de uma ameaça concretizar a exploração de uma vulnerabilidade combinada com a magnitude do impacto no negócio caso o ataque ocorra.
  $$\text{Risco} = f(\text{Probabilidade}, \text{Impacto})$$

- **Vulnerabilidade Técnica vs. Severidade de Risco no Ambiente:**
  A presença de uma fraqueza no código (como uma falha CWE) é uma característica técnica intrínseca. No entanto, a severidade do risco real no ambiente depende diretamente de fatores operacionais: se o componente está exposto à internet pública ou restrito a localhost/intranet, se exige autenticação prévia de administrador e se manipula dados confidenciais ou apenas dados sintéticos de laboratório.

> **Regra do Agente:** Nunca classifique uma vulnerabilidade isolada automaticamente como "Crítica" ou "Alta" sem antes avaliar o contexto do ambiente (exposição de rede, controles perimetrais, autenticação necessária, privilégios exigidos e dados em jogo). Uma falha grave em um serviço isolado em localhost com dados fictícios não tem o mesmo risco de negócio que a mesma falha em uma API pública de pagamentos em produção.

---

## 2. A Tríade CIA (Confidencialidade, Integridade e Disponibilidade)

A avaliação de qualquer impacto de segurança deve mapear os pilares da Tríade CIA:

1. **Confidencialidade (C):** Garantir que a informação seja acessível apenas por entidades autorizadas. Violações típicas: vazamento de credenciais, leitura indevida de dados pessoais (LGPD/GDPR) via SQL Injection ou IDOR.
2. **Integridade (I):** Garantir a precisão, exatidão e proteção contra modificação não autorizada de dados ou sistemas. Violações típicas: alteração de saldo financeiro, manipulação de logs, corrupção de tabelas.
3. **Disponibilidade (A):** Garantir que dados e serviços estejam acessíveis e operacionais quando requeridos por usuários legítimos. Violações típicas: Negação de Serviço (DoS), travamento de instâncias de banco por queries maliciosas pesadas, ransomware.

---

## 3. Padrões e Frameworks de Segurança da Indústria

### 3.1. OWASP Top 10 (Aplicações Web)

O projeto mantido pela Open Web Application Security Project lista as 10 categorias de riscos mais críticos para sistemas web.

- **Evolução do Mapeamento de Injeção:**
  - **A05:2025 – Injection:** Classificação no ciclo OWASP Top 10 2025.
  - **A03:2021 – Injection:** Classificação de referência histórica consolidada (OWASP Top 10 2021).
    _(Ao documentar, cite preferencialmente `A05:2025 – Injection`, mantendo `A03:2021` como referência histórica comparativa)._

- **Outras categorias essenciais:**
  - **A01:2021 / A01:2025 - Quebra de Controle de Acesso (Broken Access Control):** Falhas em impor permissões adequadas (IDOR, elevação de privilégio).
  - **A02:2021 / A04:2025 - Falhas Criptográficas (Cryptographic Failures):** Uso de algoritmos obsoletos, transmissão sem TLS, senhas em texto puro ou sem salt.
  - **A04:2021 / A06:2025 - Design Inseguro (Insecure Design):** Ausência de modelagem de ameaças e padrões arquiteturais seguros desde a concepção.
  - **A05:2021 / A02:2025 - Configuração Insegura (Security Misconfiguration):** Portas abertas desnecessárias, credenciais padrão, mensagens com stack trace exposto.
  - **A06:2021 / A03:2025 - Componentes Vulneráveis e Desatualizados:** Dependências antigas com CVEs conhecidas.
  - **A07:2021 / A07:2025 - Falhas de Identificação e Autenticação:** Falta de MFA, ausência de rate limiting em login, gerenciamento frouxo de sessão.

### 3.2. CWE (Common Weakness Enumeration)

Dicionário formal mantido pela MITRE que categoriza fraquezas em código fonte e arquitetura.

- **Exemplos essenciais:**
  - `CWE-89`: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection').
  - `CWE-79`: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting').
  - `CWE-20`: Improper Input Validation.
  - `CWE-306`: Missing Authentication for Critical Function.
  - `CWE-798`: Use of Hard-coded Credentials.

### 3.3. MITRE ATT&CK®

Base de conhecimento global de táticas, técnicas e procedimentos (TTPs) de adversários.

- **Critérios Rigorosos de Associação:**
  - **T1190 – Exploit Public-Facing Application:** Aplica-se **exclusivamente** quando o componente vulnerável estiver exposto diretamente à internet pública ou em perímetro de rede externo acessível ao atacante. Não se aplica a scripts locais offline ou serviços isolados em loopback sem exposição externa.
  - **T1078 – Valid Accounts:** Aplica-se **somente** quando o atacante obtém e utiliza credenciais legítimas (usuário/senha, tokens válidos) para acessar sistemas.

    > **Atenção:** Um _bypass_ de autenticação por SQL Injection (como `admin' --`) **não** é automaticamente T1078, pois o atacante está subvertendo a lógica da consulta e não usando credenciais válidas. A técnica T1078 só se aplica se o atacante extrair credenciais/hashes do banco de dados e, em um segundo momento, utilizá-las para autenticar como um usuário legítimo.

---

## 4. CVSS (Common Vulnerability Scoring System)

O CVSS v3.1 quantifica a severidade técnica de uma vulnerabilidade por meio de métricas vetoriais:

- **Vetor Base:** Vetor de Ataque (AV), Complexidade (AC), Privilégios (PR), Interação do Usuário (UI), Escopo (S), Confidencialidade (C), Integridade (I), Disponibilidade (A).

### Faixas de Severidade CVSS:

| Faixa de Score | Classificação      |
| :------------- | :----------------- |
| **0.0**        | Informativa (None) |
| **0.1 – 3.9**  | Baixa (Low)        |
| **4.0 – 6.9**  | Média (Medium)     |
| **7.0 – 8.9**  | Alta (High)        |
| **9.0 – 10.0** | Crítica (Critical) |

> **Diretriz de Transparência Técnica e Estimativas CVSS:**
>
> 1. Qualquer pontuação elevada (como CVSS 9.1: `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`) deve ser apresentada expressamente como uma **avaliação hipotética baseada no pior cenário (worst-case)** quando não houver evidências completas de produção.
>
>    As premissas dessa hipótese devem ser declaradas:
>    - _Premissa 1:_ O endpoint está exposto diretamente na internet pública sem WAF ou rate limiting.
>    - _Premissa 2:_ A exploração não requer privilégios prévios.
>    - _Premissa 3:_ O banco de dados armazena dados de produção altamente sensíveis.
>
>    Se essas premissas não se confirmarem (por exemplo, em um laboratório local isolado ou intranet restrita com dados de teste), o impacto de negócio e o risco real serão substancialmente inferiores.
>
> 2. **Proibição de CVSS 0.0 Automático Pós-Remediação:** O CVSS avalia a severidade intrínseca de uma vulnerabilidade. Após aplicar uma mitigação (ex: Prepared Statements em uma consulta específica), a fraqueza pontual foi remediada, mas **nunca atribua automaticamente "CVSS 0.0"** ao sistema ou aplicação inteira. Em vez disso, avalie o **risco residual** de forma fundamentada e qualitativa (ex.: risco residual Baixo no escopo do componente auditado), declarando expressamente quando qualquer métrica for uma estimativa hipotética.

---

## 5. Boas Práticas e Princípios Defensivos

1. **Secure by Design (Segurança por Concepção):** Segurança tratada como requisito arquitetural desde o início, e não como correção posterior.
2. **Defesa em Profundidade (Defense in Depth):** Múltiplas camadas independentes de proteção (validação de entrada + parametrização + WAF + firewall + menor privilégio).
3. **Princípio do Menor Privilégio (Least Privilege):** Cada serviço deve ter exclusivamente as permissões estritamente necessárias no banco de dados.
4. **Parametrização estrita (Prepared Statements):** A única solução estrutural definitiva contra SQL Injection. Os dados são mantidos rigorosamente separados da gramática da consulta SQL.
5. **Validação de Entrada por Allowlist:** Aceitar apenas formatos, tipos e tamanhos esperados.
6. **Gerenciamento Seguro de Configurações:** Armazenar segredos e senhas em variáveis de ambiente ou cofres seguros, nunca no código.
7. **Precisão Conceitual: `SyntaxError` de Python vs. `sqlite3.OperationalError` de Banco:**
   - A interpolação dinâmica de strings como `f"INSERT INTO users VALUES ('{username}')"` onde `username = "d'angelo"` gera a string perfeitamente válida para a linguagem Python. O interpretador Python executa a f-string sem nenhum `SyntaxError`.
   - O erro ocorre exclusivamente dentro do motor de banco de dados (SQLite) durante a análise sintática do comando SQL (`near "angelo": syntax error`). O conector do Python captura essa falha do banco e a propaga como uma exceção `sqlite3.OperationalError`.
   - _Regra:_ Nunca confunda erros de sintaxe de código-fonte da aplicação (`SyntaxError`) com erros de sintaxe SQL lançados pelo driver de banco de dados (`sqlite3.OperationalError`).
8. **Paginação Segura e Proteção contra DoS / Exaustão de Recursos (CWE-400):**
   - Em consultas de listagem e busca (ex.: `SELECT * FROM products`), nunca deixe o retorno de registros irrestrito nem confie em parâmetros não validados de paginação.
   - _Validação defensiva:_
     - Validar que `page` e `limit` sejam inteiros positivos estritos (`page >= 1`, `limit >= 1`).
     - Aplicar um teto máximo rígido para `limit` (ex.: `max_limit = 50` ou `100`), impedindo que requisições com `limit=1000000` saturem a memória ou o banco.
     - Rejeitar ou normalizar valores negativos ou zero para padrões seguros (_fail-safe defaults_).
     - Calcular o deslocamento de forma segura: `offset = (page - 1) * limit`.
9. **Hardening de Infraestrutura e Superfície de Rede:**
   - Em cenários de servidores, conduza uma mentoria gradual: questione primeiro sobre métodos de autenticação (chaves SSH vs senhas), serviços pretendidos e firewalls antes de apresentar qualquer comando de diagnóstico.
   - Respeite sempre a regra de uma pergunta por vez.
   - Esclareça que portas em estado `LISTEN` no sistema operacional (mesmo vinculadas a `0.0.0.0` no `ss -tulpn`) **não significam necessariamente portas acessíveis publicamente pela internet**, uma vez que firewalls externos de borda, grupos de segurança na nuvem (Security Groups da AWS, Azure, GCP, Oracle Cloud), VPCs e NATs atuam como filtros perimetrais antes que os pacotes alcancem a máquina.
