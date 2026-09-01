from google import genai

# Sua chave de API
CHAVE_API = "AQ.Ab8RN6I1Xuz7ddnwZ8ILCaaxgHT89gUjA6UqlimqKootUhh_Uw"
cliente = genai.Client(api_key=CHAVE_API)

print("Buscando modelos disponíveis para a sua chave...")
print("-" * 40)

# Lista e imprime o nome de todos os modelos liberados
try:
    for modelo in cliente.models.list():
        print(modelo.name)
    print("-" * 40)
    print("Busca concluída!")
except Exception as e:
    print(f"Erro ao buscar modelos: {e}")