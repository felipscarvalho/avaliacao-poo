package com.poo.java;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;

public class TableController implements Initializable {
    @FXML private TableView<Student> studentTable;
    @FXML private TableColumn<Student, String> numeroEnemColumn;
    @FXML private TableColumn<Student, String> nomeColumn;
    @FXML private TableColumn<Student, String> cursoColumn;
    @FXML private TableColumn<Student, String> campusColumn;
    @FXML private TableColumn<Student, String> demandaColumn;
    @FXML private TableColumn<Student, Double> mediaColumn;
    @FXML private TableColumn<Student, String> colocacaoColumn;
    @FXML private TableColumn<Student, String> estadoColumn;
    @FXML private TableColumn<Student, Integer> anoColumn;
    
    @Override
    public void initialize(URL location, ResourceBundle resources) {
        setupTableColumns();
        loadData();
    }
    
    private void setupTableColumns() {
        studentTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
        numeroEnemColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getNumeroEnem()));
        nomeColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getNome()));
        cursoColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getCurso()));
        campusColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getCampus()));
        demandaColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getDemanda()));
        mediaColumn.setCellValueFactory(cellData -> new SimpleDoubleProperty(cellData.getValue().getMedia()).asObject());
        colocacaoColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getColocacao()));
        estadoColumn.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getEstado()));
        anoColumn.setCellValueFactory(cellData -> new SimpleIntegerProperty(cellData.getValue().getAno()).asObject());
    }
    
    private void loadData() {
        CsvReader csvReader = new CsvReader();
        List<Student> students = csvReader.lerArquivoCSV("src/main/resources/dados.csv");
        ObservableList<Student> studentList = FXCollections.observableArrayList(students);
        studentTable.setItems(studentList);
    }
}