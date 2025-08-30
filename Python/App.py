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
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from DataExtractor import DataExtractor
from Graphs import GeradorDeGraficos


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Análise do SISU-UFS")
        self.setGeometry(100, 100, 1400, 800)

        self.extratorDeDados = DataExtractor()
        self.geradorDeGraficos = GeradorDeGraficos()

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.paginaPrincipal = self._criarPaginaPrincipal()
        self.paginaAnaliseNotaCorte = self._criarPaginaGraficoLinha()
        self.paginaAnaliseDemandas = self._criarPaginaGraficoBarra()

        self.stackedWidget.addWidget(self.paginaPrincipal)
        self.stackedWidget.addWidget(self.paginaAnaliseNotaCorte)
        self.stackedWidget.addWidget(self.paginaAnaliseDemandas)

    def _criarPaginaPrincipal(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)
        layoutTopo = QHBoxLayout()
        titulo = QLabel("Visão Geral: Perfil dos Aprovados")
        titulo.setFont(QFont("Arial", 20, QFont.Weight.Bold))

        # Botões de Navegação
        botaoIrAnaliseCorte = QPushButton("Analisar Nota de Corte →")
        botaoIrAnaliseCorte.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.paginaAnaliseNotaCorte)
        )
        botaoIrAnaliseDemanda = QPushButton("Analisar Demandas →")
        botaoIrAnaliseDemanda.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.paginaAnaliseDemandas)
        )

        layoutTopo.addWidget(titulo)
        layoutTopo.addStretch()
        layoutTopo.addWidget(botaoIrAnaliseCorte)
        layoutTopo.addWidget(botaoIrAnaliseDemanda)
        layoutPrincipal.addLayout(layoutTopo)

        layoutGraficos = QHBoxLayout()
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
            dados=contagemCampus, titulo="Aprovados por Campus (Geral)"
        )
        layoutGraficos.addWidget(graficoCampus)
        containerGraficoEstado = QWidget()
        layoutContainerEstado = QVBoxLayout(containerGraficoEstado)
        containerFiltro, self.comboCursoEstado = self._criarFiltroComboBox(
            "Filtrar por Curso:"
        )
        self.comboCursoEstado.currentTextChanged.connect(self._atualizarGraficoEstado)
        self.layoutGraficoEstado = QVBoxLayout()
        layoutContainerEstado.addWidget(containerFiltro)
        layoutContainerEstado.addLayout(self.layoutGraficoEstado)
        layoutGraficos.addWidget(containerGraficoEstado)
        layoutPrincipal.addLayout(layoutGraficos)
        self._popularFiltrosCursos(self.comboCursoEstado)
        self._atualizarGraficoEstado()
        return pagina

    def _atualizarGraficoEstado(self):
        while self.layoutGraficoEstado.count():
            item = self.layoutGraficoEstado.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        cursoSelecionado = self.comboCursoEstado.currentText()
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
        self.layoutGraficoEstado.addWidget(graficoEstado)

    def _criarPaginaGraficoLinha(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)
        headerWidget = self._criarHeaderAnaliseLinha()
        layoutPrincipal.addWidget(headerWidget)
        self.layoutGraficoLinha = QVBoxLayout()
        layoutPrincipal.addLayout(self.layoutGraficoLinha)
        self._popularFiltrosLinha()
        self._atualizarGraficoLinha()
        return pagina

    def _criarHeaderAnaliseLinha(self):
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

    def _criarPaginaGraficoBarra(self):
        pagina = QWidget()
        layoutPrincipal = QVBoxLayout(pagina)

        headerWidget = self._criarHeaderAnaliseBarra()
        layoutPrincipal.addWidget(headerWidget)

        self.layoutGraficoBarra = QVBoxLayout()
        layoutPrincipal.addLayout(self.layoutGraficoBarra)

        self._popularFiltrosBarra()
        self._atualizarGraficoBarra()
        return pagina

    def _criarHeaderAnaliseBarra(self):
        headerWidget = QWidget()
        layoutHeader = QVBoxLayout(headerWidget)
        layoutTitulo = QHBoxLayout()
        rotuloTitulo = QLabel("Análise de Competitividade por Demanda")
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
        containerCurso, self.comboCursoBarra = self._criarFiltroComboBox(
            "Selecione o Curso:"
        )
        self.comboCursoBarra.currentTextChanged.connect(self._atualizarGraficoBarra)
        layoutFiltros.addWidget(containerCurso)
        layoutFiltros.addStretch()
        layoutHeader.addLayout(layoutFiltros)
        return headerWidget

    def _atualizarGraficoBarra(self):
        while self.layoutGraficoBarra.count():
            item = self.layoutGraficoBarra.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cursoSelecionado = self.comboCursoBarra.currentText()
        if not cursoSelecionado:
            return

        alunosDoCurso = self.extratorDeDados.getData(course=cursoSelecionado)

        codigoParaGrupo = {
            codigo: grupo
            for grupo, codigos in self.extratorDeDados.DEMAND_MAP.items()
            for codigo in codigos
            if codigo
        }
        nomesDeExibicao = self._criarNomesDeExibicaoParaDemandas()

        notasPorGrupo = defaultdict(list)
        for aluno in alunosDoCurso:
            demanda = aluno.get("concorrencia", "N/A").upper()
            notaStr = aluno.get("nota", "N/A").replace(",", ".")

            if demanda and demanda in codigoParaGrupo and notaStr != "N/A":
                grupo = codigoParaGrupo[demanda]
                try:
                    notasPorGrupo[grupo].append(float(notaStr))
                except ValueError:
                    continue

        dadosParaGrafico = {}
        for grupo, notas in notasPorGrupo.items():
            if notas:
                nomeDeExibicao = nomesDeExibicao.get(grupo, grupo)
                if nomeDeExibicao:
                    dadosParaGrafico[nomeDeExibicao] = min(notas)

        widgetGrafico = self.geradorDeGraficos.criarGraficoDeBarra(
            dados=dadosParaGrafico, titulo=cursoSelecionado
        )
        self.layoutGraficoBarra.addWidget(widgetGrafico)

    def _criarFiltroComboBox(self, textoRotulo):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(QLabel(textoRotulo))
        comboBox = QComboBox()
        comboBox.setMinimumWidth(300)
        layout.addWidget(comboBox)
        return container, comboBox

    def _popularFiltrosCursos(self, comboBox):
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]

        dadosBrutosCursos = sorted(
            {s.get("curso", "") for s in todosOsAlunos if s.get("curso", "")}
        )

        cursos = [s for s in dadosBrutosCursos if not re.search(r"\d", s)]
        comboBox.addItems(cursos)

    def _popularFiltrosLinha(self):
        self._popularFiltrosCursos(self.comboCursoLinha)
        todosOsAlunos = [
            aluno
            for listaAnual in self.extratorDeDados.data.values()
            for aluno in listaAnual
        ]
        demandas = sorted(
            {
                s.get("concorrencia", "")
                for s in todosOsAlunos
                if s.get("concorrencia", "")
            }
        )
        self.comboDemandaLinha.addItems(demandas)

    def _popularFiltrosBarra(self):
        self._popularFiltrosCursos(self.comboCursoBarra)

    def _criarNomesDeExibicaoParaDemandas(self):
        mapa = {}
        for grupo, codigos in self.extratorDeDados.DEMAND_MAP.items():
            if grupo == "ampla_concorrencia":
                mapa[grupo] = "AC"
                continue

            prioridade = [
                c for c in codigos if "_" in c or c.startswith("V") or c == "L14"
            ]

            if prioridade:
                mapa[grupo] = prioridade[0]
            elif codigos:
                mapa[grupo] = sorted(list(codigos))[0]
            else:
                mapa[grupo] = grupo
        return mapa

    def _extrairAnoDaInscricao(self, inscricao):
        if inscricao and len(inscricao) >= 4:
            primeirosDigitos = inscricao[:2]
            if primeirosDigitos.isdigit():
                return "20" + primeirosDigitos
        return None
