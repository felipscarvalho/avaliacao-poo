import csv
import os
from collections import defaultdict
from statistics import mean


class ExtratorDeDados:
    MAPA_DEMANDA = {
        "AC": "AC",
        "A0": "AC",
        "AD": "AC",
        "L1": "LB_EP",
        "LB_EP": "LB_EP",
        "L2": "LB_PPI",
        "LB_PPI": "LB_PPI",
        "L5": "LI_EP",
        "LI_EP": "LI_EP",
        "L6": "LI_PPI",
        "LI_PPI": "LI_PPI",
        "L9": "LB_PCD",
        "LB_PCD": "LB_PCD",
        "L10": "L10",
        "LB_Q": "LB_Q",
        "LI_Q": "LI_Q",
        "L13": "LI_PCD",
        "LI_PCD": "LI_PCD",
        "L14": "L14",
        "V": "V",
        "V1751": "V",
        "V3062": "V",
        "V4061": "V",
        "V6071": "V",
        "V7825": "V",
    }

    def __init__(self):
        self.dados = None
        self._carregarDados()

    def _padronizarNomeCurso(self, nomeCurso):
        if not nomeCurso:
            return ""
        return " ".join(nomeCurso.replace("-", " ").split())

    def _carregarDados(self):
        self.dados = defaultdict(list)
        try:
            diretorioAtual = os.path.dirname(os.path.abspath(__file__))
            caminhoCSV = os.path.join(
                diretorioAtual, "..", "DataFiles", "sisuDados.csv"
            )

            with open(caminhoCSV, mode="r", encoding="utf-8") as dadosCSV:
                leitorCSV = csv.DictReader(dadosCSV)
                for linha in leitorCSV:
                    ano = linha.get("Ano")
                    if not ano:
                        continue

                    estudante = {
                        "inscricao": linha.get("N. ENEM"),
                        "nome": linha.get("Nome"),
                        "curso": self._padronizarNomeCurso(linha.get("Curso")),
                        "campus": linha.get("Campus"),
                        "cota": self.MAPA_DEMANDA.get(
                            linha.get("Demanda*"), linha.get("Demanda*")
                        ),
                        "nota": linha.get("Média"),
                        "classificacao": linha.get("Coloc."),
                        "estado": linha.get("Est."),
                        "ano": ano,
                    }
                    self.dados[ano].append(estudante)

            self.dados = dict(self.dados)
            print("Dados do CSV carregados e agrupados por ano com sucesso!")

        except FileNotFoundError:
            print(
                f"Erro: O arquivo '{os.path.abspath(caminhoCSV)}' não foi encontrado."
            )
            self.dados = {}
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao carregar o CSV: {e}")
            self.dados = {}

    def getDadosPorAno(self, ano):
        if self.dados:
            return self.dados.get(str(ano), [])
        return []

    def getMediaGeral(self):
        notas = []
        for candidato in self.getDados():
            notaStr = candidato.get("nota")
            if notaStr:
                try:
                    notaFloat = float(notaStr.replace(",", "."))
                    notas.append(notaFloat)
                except (ValueError, TypeError):
                    continue

        if not notas:
            return 0.0

        return mean(notas)

    def getDados(self, ano=None, curso=None, cota=None, estado=None, campus=None):
        resultados = (
            self.getDadosPorAno(ano)
            if ano
            else [
                candidato
                for listaAnual in self.dados.values()
                for candidato in listaAnual
            ]
        )
        if cota:
            resultados = [
                candidato
                for candidato in resultados
                if candidato.get("cota", "").upper() == cota
            ]
        if curso:
            resultados = [
                candidato
                for candidato in resultados
                if curso.lower() in candidato.get("curso", "").lower()
            ]
        if estado:
            resultados = [
                candidato
                for candidato in resultados
                if candidato.get("estado", "").lower() == estado.lower()
            ]
        if campus:
            resultados = [
                candidato
                for candidato in resultados
                if candidato.get("campus", "").lower() == campus.lower()
            ]
        return resultados
