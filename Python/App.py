from collections import defaultdict
from statistics import mean
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QScrollArea,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from ExtratorDeDados import ExtratorDeDados
from Graficos import GeradorDeGraficos

ESTILO_BOTAO_HEADER = """
    QPushButton {
        background-color: transparent;
        border: none;
        padding: 10px 15px;
        font-size: 15px;
        font-weight: bold;
        color: #555;
    }
    QPushButton:hover {
        color: #000;
    }
    QPushButton:checked {
        color: #007bff;
        border-bottom: 3px solid #007bff;
    }
"""

ESTILO_BOTAO_TABLE = """
    QPushButton {
        background-color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: bold;
        color: blue;
        min-height: 50;
        min-width: 100
    }
"""


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISU BI")
        self.setGeometry(100, 100, 1400, 900)

        self.extratorDeDados = ExtratorDeDados()
        self.geradorDeGraficos = GeradorDeGraficos()

        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        layoutPrincipal = QVBoxLayout(widgetCentral)
        layoutPrincipal.setSpacing(0)
        layoutPrincipal.setContentsMargins(0, 0, 0, 0)

        header = self._criarHeader()
        layoutPrincipal.addWidget(header)

        self.stackedWidget = QStackedWidget()
        layoutPrincipal.addWidget(self.stackedWidget)

        self.paginaDashboard = self._criarPaginaDashboard()
        self.paginaEstudantes = self._criarPaginaEstudantes()
        self.paginaGraficos = self._criarPaginaGraficos()

        self.stackedWidget.addWidget(self.paginaDashboard)
        self.stackedWidget.addWidget(self.paginaEstudantes)
        self.stackedWidget.addWidget(self.paginaGraficos)

        self.botaoDashboard.setChecked(True)
        self.stackedWidget.setCurrentWidget(self.paginaDashboard)

    def _mudarDeTela(self, indice, botaoPressionado):
        self.stackedWidget.setCurrentIndex(indice)
        for botao in self.botoesHeader:
            botao.setChecked(botao == botaoPressionado)

    def _criarHeader(self):
        headerWidget = QWidget()
        headerWidget.setFixedHeight(70)
        headerWidget.setStyleSheet(
            "background-color: #ffffff; border-bottom: 1px solid #dcdcdc;"
        )

        layoutHeader = QHBoxLayout(headerWidget)
        layoutHeader.setContentsMargins(20, 0, 20, 0)

        titulo = QLabel("SISU BI")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #007bff;")

        layoutHeader.addWidget(titulo)
        layoutHeader.addStretch()

        self.botaoDashboard = QPushButton("Dashboard")
        self.botaoEstudantes = QPushButton("Estudantes")
        self.botaoGraficos = QPushButton("Gráficos")

        self.botoesHeader = [
            self.botaoDashboard,
            self.botaoEstudantes,
            self.botaoGraficos,
        ]

        for botao in self.botoesHeader:
            botao.setStyleSheet(ESTILO_BOTAO_HEADER)
            botao.setCheckable(True)
            layoutHeader.addWidget(botao)

        self.botaoDashboard.clicked.connect(
            lambda: self._mudarDeTela(0, self.botaoDashboard)
        )
        self.botaoEstudantes.clicked.connect(
            lambda: self._mudarDeTela(1, self.botaoEstudantes)
        )
        self.botaoGraficos.clicked.connect(
            lambda: self._mudarDeTela(2, self.botaoGraficos)
        )

        return headerWidget

    def _criarPaginaDashboard(self):
        paginaDashboard = QWidget()

        layoutPagina = QVBoxLayout(paginaDashboard)
        layoutPagina.setContentsMargins(50, 50, 50, 50)
        layoutPagina.addStretch(1)

        rotuloTitulo = QLabel("Bem-Vindo ao Sistema!")
        rotuloTitulo.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        rotuloTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutPagina.addWidget(rotuloTitulo)

        layoutBotoes = QHBoxLayout()
        layoutBotoes.addStretch(1)

        mediaGeral = self.extratorDeDados.getMediaGeral()

        container1 = QPushButton(
            f"Número de Aprovados: {len(self.extratorDeDados.getDados())}"
        )
        container2 = QPushButton("Anos coletados: 6")
        container3 = QPushButton(f"Média Geral: {mediaGeral:.1f}")

        for botao in [container1, container2, container3]:
            botao.setStyleSheet(ESTILO_BOTAO_TABLE)
            botao.setCheckable(False)

        layoutBotoes.addWidget(container1)
        layoutBotoes.addWidget(container2)
        layoutBotoes.addWidget(container3)
        layoutBotoes.addStretch(1)

        layoutPagina.addLayout(layoutBotoes)

        rotuloSubtitulo = QLabel("Selecione uma das Abas de navegação para começar")
        rotuloSubtitulo.setFont(QFont("Arial", 14))
        rotuloSubtitulo.setStyleSheet("color: #6c757d;")
        rotuloSubtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layoutPagina.addWidget(rotuloSubtitulo)
        layoutPagina.addStretch(1)

        return paginaDashboard

    def _criarPaginaEstudantes(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)

        self.tabelaEstudantes = QTableWidget()
        self.tabelaEstudantes.setSortingEnabled(True)
        self.tabelaEstudantes.setAlternatingRowColors(True)

        layoutPrincipal.addWidget(self.tabelaEstudantes)

        self._atualizarTabelaEstudantes()

        return pagina

    def _atualizarTabelaEstudantes(self):
        self._popularTabela(self.tabelaEstudantes, self.extratorDeDados.getDados())

    def _popularTabela(self, tabela, dados):
        tabela.setRowCount(0)
        if not dados:
            return

        headers = [
            "Ano",
            "Inscrição",
            "Nome",
            "Curso",
            "Campus",
            "Cota",
            "Nota",
            "Classificação",
            "Estado",
        ]

        tabela.setColumnCount(len(headers))
        tabela.setHorizontalHeaderLabels(headers)
        tabela.setRowCount(len(dados))

        for linha, aluno in enumerate(dados):
            tabela.setItem(linha, 0, QTableWidgetItem(aluno.get("ano")))
            tabela.setItem(linha, 1, QTableWidgetItem(aluno.get("inscricao")))
            tabela.setItem(linha, 2, QTableWidgetItem(aluno.get("nome")))
            tabela.setItem(linha, 3, QTableWidgetItem(aluno.get("curso")))
            tabela.setItem(linha, 4, QTableWidgetItem(aluno.get("campus")))
            tabela.setItem(linha, 5, QTableWidgetItem(aluno.get("cota")))
            tabela.setItem(linha, 6, QTableWidgetItem(aluno.get("nota")))
            tabela.setItem(linha, 7, QTableWidgetItem(aluno.get("classificacao")))
            tabela.setItem(linha, 8, QTableWidgetItem(aluno.get("estado")))

        tabela.resizeColumnsToContents()
        tabela.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        tabela.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )

    def _criarPaginaGraficos(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        layoutPrincipal.addWidget(scrollArea)

        scrollContent = QWidget()
        scrollArea.setWidget(scrollContent)

        layoutScroll = QVBoxLayout(scrollContent)

        containerLinhas = QWidget()
        layoutLinhas = QVBoxLayout(containerLinhas)

        layoutFiltroLinhas = QHBoxLayout()
        layoutFiltroLinhas.addWidget(
            QLabel("Análise de Nota Media de Cotas por Curso:")
        )

        self.comboCursoGraficos = QComboBox()
        self.comboCursoGraficos.setMinimumWidth(300)

        layoutFiltroLinhas.addWidget(self.comboCursoGraficos)
        layoutFiltroLinhas.addStretch()

        self.layoutGraficoMultiLinha = QVBoxLayout()
        layoutLinhas.addLayout(layoutFiltroLinhas)
        layoutLinhas.addLayout(self.layoutGraficoMultiLinha)
        layoutScroll.addWidget(containerLinhas)

        containerInferior = QWidget()
        layoutInferior = QVBoxLayout(containerInferior)

        filtroAnoLayout = QHBoxLayout()
        filtroAnoLayout.addStretch()
        filtroAnoLayout.addWidget(
            QLabel("Filtrar Gráficos de Média e Distribuição por Ano:")
        )

        self.comboAnoGraficosAgrupados = QComboBox()
        self.comboAnoGraficosAgrupados.setMinimumWidth(200)

        filtroAnoLayout.addWidget(self.comboAnoGraficosAgrupados)
        filtroAnoLayout.addStretch()
        layoutInferior.addLayout(filtroAnoLayout)

        # Layout para os gráficos de barras e pizza
        layoutGraficosVerticais = QVBoxLayout()
        self.layoutGraficoBarraMedia = QVBoxLayout()
        self.layoutGraficoPizzaNotas = QVBoxLayout()

        layoutGraficosVerticais.addLayout(self.layoutGraficoBarraMedia)
        layoutGraficosVerticais.addLayout(self.layoutGraficoPizzaNotas)
        layoutInferior.addLayout(layoutGraficosVerticais)

        layoutScroll.addWidget(containerInferior)

        self.comboCursoGraficos.currentTextChanged.connect(
            self._atualizarGraficoMultiLinha
        )
        self.comboAnoGraficosAgrupados.currentTextChanged.connect(
            self._atualizarGraficosAgrupados
        )

        self._popularFiltrosGraficos()
        self._atualizarGraficoMultiLinha()
        self._atualizarGraficosAgrupados()

        return pagina

    def _popularFiltrosGraficos(self):
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.dados.values()
            for aluno in listaAnual
        ]
        # Popula o filtro de cursos
        cursos = sorted(
            list(
                {
                    s.get("curso", "N/A")
                    for s in todosOsAlunos
                    if s.get("curso", "N/A") != "N/A"
                }
            )
        )
        self.comboCursoGraficos.addItems(cursos)

        # Popula o filtro de anos
        anos = sorted(list(self.extratorDeDados.dados.keys()), reverse=True)
        self.comboAnoGraficosAgrupados.addItem("Todos")
        self.comboAnoGraficosAgrupados.addItems(anos)

    def _atualizarGraficosAgrupados(self):
        anoSelecionado = self.comboAnoGraficosAgrupados.currentText()
        alunosFiltrados = (
            self.extratorDeDados.getDadosPorAno(anoSelecionado)
            if anoSelecionado != "Todos"
            else [a for la in self.extratorDeDados.dados.values() for a in la]
        )

        self._atualizarGraficoBarraMediaPorCurso(alunosFiltrados, anoSelecionado)
        self._atualizarGraficoPizzaNotas(alunosFiltrados, anoSelecionado)

    def _atualizarGraficoBarraMediaPorCurso(self, alunos, ano):
        while self.layoutGraficoBarraMedia.count():
            item = self.layoutGraficoBarraMedia.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        titulo = f"Top 20 Cursos por Nota Média ({ano})"
        notasPorCurso = defaultdict(list)
        for aluno in alunos:
            curso = aluno.get("curso", "N/A")
            notaStr = aluno.get("nota", "N/A").replace(",", ".")
            if curso != "N/A" and notaStr != "N/A":
                try:
                    notasPorCurso[curso].append(float(notaStr))
                except ValueError:
                    continue

        mediaPorCurso = {
            curso: mean(notas) for curso, notas in notasPorCurso.items() if notas
        }

        top20Cursos = dict(
            sorted(mediaPorCurso.items(), key=lambda item: item[1], reverse=True)[:20]
        )

        graficoBarras = self.geradorDeGraficos.criarGraficoDeBarraNotaMediaPorCurso(
            dados=top20Cursos, titulo=titulo
        )

        graficoBarras.setMinimumHeight(800)

        self.layoutGraficoBarraMedia.addWidget(graficoBarras)

    def _atualizarGraficoPizzaNotas(self, alunos, ano):
        while self.layoutGraficoPizzaNotas.count():
            item = self.layoutGraficoPizzaNotas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        titulo = f"Distribuição de Notas ({ano})"
        faixas = {
            "400-500": 0,
            "500-600": 0,
            "600-700": 0,
            "700-800": 0,
            "800-900": 0,
            "900-1000": 0,
        }

        for aluno in alunos:
            notaStr = aluno.get("nota", "N/A").replace(",", ".")
            if notaStr != "N/A":
                try:
                    nota = float(notaStr)
                    if 400 <= nota < 500:
                        faixas["400-500"] += 1
                    elif 500 <= nota < 600:
                        faixas["500-600"] += 1
                    elif 600 <= nota < 700:
                        faixas["600-700"] += 1
                    elif 700 <= nota < 800:
                        faixas["700-800"] += 1
                    elif 800 <= nota < 900:
                        faixas["800-900"] += 1
                    elif 900 <= nota <= 1000:
                        faixas["900-1000"] += 1
                except ValueError:
                    continue

        graficoPizza = self.geradorDeGraficos.criarGraficoPizzaDistribuicaoNotas(
            dados=faixas, titulo=titulo
        )

        graficoPizza.setMinimumHeight(800)

        self.layoutGraficoPizzaNotas.addWidget(graficoPizza)

    def _atualizarGraficoMultiLinha(self):
        while self.layoutGraficoMultiLinha.count():
            item = self.layoutGraficoMultiLinha.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cursoSelecionado = self.comboCursoGraficos.currentText()
        if not cursoSelecionado:
            return

        alunosFiltrados = self.extratorDeDados.getDados(curso=cursoSelecionado)
        notasPorCotaPorAno = defaultdict(lambda: defaultdict(list))

        for aluno in alunosFiltrados:
            cota = aluno.get("cota", "N/A")
            notaStr = aluno.get("nota", "N/A").replace(",", ".")
            ano = aluno.get("ano")
            if cota != "N/A" and notaStr != "N/A" and ano and ano.isdigit():
                try:
                    notasPorCotaPorAno[cota][ano].append(float(notaStr))
                except (ValueError, IndexError):
                    continue

        dadosParaGrafico = defaultdict(dict)

        for cota, notasPorAno in notasPorCotaPorAno.items():
            for ano, notas in notasPorAno.items():
                if notas:
                    dadosParaGrafico[cota][ano] = mean(notas)

        widgetGrafico = self.geradorDeGraficos.criarGraficoDeLinhaMultiplasSeries(
            dadosSeries=dadosParaGrafico,
            titulo=cursoSelecionado,
            eixoXTitulo="Ano",
            eixoYTitulo="Nota Média",
        )

        widgetGrafico.setMinimumHeight(900)

        self.layoutGraficoMultiLinha.addWidget(widgetGrafico)
