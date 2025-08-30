import json
import os
import re


def get_year_from_filename(filename):
    match = re.search(r"(\d+)", filename)
    if match:
        year_str = match.group(1)
        if len(year_str) == 2:
            return "20" + year_str
        elif len(year_str) == 4:
            return year_str
    return None


def unify_json_files():
    json_files = [
        f
        for f in os.listdir(".")
        if f.endswith(".json") and "UNIFICADO" not in f.upper()
    ]

    if not json_files:
        print("Nenhum arquivo .json encontrado para unificar.")
        return

    print("Arquivos encontrados para unificação:")
    for f in json_files:
        print(f" - {f}")

    unified_data = {}

    for file_name in json_files:
        year = get_year_from_filename(file_name)
        if not year:
            print(f"Não foi possível extrair o ano de '{file_name}'. Pulando.")
            continue

        try:
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                unified_data[year] = data
                print(f"Dados do ano {year} carregados com sucesso de '{file_name}'.")
        except json.JSONDecodeError:
            print(
                f"Erro ao ler o arquivo JSON '{file_name}'. Verifique se o formato está correto."
            )
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar '{file_name}': {e}")

    output_filename = "APROVADOS_UNIFICADO.json"

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(unified_data, f, ensure_ascii=False, indent=2)
        print(f"\nSucesso! Todos os dados foram unificados em '{output_filename}'.")
    except Exception as e:
        print(f"\nOcorreu um erro ao salvar o arquivo unificado: {e}")


if __name__ == "__main__":
    unify_json_files()
