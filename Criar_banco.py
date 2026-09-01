import sqlite3

# Conectando (ou criando) o arquivo do banco de dados local
conexao = sqlite3.connect("tig_dados.db")
cursor = conexao.cursor()

# Criando a tabela de transações fictícias para simulação educacional
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT,
    descricao TEXT,
    valor REAL,
    tipo TEXT
)
""")

# Inserindo alguns dados de exemplo para o Tig poder analisar depois
dados_iniciais = [
    ("Alimentação", "Supermercado Mensal", 450.00, "Despesa"),
    ("Lazer", "Cinema e Jantar", 120.00, "Despesa"),
    ("Salário", "Empresa X", 3500.00, "Receita"),
    ("Moradia", "Aluguel", 1200.00, "Despesa")
]

cursor.executemany("""
INSERT INTO transacoes (categoria, descricao, valor, tipo)
VALUES (?, ?, ?, ?)
""", dados_iniciais)

conexao.commit()
conexao.close()

print("Banco de dados SQLite do Tig criado e populado com sucesso!")