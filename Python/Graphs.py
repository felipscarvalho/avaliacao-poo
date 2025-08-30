from PyQt6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
)
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class GeradorDeGraficos:
    def criarGraficoDeLinha(self, dados, titulo, subtitulo, eixoXTitulo, eixoYTitulo):
        series = QLineSeries()
        if dados:
            for x, y in sorted(dados.items()):
                series.append(float(x), float(y))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"{titulo}<br/><font size='-1'><i>{subtitulo}</i></font>")
        chart.legend().hide()

        axisX = QValueAxis()
        axisX.setLabelFormat("%d")
        axisX.setTitleText(eixoXTitulo)
        if dados:
            axisX.setTickCount(len(dados) or 2)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText(eixoYTitulo)
        if dados:
            min_val = min(dados.values())
            max_val = max(dados.values())
            axisY.setRange(min_val * 0.98, max_val * 1.02)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chartView
