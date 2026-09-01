import csv
import json
import sqlite3
import random
from datetime import datetime, timedelta

def gerar_base_conhecimento():
    """Gera os arquivos iniciais para a base de conhecimento do Tig."""
    
    print("Iniciando a geração da base de conhecimento do Tig...")

    # 1. Textos Explicativos (.md)
    criar_dicionario_financeiro()
    criar_cartilha_seguranca()

    # 2. Dados Estruturados (CSV, JSON, SQLite)
    gerar_dados_transacoes_csv()
    gerar_perfil_usuario_json()
    inicializar_banco_sqlite()

    print("\nBase de conhecimento gerada com sucesso!")


def criar_dicionario_financeiro():
    """Cria um arquivo Markdown com conceitos básicos."""
    conteudo = """# Dicionário Financeiro do Tig

## Selic
A Taxa Selic é a taxa básica de juros da economia brasileira. Ela influencia todas as outras taxas de juros, como as de empréstimos, financiamentos e aplicações financeiras.

## CDI (Certificado de Depósito Interbancário)
É uma taxa que os bancos cobram para emprestar dinheiro uns aos outros de um dia para o outro. É muito usada como referência para a rentabilidade de investimentos de renda fixa.

## Reserva de Emergência
Um valor guardado para cobrir imprevistos (como desemprego ou problemas de saúde). O ideal é que cubra de 3 a 6 meses do seu custo de vida básico.

## Juros Compostos
São os "juros sobre juros". O rendimento de cada período é somado ao valor principal para o cálculo dos juros do período seguinte, acelerando o crescimento do dinheiro no longo prazo.
"""
    with open('dicionario_financeiro.md', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("- dicionario_financeiro.md criado.")


def criar_cartilha_seguranca():
    """Cria um arquivo Markdown sobre segurança e golpes."""
    conteudo = """# Cartilha de Segurança Digital

## Phishing
É um golpe onde criminosos se passam por instituições confiáveis (por e-mail ou mensagem) para roubar suas senhas ou dados do cartão. 
*Regra de Ouro:* Nunca clique em links suspeitos e lembre-se: seu banco não pede sua senha por SMS.

## Fraudes de WhatsApp
Alguém se passando por um familiar ou amigo pede dinheiro emprestado com urgência.
*Regra de Ouro:* Ligue para a pessoa para confirmar a história antes de fazer qualquer transferência.
"""
    with open('cartilha_seguranca.md', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("- cartilha_seguranca.md criado.")


def gerar_dados_transacoes_csv():
    """Gera um arquivo CSV com um histórico de transações fictício."""
    categorias_despesa = ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Saúde']
    
    with open('transacoes_usuario.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Data', 'Categoria', 'Tipo', 'Valor'])
        
        # Gerando dados para os últimos 30 dias
        data_atual = datetime.now()
        for i in range(30):
            data_transacao = (data_atual - timedelta(days=i)).strftime('%Y-%m-%d')
            
            # 1 a 3 compras por dia
            num_compras = random.randint(1, 3)
            for _ in range(num_compras):
                categoria = random.choice(categorias_despesa)
                valor = round(random.uniform(15.50, 250.00), 2)
                writer.writerow([data_transacao, categoria, 'Despesa', valor])
            
            # Adicionando um salário no dia 5 (aproximadamente)
            if i == 25:
                 writer.writerow([data_transacao, 'Salário', 'Receita', 3500.00])
                 
    print("- transacoes_usuario.csv criado com dados aleatórios.")


def gerar_perfil_usuario_json():
    """Gera um arquivo JSON com informações do perfil de investimento."""
    perfil = {
        "nome": "Usuário Teste",
        "objetivo_principal": "Montar Reserva de Emergência",
        "meta_valor": 10000.00,
        "valor_atual_guardado": 2500.00,
        "aporte_mensal_planejado": 300.00,
        "perfil_risco": "Conservador"
    }
    with open('perfil_simulacao.json', 'w', encoding='utf-8') as f:
        json.dump(perfil, f, indent=4, ensure_ascii=False)
    print("- perfil_simulacao.json criado.")


def inicializar_banco_sqlite():
    """Cria um banco SQLite e uma tabela de controle de orçamentos."""
    # Usando SQLite para reforçar o foco em modelagem de dados
    conn = sqlite3.connect('tig_dados.db')
    cursor = conn.cursor()
    
    # Criando tabela de orçamentos mensais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orcamento_mensal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes_ano TEXT NOT NULL,
            categoria TEXT NOT NULL,
            limite_gasto REAL NOT NULL
        )
    ''')
    
    # Limpando dados antigos se houver
    cursor.execute('DELETE FROM orcamento_mensal')
    
    # Inserindo dados iniciais
    orcamentos = [
        ('2026-09', 'Alimentação', 800.00),
        ('2026-09', 'Transporte', 300.00),
        ('2026-09', 'Lazer', 200.00)
    ]
    cursor.executemany('INSERT INTO orcamento_mensal (mes_ano, categoria, limite_gasto) VALUES (?, ?, ?)', orcamentos)
    
    conn.commit()
    conn.close()
    print("- tig_dados.db criado e tabela orcamento_mensal inicializada.")


# Executa a função principal
if __name__ == "__main__":
    gerar_base_conhecimento()
