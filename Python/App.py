import sys
import re
from collections import defaultdict
from statistics import mean

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QStackedWidget,
    QApplication,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from DataExtractor import DataExtractor
from Graphs import GeradorDeGraficos


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análise do SISU-UFS")
        self.setGeometry(100, 100, 1200, 800)

        self.extratorDeDados = DataExtractor()
        self.geradorDeGraficos = GeradorDeGraficos()

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.paginaPrincipal = self._criarPaginaPrincipal()
        self.paginaAnaliseNotaCorte = self._criarPaginaGraficoLinha()

        self.stackedWidget.addWidget(self.paginaPrincipal)
        self.stackedWidget.addWidget(self.paginaAnaliseNotaCorte)

    def _criarPaginaPrincipal(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)

        # --- Layout do Topo ---
        layoutTopo = QHBoxLayout()
        titulo = QLabel("Visão Geral: Perfil dos Aprovados")
        titulo.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        botaoIrAnalise = QPushButton("Analisar Nota de Corte →")
        botaoIrAnalise.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.paginaAnaliseNotaCorte)
        )
        layoutTopo.addWidget(titulo)
        layoutTopo.addStretch()
        layoutTopo.addWidget(botaoIrAnalise)
        layoutPrincipal.addLayout(layoutTopo)

        # --- Layout dos Filtros ---
        layoutFiltros = QHBoxLayout()
        # Filtro 1: Tipo de Análise (Estado ou Campus)
        containerTipoAnalise, self.comboTipoAnalise = self._criarFiltroComboBox(
            "Tipo de Análise:"
        )
        self.comboTipoAnalise.addItems(
            ["Por Estado (em um Curso)", "Por Campus (Geral)"]
        )

        # Filtro 2: Curso (só aparece quando necessário)
        self.containerFiltroCurso, self.comboCursoPizza = self._criarFiltroComboBox(
            "Filtrar por Curso:"
        )

        layoutFiltros.addWidget(containerTipoAnalise)
        layoutFiltros.addWidget(self.containerFiltroCurso)
        layoutFiltros.addStretch()
        layoutPrincipal.addLayout(layoutFiltros)

        # --- Layout do Gráfico ---
        self.layoutGraficoPizza = QVBoxLayout()
        layoutPrincipal.addLayout(self.layoutGraficoPizza)

        # Conecta os sinais para atualizar a UI dinamicamente
        self.comboTipoAnalise.currentTextChanged.connect(self._atualizarUIPrincipal)
        self.comboCursoPizza.currentTextChanged.connect(self._atualizarUIPrincipal)

        self._popularFiltroCursosPizza()
        self._atualizarUIPrincipal()

        return pagina

    def _atualizarUIPrincipal(self):
        """Controla a visibilidade dos filtros e qual gráfico é exibido."""
        tipoAnalise = self.comboTipoAnalise.currentText()

        if tipoAnalise == "Por Estado (em um Curso)":
            self.containerFiltroCurso.setVisible(True)
            self._atualizarGraficoEstado()
        else:  # "Por Campus (Geral)"
            self.containerFiltroCurso.setVisible(False)
            self._atualizarGraficoCampus()

    def _atualizarGraficoCampus(self):
        """Calcula e exibe o gráfico de pizza por campus."""
        # Limpa o gráfico anterior
        while self.layoutGraficoPizza.count():
            item = self.layoutGraficoPizza.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]
        contagemCampus = defaultdict(int)
        for aluno in todosOsAlunos:
            if aluno.get("campus", "N/A") != "N/A":
                contagemCampus[aluno["campus"]] += 1

        graficoCampus = self.geradorDeGraficos.criarGraficoDePizza(
            dados=contagemCampus, titulo="Porcentagem de Aprovados por Campus (Geral)"
        )
        self.layoutGraficoPizza.addWidget(graficoCampus)

    def _atualizarGraficoEstado(self):
        """Calcula e exibe o gráfico de pizza por estado para um curso."""
        while self.layoutGraficoPizza.count():
            item = self.layoutGraficoPizza.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cursoSelecionado = self.comboCursoPizza.currentText()
        if not cursoSelecionado:
            return

        alunosDoCurso = self.extratorDeDados.getData(course=cursoSelecionado)

        contagemEstado = defaultdict(int)
        for aluno in alunosDoCurso:
            if aluno.get("estado", "N/A") != "N/A":
                contagemEstado[aluno["estado"]] += 1

        graficoEstado = self.geradorDeGraficos.criarGraficoDePizza(
            dados=contagemEstado,
            titulo=f"Origem (Estado) dos Aprovados em\n{cursoSelecionado}",
        )
        self.layoutGraficoPizza.addWidget(graficoEstado)

    def _popularFiltroCursosPizza(self):
        """Popula o ComboBox de cursos com dados limpos."""
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]

        # Conjunto de todas as siglas de demanda para limpeza
        todasAsDemandas = set()
        for codes in self.extratorDeDados.DEMAND_MAP.values():
            todasAsDemandas.update(codes)

        dadosBrutosCursos = sorted(
            {s.get("curso", "") for s in todosOsAlunos if s.get("curso", "")}
        )

        cursos = [s for s in dadosBrutosCursos if not re.search(r"\d", s)]

        self.comboCursoPizza.addItems(cursos)

    def _criarPaginaGraficoLinha(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)
        headerWidget = self._criarHeaderAnalise()
        layoutPrincipal.addWidget(headerWidget)
        self.layoutGraficoLinha = QVBoxLayout()
        layoutPrincipal.addLayout(self.layoutGraficoLinha)
        self._popularFiltrosLinha()
        self._atualizarGraficoLinha()
        return pagina

    def _criarHeaderAnalise(self):
        headerWidget = QWidget()
        layoutHeader = QVBoxLayout(headerWidget)
        layoutTitulo = QHBoxLayout()
        rotuloTitulo = QLabel("Evolução da Nota Média por Ano")
        rotuloTitulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        botaoVoltar = QPushButton("← Voltar para Visão Geral")
        botaoVoltar.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.paginaPrincipal)
        )
        layoutTitulo.addWidget(rotuloTitulo)
        layoutTitulo.addStretch()
        layoutTitulo.addWidget(botaoVoltar)
        layoutHeader.addLayout(layoutTitulo)
        layoutFiltros = QHBoxLayout()
        containerCurso, self.comboCursoLinha = self._criarFiltroComboBox("Curso:")
        containerDemanda, self.comboDemandaLinha = self._criarFiltroComboBox("Demanda:")
        botaoGerarGrafico = QPushButton("Gerar Gráfico")
        botaoGerarGrafico.clicked.connect(self._atualizarGraficoLinha)
        layoutFiltros.addWidget(containerCurso)
        layoutFiltros.addWidget(containerDemanda)
        layoutFiltros.addWidget(
            botaoGerarGrafico, alignment=Qt.AlignmentFlag.AlignBottom
        )
        layoutHeader.addLayout(layoutFiltros)
        return headerWidget

    def _popularFiltrosLinha(self):
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]

        dadosBrutosCursos = sorted(
            {s.get("curso", "") for s in todosOsAlunos if s.get("curso", "")}
        )

        cursos = [s for s in dadosBrutosCursos if not re.search(r"\d", s)]

        demandas = sorted(
            {
                "AC",
                "LB_EP",
                "LB_PPI",
                "LI_PPI",
                "LI_EP",
                "LB_PCD",
                "LI_PCD",
                "V",
                "LB_Q",
                "LI_Q",
            }
        )

        self.comboCursoLinha.addItems(cursos)
        self.comboDemandaLinha.addItems(demandas)

    def _atualizarGraficoLinha(self):
        while self.layoutGraficoLinha.count():
            item = self.layoutGraficoLinha.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        cursoSelecionado = self.comboCursoLinha.currentText()
        demandaSelecionada = self.comboDemandaLinha.currentText()
        alunosFiltrados = self.extratorDeDados.getData(
            course=cursoSelecionado, demand=demandaSelecionada
        )
        notasPorAno = defaultdict(list)
        for aluno in alunosFiltrados:
            notaStr = aluno.get("nota", "N/A").replace(",", ".")
            ano = self._extrairAnoDaInscricao(aluno.get("inscricao", ""))
            if ano and notaStr != "N/A":
                try:
                    notasPorAno[ano].append(float(notaStr))
                except ValueError:
                    continue
        dadosParaGrafico = {
            ano: mean(notas) for ano, notas in notasPorAno.items() if notas
        }
        widgetGrafico = self.geradorDeGraficos.criarGraficoDeLinha(
            dados=dadosParaGrafico,
            titulo=cursoSelecionado,
            subtitulo=f"Demanda: {demandaSelecionada}",
            eixoXTitulo="Ano",
            eixoYTitulo="Nota Média",
        )
        self.layoutGraficoLinha.addWidget(widgetGrafico)

    def _criarFiltroComboBox(self, textoRotulo):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(textoRotulo))
        comboBox = QComboBox()
        comboBox.setMinimumWidth(250)
        layout.addWidget(comboBox)
        return container, comboBox

    def _extrairAnoDaInscricao(self, inscricao):
        if inscricao and len(inscricao) >= 4:
            primeirosDigitos = inscricao[:2]
            if primeirosDigitos.isdigit():
                return "20" + primeirosDigitos
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
