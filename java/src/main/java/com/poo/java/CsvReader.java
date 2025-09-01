package com.poo.java;

import java.io.*;   
import java.util.*;

public class CsvReader {
    private Map<String, String> mapCotas;
    
    public List<Student> lerArquivoCSV(String nomeArquivo) {
        List<Student> students = new ArrayList<>();
        setMapCotas();
        
        try {
            BufferedReader br = new BufferedReader(new FileReader(nomeArquivo));
            
            boolean primeiraLinha = true;
            int numeroLinha = 0;
            String linha;
            
            while ((linha = br.readLine()) != null) {
                numeroLinha++;
                
                // Pula o cabeçalho
                if (primeiraLinha) {
                    primeiraLinha = false;
                    continue;
                }
                
                try {
                    Student student = parsearLinha(linha);
                    
                    if (student != null) {
                        students.add(student);
                    }
                } catch (Exception e) {
                    System.err.println("Erro ao processar linha " + numeroLinha + ": " + linha);
                    System.err.println("Erro: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Erro ao ler arquivo: " + e.getMessage());
        }
        
        return students;
    }
    
    private Student parsearLinha(String linha) {
        String[] campos = separarCampos(linha);
        
        if (campos.length < 9) {
            System.err.println("Linha com campos insuficientes: " + linha);
            return null;
        }
        
        try {
            
            // Define os valores usando setters
            String numeroEnem = campos[0].trim();
            String nome = campos[1].trim();
            String curso = campos[2].trim();
            String campus = campos[3].trim();
            String demanda = campos[4].trim();
            double media = Double.parseDouble(campos[5].trim().replace(",", "."));
            String colocacao = campos[6].trim();
            String estado = campos[7].trim();
            int ano = Integer.parseInt(campos[8].trim());
            
            demanda = mapCotas.get(demanda);          
            
            Student student = new Student(numeroEnem, nome, curso, campus, demanda, media, colocacao, estado, ano);
            
            return student;
            
        } catch (NumberFormatException e) {
            System.err.println("Erro ao converter números na linha: " + linha);
            return null;
        }
    }
    
    private String[] separarCampos(String linha) {
        List<String> campos = new ArrayList<>();
        String[] camposLinha = linha.split(",");
        
        for(String campo : camposLinha) {
            campos.add(campo.toString());
        }
        
        return campos.toArray(new String[0]);
    }
    
    private void setMapCotas() {
        mapCotas = new HashMap<>();
        
        mapCotas.put("A0", "Ampla Concorrência");
        mapCotas.put("AC", "Ampla Concorrência");
        
        mapCotas.put("L1", "Escola pública, baixa renda");
        mapCotas.put("LB_EP", "Escola pública, baixa renda");
        
        mapCotas.put("L2", "Escola pública, baixa renda, PPI");
        mapCotas.put("LB_PPI", "Escola pública, baixa renda, PPI");
        
        mapCotas.put("L5", "Escola pública, independente da renda");
        mapCotas.put("LI_EP", "Escola pública, independente da renda");
        
        mapCotas.put("L6", "Escola pública, PPI, independente da renda");
        mapCotas.put("LI_PPI", "Escola pública, PPI, independente da renda");
        
        mapCotas.put("L9", "Escola pública, baixa renda, PcD");
        mapCotas.put("LB_PCD", "Escola pública, baixa renda, PcD");
        
        mapCotas.put("L10", "Escola pública, baixa renda, PcD, PPI");
        
        mapCotas.put("L13", "Escola pública, PcD, independente da renda");
        mapCotas.put("LI_PCD", "Escola pública, PcD, independente da renda");
        
        mapCotas.put("L14", "Escola pública, PcD, PPI, independente da renda");
        
        mapCotas.put("V1751", "PcD");
        mapCotas.put("V3062", "PcD");
        mapCotas.put("V4061", "PcD");
        mapCotas.put("V6071", "PcD");
        mapCotas.put("V7825", "PcD");
        mapCotas.put("V", "PcD");
        
        mapCotas.put("LI_Q", "Escola pública, quilombola, independente da renda");
        
        mapCotas.put("LB_Q", "Escola pública, quilombola, baixa renda");
    }
}