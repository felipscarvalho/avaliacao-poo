from PyQt6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
    QPieSeries,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
)
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class GeradorDeGraficos:
    def criarGraficoDeLinhaMultiplasSeries(
        self, dadosSeries, titulo, eixoXTitulo, eixoYTitulo
    ):
        chart = QChart()
        chart.setTitle(f"Evolução da Nota Média para o curso de {titulo}")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        for nomeSerie, dadosPontos in dadosSeries.items():
            series = QLineSeries()
            series.setName(nomeSerie)
            if dadosPontos:
                for x, y in sorted(dadosPontos.items()):
                    series.append(float(x), float(y))
                chart.addSeries(series)

        chart.createDefaultAxes()
        if chart.axes(Qt.Orientation.Horizontal):
            axisX = chart.axes(Qt.Orientation.Horizontal)[0]
            axisX.setTitleText(eixoXTitulo)
            axisX.setLabelFormat("%d")
        if chart.axes(Qt.Orientation.Vertical):
            chart.axes(Qt.Orientation.Vertical)[0].setTitleText(eixoYTitulo)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chartView

    def criarGraficoDeBarraNotaMediaPorCurso(self, dados, titulo):
        series = QBarSeries()
        barSet = QBarSet("Nota Média Geral Por Curso")

        cursosOrdenados = sorted(dados.items(), key=lambda item: item[1], reverse=True)
        categorias = [curso[0] for curso in cursosOrdenados]
        notas = [media for curso, media in cursosOrdenados]
        barSet.append(notas)
        series.append(barSet)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(titulo)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()

        axisX = QBarCategoryAxis()
        axisX.append(categorias)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Nota Média")
        if dados:
            min_val = min(dados.values()) if dados.values() else 0
            max_val = max(dados.values()) if dados.values() else 0
            if min_val != max_val:
                axisY.setRange(min_val * 0.98, max_val * 1.02)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        if chartView.chart().axes(Qt.Orientation.Horizontal):
            chartView.chart().axes(Qt.Orientation.Horizontal)[0].setLabelsAngle(-45)
        return chartView

    def criarGraficoPizzaDistribuicaoNotas(self, dados, titulo):
        series = QPieSeries()
        series.setHoleSize(0.35)

        for faixa, contagem in dados.items():
            if contagem > 0:
                series.append(f"{faixa} ({contagem})", contagem)

        series.setLabelsVisible(True)

        for fatia in series.slices():
            rotuloOriginal = fatia.label()

            nomeDaFaixa = rotuloOriginal.split(" (")[0]

            porcentagem = f"{fatia.percentage() * 100:.1f}%"

            fatia.setLabel(f"{nomeDaFaixa}\n{porcentagem}")

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(titulo)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chartView
