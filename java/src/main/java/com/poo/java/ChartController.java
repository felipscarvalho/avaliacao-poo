package com.poo.java;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.chart.*;
import javafx.scene.control.ComboBox;
import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;

public class ChartController implements Initializable {
    @FXML private BarChart<String, Number> cursoBarChart;
    @FXML private CategoryAxis cursoXAxis;
    @FXML private NumberAxis cursoYAxis;
    
    @FXML private LineChart<String, Number> notaCursoLineChart;
    @FXML private CategoryAxis notaCursoXAxis;
    @FXML private NumberAxis notaCursoYAxis;
    
    @FXML private PieChart notasPieChart;
    
    @FXML private AreaChart<String, Number> demandAreaChart;
    @FXML private CategoryAxis demandXAxis;
    @FXML private NumberAxis demandYAxis;
    
    @FXML private ComboBox<String> seletorAno;
    @FXML private ComboBox<String> seletorAno2;
    @FXML private ComboBox<String> seletorCurso;
    
    private Integer anoSelecionado = 2025;
    private Integer anoSelecionado2 = 2025;
    private String cursoSelecionado;
    ChartDataInitializer chartDataInitializer = new ChartDataInitializer();
    
    @Override
    public void initialize(URL location, ResourceBundle resources) {
        setupSeletores();
        setupCharts();
        carregarDados();
    }
    
    private void setupSeletores() {
        List<String> listaCursos = chartDataInitializer.listarCursos();
        
        seletorAno.setItems(FXCollections.observableArrayList(
            "2020", "2021", "2022", "2023", "2024", "2025"
        ));
        seletorAno.getSelectionModel().select(anoSelecionado.toString());
        
        seletorAno2.setItems(FXCollections.observableArrayList(
            "2020", "2021", "2022", "2023", "2024", "2025"
        ));
        seletorAno2.getSelectionModel().select(anoSelecionado2.toString());
        
        seletorCurso.setItems(FXCollections.observableArrayList(listaCursos));
    }
    
    private void setupCharts() {
        // Configurar labels dos eixos
        cursoXAxis.setLabel("Cursos");
        cursoYAxis.setLabel("Número de Estudantes");
        
        notaCursoXAxis.setLabel("Ano");
        notaCursoYAxis.setLabel("Média");
        
        demandXAxis.setLabel("Ano");
        demandYAxis.setLabel("Demanda");
        
        // Configurar propriedades dos gráficos
        cursoBarChart.setLegendVisible(false);
        notasPieChart.setLegendVisible(true);
        notaCursoLineChart.setCreateSymbols(true);
        demandAreaChart.setCreateSymbols(false);
    }
    
    private void carregarDados() {
        carregarCursoBarChartData();
        carregarNotasPieChartData();
        carregarNotaCursoLineChartData();
        loadAreaChartData();
    }
    
    private void carregarCursoBarChartData() {
        cursoBarChart.getData().clear();
        
        XYChart.Series<String, Number> dados = chartDataInitializer.prepararDadosCursoBarChart(anoSelecionado);
        
        cursoBarChart.getData().add(dados);
    }
    
    private void carregarNotaCursoLineChartData() {
        notaCursoLineChart.getData().clear();
        
        List<XYChart.Series<String, Number>> dados = chartDataInitializer.prepararNotaCursoLineChart(cursoSelecionado);
        
        dados.forEach(dado -> {
            notaCursoLineChart.getData().add(dado);
        });
    }
    
    private void carregarNotasPieChartData() {
        notasPieChart.getData().clear();
        
        ObservableList<PieChart.Data> dados = chartDataInitializer.prepararDadosNotasPieChart(anoSelecionado2);
        
        // Calcula porcentagens
        double total = dados.stream().mapToDouble(PieChart.Data::getPieValue).sum();
    
        dados.forEach(data -> {
            double percentage = (data.getPieValue() / total) * 100;
            data.setName(data.getName() + String.format(" (%.1f%%)", percentage));
        });

        notasPieChart.setData(dados);
    }
    
    private void loadAreaChartData() {
        XYChart.Series<String, Number> engenharia = new XYChart.Series<>();
        engenharia.setName("Engenharia");
        engenharia.getData().addAll(
            new XYChart.Data<>("2020", 120),
            new XYChart.Data<>("2021", 135),
            new XYChart.Data<>("2022", 150),
            new XYChart.Data<>("2023", 145),
            new XYChart.Data<>("2024", 160)
        );
        
        XYChart.Series<String, Number> medicina = new XYChart.Series<>();
        medicina.setName("Medicina");
        medicina.getData().addAll(
            new XYChart.Data<>("2020", 100),
            new XYChart.Data<>("2021", 110),
            new XYChart.Data<>("2022", 120),
            new XYChart.Data<>("2023", 115),
            new XYChart.Data<>("2024", 125)
        );
        
        demandAreaChart.getData().addAll(engenharia, medicina);
    }
    
    @FXML
    private void recarregarGraficoNotaMedia() {
        anoSelecionado = Integer.parseInt(seletorAno.getValue());
        
        carregarCursoBarChartData();
    }
    
    @FXML
    private void recarregarGraficoCurso() {
        cursoSelecionado = seletorCurso.getValue();
        
        carregarNotaCursoLineChartData();
    }
    
    @FXML
    private void recarregarGraficoNota() {
        anoSelecionado2 = Integer.parseInt(seletorAno2.getValue());
        
        carregarNotasPieChartData();
    }
}