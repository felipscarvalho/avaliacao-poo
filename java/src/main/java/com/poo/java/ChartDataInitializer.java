package com.poo.java;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.chart.PieChart;
import javafx.scene.chart.XYChart;

public class ChartDataInitializer {
    private List<Student> students;
    
    public ChartDataInitializer() {
        CsvReader csvReader = new CsvReader();
        students = csvReader.lerArquivoCSV("src/main/resources/dados.csv");
    }
    
    public List<Student> getStudents() {
        return students;
    }
    
    private List<Student> separarDadosPorAno(int ano){
        List<Student> anoXStudents = new ArrayList<>();
        
        for(Student student : students) {
            if (student.getAno() == ano) {
                anoXStudents.add(student);
            }
        }
        
        return anoXStudents;
    }
    
    private Map<String, Double> separarMediasPorCurso(int ano) {
        List<Student> dadosStudents = separarDadosPorAno(ano);
        Map<String, Integer> alunosPorCurso = new HashMap<>();
        Map<String, Double> notaTotalPorCurso = new HashMap<>();
        Map<String, Double> notaMediaPorCurso = new HashMap<>();
        
        for(Student student : dadosStudents) {
            if(alunosPorCurso.containsKey(student.getCurso())){
                alunosPorCurso.put(student.getCurso(), alunosPorCurso.get(student.getCurso()) + 1);
                notaTotalPorCurso.put(student.getCurso(), notaTotalPorCurso.get(student.getCurso()) + student.getMedia());
            } else {
                alunosPorCurso.put(student.getCurso(), 1);
                notaTotalPorCurso.put(student.getCurso(), student.getMedia());
            }
        }
        
        Set<String> keys = alunosPorCurso.keySet();
        
        for(String key : keys) {
            notaMediaPorCurso.put(key, notaTotalPorCurso.get(key) / alunosPorCurso.get(key));
        }
        
        return notaMediaPorCurso;
    }
    
    private Map<String, Map<Integer, Double>> separarNotaCursoAno(String curso) {
        Map<String, Map<Integer, Double>> mediasPorCotaCursoAno = new HashMap<>();
        Map<String, Map<Integer, Integer>> alunosPorCotaAno = new HashMap<>();
        Map<String, Map<Integer, Double>> notaTotalPorCotaAno = new HashMap<>();
        
        for(Student student : students) {
            if (!student.getCurso().equals(curso)) {
                continue;
            }
            
            String demanda = student.getDemanda();
            Map<Integer, Integer> anosMap1 = alunosPorCotaAno.get(demanda);
            Map<Integer, Double> anosMap2 = notaTotalPorCotaAno.get(demanda);
            
            if(alunosPorCotaAno.containsKey(demanda)){
                if(anosMap1.containsKey(student.getAno())) {
                    anosMap1.put(student.getAno(), anosMap1.get(student.getAno()) + 1);
                } else {
                    anosMap1.put(student.getAno(), 1);
                }
                
                alunosPorCotaAno.put(demanda, anosMap1);
            } else {
                alunosPorCotaAno.put(demanda, new HashMap<>(){{put(student.getAno(), 1);}});
            }
            
            if(notaTotalPorCotaAno.containsKey(demanda)){
                if(anosMap2.containsKey(student.getAno())) {
                    anosMap2.put(student.getAno(), anosMap2.get(student.getAno()) + student.getMedia());
                } else {
                    anosMap2.put(student.getAno(), student.getMedia());
                }
                
                notaTotalPorCotaAno.put(demanda, anosMap2);
            } else {
                notaTotalPorCotaAno.put(demanda, new HashMap<>(){{put(student.getAno(), student.getMedia());}});
            }
        }
        
        Set<String> cotas = alunosPorCotaAno.keySet();
        
        
        for (String cota : cotas) {
            Map<Integer, Integer> anosAlunos = alunosPorCotaAno.get(cota);
            Map<Integer, Double> anosNotas = notaTotalPorCotaAno.get(cota);
            Set<Integer> anos = anosAlunos.keySet();
        
            Map<Integer, Double> mediasAno = new HashMap<>();
        
            for (Integer ano : anos) {
                int numeroAlunos = anosAlunos.get(ano);
                Double notaTotal = anosNotas.get(ano);
            
                if (notaTotal != null && numeroAlunos > 0) {
                    double media = notaTotal / numeroAlunos;
                    mediasAno.put(ano, media);
                }
            }
        
            mediasPorCotaCursoAno.put(cota, mediasAno);
        }
        
        return mediasPorCotaCursoAno;
    }
    
    private Map<String, Double> separarIntervaloNota(int ano) {
        List<Student> dadosStudents = separarDadosPorAno(ano);
        List<String> intervalos = new ArrayList<>(List.of("401-500", "501-600", "601-700", "701-800", "801-900"));
        Map<String, Integer> alunosPorIntervaloNotas = new HashMap<>();
        Map<String, Double> totalNotasPorIntervaloNotas = new HashMap<>();
        Map<String, Double> mediasPorIntervaloNotas = new HashMap<>();
        
        
        
        for(Student student : dadosStudents) {
            double media = student.getMedia();
            
            for (String intervalo : intervalos) {
                String[] range = intervalo.split("-");
                int min = Integer.parseInt(range[0]);
                int max = Integer.parseInt(range[1]);
                
                if (media > min && media < max){
                    if(alunosPorIntervaloNotas.containsKey(intervalo)){
                        alunosPorIntervaloNotas.put(intervalo, alunosPorIntervaloNotas.get(intervalo) + 1);
                        totalNotasPorIntervaloNotas.put(intervalo, totalNotasPorIntervaloNotas.get(intervalo) + student.getMedia());
                    } else {
                        alunosPorIntervaloNotas.put(intervalo, 1);
                        totalNotasPorIntervaloNotas.put(intervalo, student.getMedia());
                    }
                }
            }
        }
        
        for (String intervalo : intervalos) {
            mediasPorIntervaloNotas.put(intervalo, totalNotasPorIntervaloNotas.get(intervalo) / alunosPorIntervaloNotas.get(intervalo));
        }
        
        return mediasPorIntervaloNotas;
    }
    
    public List<String> listarCursos() {
        List<String> cursos = new ArrayList<>();
        
        for (Student student: students) {
            if (!cursos.contains(student.getCurso())){
                cursos.add(student.getCurso());
            }
        }
    
        return cursos;
    }
    
    public XYChart.Series<String, Number> prepararDadosCursoBarChart(int ano) {
        Map<String, Double> dadosStudents = separarMediasPorCurso(ano);
        XYChart.Series<String, Number> dadosBarChart = new XYChart.Series<>();       
        
        dadosStudents.forEach((curso, alunos) -> {
            dadosBarChart.getData().add(new XYChart.Data<>(curso, alunos));
        });
        
        return dadosBarChart;
    }
    
    public List<XYChart.Series<String, Number>> prepararNotaCursoLineChart(String curso) {
        Map<String, Map<Integer, Double>> dadosStudents = separarNotaCursoAno(curso);
        List<XYChart.Series<String, Number>> dadosBarChart = new ArrayList<>();       
        
        Set<String> keys = dadosStudents.keySet();
        
        for(String key: keys) {
            XYChart.Series<String, Number> series = new XYChart.Series<>();
            Map<Integer, Double> dados = dadosStudents.get(key);
            series.setName(key);
            
            dados.forEach((_ano, quantia) -> {
                series.getData().add(new XYChart.Data<>(_ano.toString(), quantia));
            });
            
            dadosBarChart.add(series);
        }
        
        return dadosBarChart;
    }
    
    public ObservableList<PieChart.Data> prepararDadosNotasPieChart(int ano) {
        Map<String, Double> dadosStudents = separarIntervaloNota(ano);
        ObservableList<PieChart.Data> dadosPieChart = FXCollections.observableArrayList();       
        
        dadosStudents.forEach((curso, alunos) -> {
            dadosPieChart.add(new PieChart.Data(curso, alunos));
        });
        
        return dadosPieChart;
    }
}
