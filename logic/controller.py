from data_access.ipma_api import listar_cidades, get_forecast_by_global_id
from data_access.data_parser import parse_forecast_data

def fetch_forecast_by_city_name(city_name):
    cidades = listar_cidades()
    if not cidades:
        print("Não foi possível carregar cidades.")
        return None

    cidade_selecionada = next((c for c in cidades if c["local"].lower() == city_name.lower()), None)
    if not cidade_selecionada:
        print("Cidade não encontrada.")
        return None

    print(f"Selecionada: {cidade_selecionada['local']} (globalIdLocal={cidade_selecionada['globalIdLocal']})")

    raw_data = get_forecast_by_global_id(cidade_selecionada["globalIdLocal"])
    print(f"Resposta bruta da previsão: {raw_data}")

    if raw_data is None:
        print("Não foi possível obter dados da previsão.")
        return None
    
    # Passar só o campo 'data' para o parser
    return parse_forecast_data(raw_data.get("data", []))
