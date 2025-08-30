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

        self.paginaPrincipal = self._criarPaginaAnalise()
        self.stackedWidget.addWidget(self.paginaPrincipal)

        self._popularFiltrosAnalise()
        self._atualizarGraficoLinha()

    def _criarPaginaAnalise(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)

        headerWidget = self._criarHeaderAnalise()
        layoutPrincipal.addWidget(headerWidget)

        self.layoutGraficoLinha = QVBoxLayout()
        layoutPrincipal.addLayout(self.layoutGraficoLinha)

        return pagina

    def _criarHeaderAnalise(self):
        headerWidget = QWidget()
        layoutHeader = QVBoxLayout(headerWidget)

        layoutTitulo = QHBoxLayout()
        rotuloTitulo = QLabel("Evolução da Nota Média por Ano")
        rotuloTitulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layoutTitulo.addWidget(rotuloTitulo)
        layoutTitulo.addStretch()
        layoutHeader.addLayout(layoutTitulo)

        layoutFiltros = QHBoxLayout()

        containerCurso, self.comboCurso = self._criarFiltroComboBox("Curso:")
        containerDemanda, self.comboDemanda = self._criarFiltroComboBox("Demanda:")

        botaoGerarGrafico = QPushButton("Gerar Gráfico")
        botaoGerarGrafico.clicked.connect(self._atualizarGraficoLinha)

        layoutFiltros.addWidget(containerCurso)
        layoutFiltros.addWidget(containerDemanda)
        layoutFiltros.addWidget(
            botaoGerarGrafico, alignment=Qt.AlignmentFlag.AlignBottom
        )

        layoutHeader.addLayout(layoutFiltros)
        return headerWidget

    def _criarFiltroComboBox(self, textoRotulo):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(textoRotulo))
        comboBox = QComboBox()
        layout.addWidget(comboBox)
        return container, comboBox

    # TODO -> Resolver o problema de multiplicação de cursos e cursos com nomes inválidos

    def _popularFiltrosAnalise(self):
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]
        cursos = sorted(
            {s.get("curso", "") for s in todosOsAlunos if s.get("curso", "")}
        )
        demandas = sorted(
            {
                s.get("concorrencia", "")
                for s in todosOsAlunos
                if s.get("concorrencia", "")
            }
        )

        self.comboCurso.addItems(cursos)
        self.comboDemanda.addItems(demandas)

    def _atualizarGraficoLinha(self):
        while self.layoutGraficoLinha.count():
            item = self.layoutGraficoLinha.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cursoSelecionado = self.comboCurso.currentText()
        demandaSelecionada = self.comboDemanda.currentText()

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

    def _extrairAnoDaInscricao(self, inscricao):
        if inscricao and len(inscricao) >= 4:
            primeirosDigitos = inscricao[:2]
            if primeirosDigitos.isdigit():
                return "20" + primeirosDigitos
        return None
