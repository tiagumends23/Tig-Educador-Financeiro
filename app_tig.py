import streamlit as st
import sqlite3
import time
import pandas as pd
from google import genai
from google.genai import types

# 1. Configuração da API e Persona
CHAVE_API = st.secrets["GOOGLE_API_KEY"]

cliente = genai.Client(api_key=CHAVE_API)

instrucoes_sistema = """
Você é o Tig, um Educador Financeiro Virtual. Sua missão é ajudar pessoas iniciantes a entenderem conceitos básicos de finanças, organização orçamentária e segurança digital de forma clara e objetiva.
Você é amigável, acolhedor e muito didático, mas mantém uma postura madura e profissional.
Regras Inegociáveis (Guardrails):
1. Zero Recomendações: Você atua estritamente como educador. Nunca dê dicas sobre onde investir ou qual ação comprar.
2. Privacidade e Contexto Educacional: Nunca solicite dados sensíveis reais do usuário. No entanto, você pode analisar e usar os dados de transações simuladas e conceitos teóricos fornecidos no contexto técnico da aplicação para fins estritamente educacionais e de organização orçamentária.
3. Foco: Recuse perguntas fora do escopo financeiro, econômico ou de segurança digital.
"""

# Inicializar o banco de dados (transações e histórico de chat)
def inicializar_banco():
    conexao = sqlite3.connect("tig_dados.db")
    cursor = conexao.cursor()
    # Tabela de transações financeiras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT,
        descricao TEXT,
        valor REAL,
        tipo TEXT
    )
    """)
    # Tabela para persistir o histórico de conversas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        papel TEXT,
        conteudo TEXT
    )
    """)
    conexao.commit()
    conexao.close()

inicializar_banco()

# Função para carregar o histórico salvo do SQLite
def carregar_historico_db():
    try:
        conexao = sqlite3.connect("tig_dados.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT papel, conteudo FROM historico_chat")
        dados = cursor.fetchall()
        conexao.close()
        
        if not dados:
            return [{
                "role": "assistant", 
                "content": "Olá! Sou o Tig, seu educador financeiro amigável e maduro. O que você gostaria de aprender hoje?"
            }]
        
        return [{"role": papel, "content": conteudo} for papel, conteudo in dados]
    except Exception:
        return []

# Função para salvar uma mensagem no SQLite
def salvar_mensagem_db(papel, conteudo):
    try:
        conexao = sqlite3.connect("tig_dados.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO historico_chat (papel, conteudo) VALUES (?, ?)", (papel, conteudo))
        conexao.commit()
        conexao.close()
    except Exception:
        pass

# Função para limpar o histórico no banco
def limpar_historico_db():
    try:
        conexao = sqlite3.connect("tig_dados.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM historico_chat")
        conexao.commit()
        conexao.close()
    except Exception:
        pass

# Salvando o CLIENTE na sessão
if "cliente_tig" not in st.session_state:
    st.session_state.cliente_tig = genai.Client(api_key=CHAVE_API)

# FUNÇÃO DE ESCRITA: Inserir nova transação no SQLite
def registrar_transacao(categoria: str, descricao: str, valor: float, tipo: str):
    """Registra uma nova transação financeira no banco de dados SQLite."""
    try:
        conexao = sqlite3.connect("tig_dados.db")
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO transacoes (categoria, descricao, valor, tipo)
            VALUES (?, ?, ?, ?)
        """, (categoria, descricao, valor, tipo))
        conexao.commit()
        conexao.close()
        return f"Sucesso! A transação de {tipo} ({descricao} - {categoria}) no valor de R$ {valor:.2f} foi cadastrada com sucesso."
    except Exception as e:
        return f"Erro ao registrar no banco de dados: {e}"

# Inicializando o chat amarrado ao cliente salvo e permitindo o uso da ferramenta
if "chat_tig" not in st.session_state:
    st.session_state.chat_tig = st.session_state.cliente_tig.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=instrucoes_sistema,
            tools=[registrar_transacao],
        )
    )

# Função para buscar dados do SQLite
def buscar_dados_financeiros():
    try:
        conexao = sqlite3.connect("tig_dados.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT categoria, descricao, valor, tipo FROM transacoes")
        transacoes = cursor.fetchall()
        conexao.close()
        
        if not transacoes:
            return ""
            
        resumo = "\n[Contexto de Dados do Usuário no Banco SQLite]:\n"
        for cat, desc, val, tipo in transacoes:
            resumo += f"- {tipo}: {desc} ({cat}) no valor de R$ {val:.2f}\n"
        return resumo
    except Exception:
        return ""

# Função para ler o Dicionário Financeiro em Markdown
def buscar_dicionario_financeiro(pergunta_usuario):
    try:
        with open("dicionario_financeiro.md", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        return f"\n[Contexto Teórico do Dicionário Financeiro do Tig]:\n{conteudo}\n"
    except Exception:
        return ""

# 2. Configuração da página visual e Barra Lateral
st.set_page_config(page_title="Tig - Educador Financeiro", page_icon="🐯", layout="centered")

with st.sidebar:
    st.markdown("# 🐯")
    st.subheader("Painel do Tig")
    st.markdown("Seu assistente virtual para educação financeira e organização de rotina.")
    
    st.divider()
    
    # --- GRÁFICO DE GASTOS NA SIDEBAR ---
    st.markdown("### 📊 Resumo de Gastos")
    try:
        conexao = sqlite3.connect("tig_dados.db")
        df_transacoes = pd.read_sql_query("SELECT categoria, valor, tipo FROM transacoes", conexao)
        conexao.close()
        
        if not df_transacoes.empty:
            # Padroniza a coluna tipo para minúsculas e remove espaços em branco
            df_transacoes['tipo_limpo'] = df_transacoes['tipo'].astype(str).str.strip().str.lower()
            
            # Filtra por termos comuns de saída financeira
            df_despesas = df_transacoes[df_transacoes['tipo_limpo'].isin(['despesa', 'gasto', 'saida', 'saída'])]
            
            # Caso não haja marcação explícita de despesa, agrupa todas as categorias registradas
            if df_despesas.empty:
                df_despesas = df_transacoes
                
            df_grouped = df_despesas.groupby('categoria')['valor'].sum()
            st.bar_chart(df_grouped)
        else:
            st.info("Nenhuma despesa cadastrada ainda.")
    except Exception:
        st.caption("Gráfico indisponível no momento.")

    st.divider()
    
    st.markdown("### 💡 Dicas de Comandos:")
    st.markdown("- *\"Quanto eu gastei com lazer?\"*")
    st.markdown("- *\"Anota aí que gastei 50 com mercado\"*")
    st.markdown("- *\"O que é Reserva de Emergência?\"*")
    
    st.divider()
    
    if st.button("🗑️ Limpar Conversa"):
        limpar_historico_db()
        st.session_state.mensagens = [{
            "role": "assistant", 
            "content": "Conversa reiniciada e histórico limpo! Como posso te ajudar hoje?"
        }]
        st.rerun()
        
    st.caption("Status: SQLite Conectado 🟢")
    st.caption("Versão: 1.3.0 (Persistência + Gráficos)")

# Título principal da tela
st.title("🐯 Olá! Eu sou o Tig.")
st.markdown("Seu educador financeiro pessoal. Como posso te ajudar a organizar suas finanças hoje?")

# Inicialização da memória visual utilizando o banco SQLite persistente
if "mensagens" not in st.session_state:
    st.session_state.mensagens = carregar_historico_db()

# Exibição do histórico de mensagens
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Interação com o usuário e laços de tentativa
if prompt := st.chat_input("Digite sua dúvida financeira aqui..."):
    # Exibe e salva a pergunta do usuário
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    salvar_mensagem_db("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chama o Gemini e exibe a resposta
    with st.chat_message("assistant"):
        resposta_placeholder = st.empty()
        resposta_placeholder.markdown("Pensando... 🤔")
        
        dados_sqlite = buscar_dados_financeiros()
        dados_dicionario = buscar_dicionario_financeiro(prompt)
        
        prompt_enriquecido = f"""
        {dados_sqlite}
        {dados_dicionario}
        
        Instrução interna para esta mensagem: Utilize obrigatoriamente os dados simulados e o contexto teórico fornecidos acima. Se o usuário pedir para registrar ou anotar um gasto/receita, utilize a ferramenta 'registrar_transacao' disponível para você.
        
        Dúvida do usuário: {prompt}
        """
        
        tentativas = 3
        texto_resposta = ""
        
        for tentativa in range(tentativas):
            try:
                resposta = st.session_state.chat_tig.send_message(prompt_enriquecido)
                texto_resposta = resposta.text
                break
            except Exception as e:
                if tentativa < tentativas - 1:
                    resposta_placeholder.markdown(f"Servidor sobrecarregado (Tentativa {tentativa + 1}/{tentativas}), aguardando para reenviar...")
                    time.sleep(3)
                else:
                    texto_resposta = f"**Ops, o servidor do Google continua instável (Erro 503):** {e}"

        # Atualiza a tela e salva a resposta da IA no SQLite
        resposta_placeholder.markdown(texto_resposta)
        st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
        salvar_mensagem_db("assistant", texto_resposta)
        
        # Recarrega a página para atualizar o gráfico automaticamente caso o usuário tenha cadastrado um gasto novo!
        if "sucesso" in texto_resposta.lower() or "anotei" in texto_resposta.lower():
            st.rerun()