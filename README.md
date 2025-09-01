https://github.com/felipscarvalho/avaliacao-poo.git

## Análise de Dados do SISU - Projeto POO (2025.1 - T02)
- Felipe Carvalho Leal
- Eduardo Curcino Monteiro Filho
## Funcionalidades
- Gráfico em barras para representação da nota média de cada curso por ano.
- Gráfico em linha para representação da nota média por cota em um curso ao longo dos anos;
- Gráfico em pizza para representação da proporção de aprovados em cada intervalo de notas por ano;
- Tabela para visualização geral dos dados;
- Tela home com dados básicos.
## Como rodar em Java
Versão do Java: jdk24.0.2

Entre na pasta java do projeto e execute (É necessário ter o Maven instalado):

```shell
mvn clean javafx:run
```
## Como rodar em Python
Versão do Python: 3.13.7

Entre na pasta Python do projeto e execute:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Main.py
```

## Diferenças entre Java e Python na implementação do Paradigma de Orientação a Objetos
- **Encapsulamento**: em Python o encapsulamento é mais fraco. Ele se dá por convenção: prefixar um atributo com `_` indica que é "protegido", enquanto `__` ativa o *name mangling* (transforma `__attr` em `_Classe__attr`), dificultando o acesso externo, mas não impedindo. Em Java, modificadores como `private`, `protected` e `public` impõem restrições reais em nível de compilador.
- **Sobrecarga de métodos**: Python não suporta *method overloading* nativo (mesmo nome de função com assinaturas diferentes). Em vez disso, usa parâmetros opcionais, `*args` e `**kwargs` para flexibilizar chamadas. Já em Java, sobrecarga de métodos é parte essencial do idioma.
- **Static e Final**: em Python não existem palavras-chave como `static` ou `final`. A linguagem resolve tudo em tempo de execução e permite reatribuição de atributos/métodos. Java, por outro lado, usa `static` para membros de classe e `final` para impedir herança ou reatribuição.
- **Tudo é objeto**: em Python, até inteiros, booleanos e funções são objetos. Isso permite chamadas como:
  ```python
  (5).bit_length()   # retorna número de bits necessários para representar 5
  (10).to_bytes(2, 'big')  # converte inteiro para bytes
  True.__str__()     # retorna "True"
