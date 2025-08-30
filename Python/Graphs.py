from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QPieSeries
from PyQt6.QtGui import QPainter, QFont
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
            if min(dados.values()) != max(dados.values()):
                axisY.setRange(min(dados.values()) * 0.98, max(dados.values()) * 1.02)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chartView

    def criarGraficoDePizza(self, dados, titulo):
        series = QPieSeries()
        total = sum(dados.values())

        outros_valor = 0
        itens_ordenados = sorted(dados.items(), key=lambda item: item[1], reverse=True)

        for rotulo, valor in itens_ordenados:
            porcentagem = (valor / total) * 100 if total > 0 else 0
            if porcentagem < 2.0 and len(dados) > 7:
                outros_valor += valor
            else:
                fatia = series.append(rotulo, valor)
                fatia.setLabel(
                    f"{rotulo}\n{porcentagem:.1f}%"
                )  # Exibe nome e porcentagem
                fatia.setLabelVisible()

        if outros_valor > 0:
            porcentagem_outros = (outros_valor / total) * 100 if total > 0 else 0
            fatia = series.append(f"Outros ({outros_valor})", outros_valor)
            fatia.setLabel(f"Outros\n{porcentagem_outros:.1f}%")
            fatia.setLabelVisible()

        if series.slices():
            series.slices()[0].setExploded(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(titulo)
        chart.setTitleFont(QFont("Arial", 16, QFont.Weight.Bold))
        chart.legend().setVisible(False)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chartView
