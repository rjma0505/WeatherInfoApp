def is_valid_city_name(name):
    if not name or not name.strip():
        return False
    # Permite letras, espaços e caracteres especiais comuns em nomes (acentos, hífens)
    import re
    pattern = r"^[a-zA-ZÀ-ÿ\s\-]+$"
    return bool(re.match(pattern, name.strip()))
