import pdfplumber
import os
import re
import json
from collections import defaultdict


def clean_repeated_chars(text):
    """Remove caracteres duplicados que são artefatos da extração do PDF."""
    return re.sub(r"(.)\1+", r"\1", text)


def convert_pdf_to_json(pdf_path):
    """
    Converte um PDF de aprovados para JSON com uma lógica de extração universal,
    incluindo uma busca precisa por siglas de estados brasileiros.
    """
    print(f"Iniciando a conversão do arquivo: '{pdf_path}'...")

    if not os.path.exists(pdf_path):
        print("  -> Erro: Arquivo não encontrado.")
        return

    # **CORREÇÃO: Lista definitiva de siglas de estados brasileiros**
    BRAZILIAN_STATES = [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
    states_pattern = (
        r"\s(" + "|".join(BRAZILIAN_STATES) + r")$"
    )  # Ex: \s(AC|AL|...|TO)$

    all_students_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(
                    x_tolerance=1, y_tolerance=1, keep_blank_chars=False
                )
                if not words:
                    continue

                lines = defaultdict(list)
                for word in words:
                    lines[int(word["top"])].append(word)

                for y_pos in sorted(lines.keys()):
                    line_words = sorted(lines[y_pos], key=lambda w: w["x0"])
                    line_text = " ".join(w["text"] for w in line_words)

                    match = re.match(r"^(?P<inscricao>[\d\*]{10,})\s+.*", line_text)
                    if not match:
                        continue

                    inscricao = match.group("inscricao")

                    start_index = -1
                    for i, word in enumerate(line_words):
                        if word["text"] in inscricao:
                            start_index = i + 1
                            break
                    if start_index == -1:
                        continue

                    relevant_words = line_words[start_index:]
                    if not relevant_words:
                        continue

                    max_gap, split_index = 0, len(relevant_words)
                    for i in range(len(relevant_words) - 1):
                        gap = relevant_words[i + 1]["x0"] - relevant_words[i]["x1"]
                        if gap > max_gap and gap > 10:
                            max_gap = gap
                            split_index = i + 1

                    nome = " ".join(w["text"] for w in relevant_words[:split_index])
                    remaining_text = " ".join(
                        w["text"] for w in relevant_words[split_index:]
                    )

                    data = {}

                    # Usa a nova regex precisa para encontrar o estado
                    estado_match = re.search(states_pattern, remaining_text)
                    if estado_match:
                        data["estado"] = estado_match.group(1)
                        remaining_text = remaining_text[: estado_match.start()].strip()

                    classificacao_match = re.search(r"\s(\d+º?)$", remaining_text)
                    if classificacao_match:
                        data["classificacao"] = classificacao_match.group(1)
                        remaining_text = remaining_text[
                            : classificacao_match.start()
                        ].strip()

                    nota_match = re.search(r"(\d{2,3}[,.]\d{2,3})", remaining_text)
                    if nota_match:
                        data["nota"] = nota_match.group(1).replace(".", ",")
                        remaining_text = remaining_text.replace(nota_match.group(1), "")

                    campus_pattern = r"(SAO CRISTOVAO|ARACAJU|LAGARTO|LARANJEIRAS|ITABAIANA|SERTÃO|CAMPUS DO SERTAO|CAMPUS DO SER)"
                    campus_match = re.search(
                        campus_pattern, remaining_text, re.IGNORECASE
                    )
                    if campus_match:
                        campus_found = campus_match.group(0).strip().upper()
                        data["campus"] = (
                            "Sertão" if "SER" in campus_found else campus_found.title()
                        )
                        remaining_text = re.sub(
                            campus_pattern,
                            "",
                            remaining_text,
                            flags=re.IGNORECASE,
                            count=1,
                        )

                    tipos_concorrencia = r"(?<!\w)(AC|A0|AD|L1|L2|L5|L6|L9|L10|L13|L14|V7825|V3062|V4061|V1751|V6071|D3|LB_PPI|LI_PPI|LB_Q|LI_Q|LB_PCD|LI_PCD|LB_EP|LI_EP|V)\b"
                    tipo_match = re.search(tipos_concorrencia, remaining_text)
                    if tipo_match:
                        data["concorrencia"] = tipo_match.group(1)
                        remaining_text = re.sub(
                            r"\s" + data["concorrencia"] + r"\b",
                            " ",
                            remaining_text,
                            count=1,
                        )

                    curso = " ".join(remaining_text.split())

                    all_students_data.append(
                        {
                            "inscricao": inscricao,
                            "nome": clean_repeated_chars(nome.strip()),
                            "curso": clean_repeated_chars(curso.strip()),
                            "nota": data.get("nota", "N/A"),
                            "campus": data.get("campus", "N/A"),
                            "concorrencia": data.get("concorrencia", "N/A"),
                            "classificacao": data.get("classificacao", "N/A"),
                            "estado": data.get("estado", "N/A"),
                        }
                    )

        json_output_path = os.path.splitext(pdf_path)[0] + ".json"
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(all_students_data, f, ensure_ascii=False, indent=4)

        print(
            f"  -> Sucesso! {len(all_students_data)} registros salvos em '{json_output_path}'."
        )

    except Exception as e:
        print(
            f"  -> Ocorreu um erro inesperado durante a conversão de '{pdf_path}': {e}"
        )


if __name__ == "__main__":
    pdf_files = [
        "Aprovados19.pdf",
        "Aprovados20.pdf",
        "Aprovados21.pdf",
        "Aprovados22.pdf",
        "APROVADOS2023.pdf",
        "Aprovados2024.pdf",
        "APROVADOS2025.pdf",
    ]

    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            convert_pdf_to_json(pdf_file)
        else:
            print(f"Arquivo '{pdf_file}' não encontrado, pulando.")
    print("\nProcesso de conversão finalizado.")
