package com.poo.java;

class Student {
    private String numeroEnem;
    private String nome;
    private String curso;
    private String campus;
    private String demanda;
    private double media;
    private String colocacao;
    private String estado;
    private int ano;
    
    public Student(String numeroEnem, String nome, String curso, String campus, String demanda, double media, String colocacao, String estado, int ano) {
        this.numeroEnem = numeroEnem;
        this.nome = nome;
        this.curso = curso;
        this.campus = campus;
        this.demanda = demanda;
        this.media = media;
        this.colocacao = colocacao;
        this.estado = estado;
        this.ano = ano;
    }
    
    public String getNumeroEnem() { return numeroEnem; }
    public String getNome() { return nome; }
    public String getCurso() { return curso; }
    public String getCampus() { return campus; }
    public String getDemanda() { return demanda; }
    public Double getMedia() { return media; }
    public String getColocacao() { return colocacao; }
    public String getEstado() { return estado; }
    public Integer getAno() { return ano; } 
    
    @Override
    public String toString() {
        return String.format("Student{enem='%s', nome='%s', curso='%s', campus='%s', demanda='%s', media=%.2f, colocacao='%s', estado='%s', ano=%d}", numeroEnem, nome, curso, campus, demanda, media, colocacao, estado, ano);
    }
}