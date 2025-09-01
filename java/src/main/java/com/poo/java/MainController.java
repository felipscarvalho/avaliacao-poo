package com.poo.java;

import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;

public class MainController implements Initializable {
    @FXML private Label totalAprovadosLabel;
    @FXML private Label mediaGeralLabel;
    
    ChartDataInitializer chartDataInitializer = new ChartDataInitializer();
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        carregarDados();
        carregarMediaGeral();
    }    
    
    private void carregarDados() {
        carregarTotal();
    }
    
    private void carregarTotal() {
        Integer totalStudents = chartDataInitializer.getStudents().size();
        
        totalAprovadosLabel.setText(totalStudents.toString());
    }
    
    private void carregarMediaGeral() {
        List<Student> students = chartDataInitializer.getStudents();
        Double totalNotas = 0.0;
        
        for (Student student: students) {
            totalNotas = totalNotas + student.getMedia();
        }
        
        Double media = totalNotas / students.size();
        
        mediaGeralLabel.setText(String.format("%.1f%%", media));
    }
}
