import requests

CITIES_URL = "https://api.ipma.pt/open-data/distrits-islands.json"

def listar_cidades():
    try:
        response = requests.get(CITIES_URL, timeout=10)
        response.raise_for_status()
        cidades = response.json().get("data", [])
        return cidades
    except requests.RequestException as e:
        print(f"Erro ao listar cidades: {e}")
        return []

def get_city_global_id(city_name):
    cidades = listar_cidades()
    for cidade in cidades:
        if cidade["local"].lower() == city_name.lower():
            return cidade["globalIdLocal"]
    return None

def escolher_cidade(cidades):
    print("Escolha uma cidade:")
    for idx, cidade in enumerate(cidades, start=1):
        print(f"{idx}. {cidade['local']}")
    while True:
        escolha = input("Digite o número da cidade: ").strip()
        if not escolha.isdigit():
            print("Por favor, digite um número válido.")
            continue
        escolha_num = int(escolha)
        if 1 <= escolha_num <= len(cidades):
            return cidades[escolha_num - 1]
        else:
            print("Número inválido, tente novamente.")

def get_forecast_by_global_id(global_id):
    url = f"https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{global_id}.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Erro ao buscar previsão: {e}")
        return None
