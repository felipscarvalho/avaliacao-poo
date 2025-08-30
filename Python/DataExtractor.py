import json
import os


class DataExtractor:
    DEMAND_MAP = {
        "ampla_concorrencia": {"AC", "A0", "AD"},
        "escola_publica_baixa_renda": {"L1", "LB_EP"},
        "escola_publica_baixa_renda_ppi": {"L2", "LB_PPI"},
        "escola_publica_independente_renda": {"L5", "LI_EP"},
        "escola_publica_independente_renda_ppi": {"L6", "LI_PPI"},
        "escola_publica_baixa_renda_pcd": {"L9", "LB_PCD"},
        "escola_publica_baixa_renda_ppi_pcd": {"L10", ""},
        "escola_publica_baixa_renda_q": {"LB_Q"},
        "escola_publica_q": {"LI_Q"},
        "escola_publica_independente_renda_pcd": {"L13", "LI_PCD"},
        "escola_publica_independente_renda_ppi_pcd": {"L14"},
        "pcd": {"V", "V1751", "V3062", "V4061", "V6071", "V7825"},
    }

    def __init__(self):
        self.data = None
        self._loadData()

    def _loadData(self):
        try:
            currentDirectory = os.path.dirname(os.path.abspath(__file__))
            pathToJson = os.path.join(
                currentDirectory, "..", "DataFiles", "Aprovados.json"
            )

            with open(pathToJson, "r", encoding="utf-8") as jsonFile:
                self.data = json.load(jsonFile)
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = {}

    def getDataByYear(self, year):
        if self.data:
            return self.data.get(str(year), [])
        return []

    def getData(self, year=None, course=None, demand=None, state=None, campus=None):
        results = (
            self.getDataByYear(year)
            if year
            else [
                student for yearlyList in self.data.values() for student in yearlyList
            ]
        )

        if demand:
            equivalentDemands = set()
            demandUpper = demand.upper()

            for group, codes in self.DEMAND_MAP.items():
                if demandUpper in codes:
                    equivalentDemands = codes
                    break

            if not equivalentDemands:
                equivalentDemands = {demandUpper}

            results = [
                student
                for student in results
                if student.get("concorrencia", "").upper() in equivalentDemands
            ]

        if course:
            results = [
                student
                for student in results
                if course.lower() in student.get("curso", "").lower()
            ]
        if state:
            results = [
                student
                for student in results
                if student.get("estado", "").lower() == state.lower()
            ]
        if campus:
            results = [
                student
                for student in results
                if student.get("campus", "").lower() == campus.lower()
            ]

        return results
