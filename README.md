# 🐯 Tig - Assistente Virtual & Educador Financeiro

O **Tig** é um assistente virtual inteligente e educador financeiro desenvolvido em **Python** utilizando **Streamlit** e a API oficial do **Google GenAI**. O aplicativo foi projetado para auxiliar no controle de despesas diárias, fornecendo orientações financeiras personalizadas, resumos categorizados e gráficos dinâmicos em tempo real integrados com um banco de dados SQLite.

---

## 🚀 Funcionalidades

- **Chat Inteligente**: Interação em linguagem natural com o modelo do Google Gemini para tirar dúvidas financeiras e planejar orçamentos.
- **Gerenciamento de Gastos via IA**: Capacidade de registrar transações e despesas conversando diretamente com o assistente.
- **Gráficos e Métricas Dinâmicas**: Acompanhamento visual dos gastos por categorias diretamente na barra lateral.
- **Armazenamento Local Seguro**: Dados persistidos localmente utilizando SQLite (`tig_dados.db`).
- **Segurança de Credenciais**: Isolamento completo da chave de API utilizando o sistema nativo de segredos do Streamlit (`st.secrets`).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** (Interface Web e gerenciamento de segredos)
- **Google GenAI SDK** (`google-genai`)
- **SQLite3** (Banco de dados)
- **Pandas / Matplotlib** (Processamento de dados e visualização)

---

## ⚙️ Como Configurar e Executar o Projeto

Siga os passos abaixo para clonar e rodar o projeto localmente na sua máquina:

### 1. Clonar o Repositório
`git clone https://github.com/tiagumends23/tig-educador-financeiro.git`
`cd Tig_Assitente_Virtual`

### 2. Instalar as Dependências
Certifique-se de ter o Python instalado e execute:
`pip install -r requirements.txt`
*(Nota: caso não possua um arquivo requirements.txt, instale as principais bibliotecas manualmente: `pip install streamlit google-genai pandas`)*

### 3. Configurar a Chave de API (Segurança)
Para que o assistente se comunique com a API do Google GenAI, você precisa configurar sua chave de acesso de forma segura:

- Na raiz do projeto, crie uma pasta chamada `.streamlit` (caso ela não exista).
- Dentro da pasta `.streamlit`, crie um arquivo chamado `secrets.toml`.
- Adicione a sua chave de API no arquivo `secrets.toml` com a seguinte estrutura:

`GOOGLE_API_KEY = "sua_chave_de_api_aqui"`

> ⚠️ **Importante:** O arquivo `secrets.toml` está listado no `.gitignore` para garantir que suas credenciais **nunca** sejam enviadas publicamente para o GitHub.

### 4. Executar a Aplicação
Com o ambiente configurado, inicie o aplicativo Streamlit:
`streamlit run app_tig.py`

O navegador abrirá automaticamente na porta `http://localhost:8501` com o seu assistente pronto para uso!

---

## 📂 Estrutura do Projeto

- `app_tig.py`: Aplicação principal em Streamlit com a interface e lógica do agente.
- `Criar_banco.py`: Script responsável pela inicialização do banco de dados SQLite.
- `tig_dados.db`: Banco de dados local (armazenado de forma isolada).
- `.streamlit/secrets.toml`: Arquivo local de configuração de segredos (não versionado).
- `.gitignore`: Configuração para ignorar arquivos sensíveis e caches.

---

## 👤 Autor
Desenvolvido por **Tiago Mendes** como parte de projetos práticos de desenvolvimento de software e inteligência artificial do Bootcamp Bradesco na DIO.
