# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 1 · Data Engineering + AI/BI + Genie
# MAGIC
# MAGIC **Objetivo:** transformar os CSVs brutos da universidade em tabelas confiáveis
# MAGIC (arquitetura **Medalhão**: Bronze → Silver → Gold), construir um **dashboard AI/BI**
# MAGIC e um **Genie Space** para perguntar aos dados em português.
# MAGIC
# MAGIC **Pré-requisito:** rode o notebook `00_gerar_dados` antes deste.
# MAGIC
# MAGIC Este notebook te dá um **exemplo funcional de Bronze** para você copiar o padrão.
# MAGIC O resto (Silver, Gold, dashboard, Genie) você constrói com o **Databricks Assistant** —
# MAGIC os prompts sugeridos estão nas células marcadas com 🧞 **SUA VEZ**.

# COMMAND ----------

CATALOG = "workspace"
SCHEMA  = "sistema_academico"
CSV_BASE = f"/Volumes/{CATALOG}/{SCHEMA}/staging/csvs"
spark.sql(f"USE {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0 · Confira a matéria-prima
# MAGIC Os CSVs brutos já estão no Volume. Vamos olhar de onde os dados vêm.

# COMMAND ----------

display(dbutils.fs.ls(CSV_BASE))

# COMMAND ----------

# Espie o CSV bruto de matrículas — é a tabela "transacional" principal
display(
    spark.read.option("header", True).option("inferSchema", True)
    .csv(f"{CSV_BASE}/matriculas")
    .limit(10)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Bronze (EXEMPLO FUNCIONAL) — copie este padrão
# MAGIC Bronze = cópia fiel do dado bruto, só ingerido para dentro de uma tabela Delta governada.
# MAGIC Aqui usamos `read_files` (Auto Loader em modo batch) — a forma moderna de ingerir arquivos no Databricks.

# COMMAND ----------

(
    spark.read.format("csv")
    .option("header", True).option("inferSchema", True)
    .load(f"{CSV_BASE}/matriculas")
    .write.mode("overwrite").saveAsTable("bronze_matriculas")
)
print("✅ bronze_matriculas criada")
display(spark.table("bronze_matriculas").limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · 🧞 SUA VEZ — crie as outras tabelas Bronze
# MAGIC Faltam: `bronze_alunos`, `bronze_disciplinas`, `bronze_cursos`,
# MAGIC `bronze_departamentos`, `bronze_professores`.
# MAGIC
# MAGIC **Abra o Databricks Assistant** (ícone ✨ ou `Cmd/Ctrl + I`) e peça, por exemplo:
# MAGIC
# MAGIC > _"Seguindo exatamente o mesmo padrão da célula que cria `bronze_matriculas` a partir de
# MAGIC > `{CSV_BASE}/matriculas`, gere uma célula para cada um destes CSVs criando as tabelas Bronze
# MAGIC > correspondentes: alunos, disciplinas, cursos, departamentos, professores."_
# MAGIC
# MAGIC 💡 Dica: escreva o código numa célula vazia abaixo e use o Assistant para completar/ajustar.

# COMMAND ----------

# 👇 cole/gere aqui o código das demais tabelas Bronze


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — Silver (limpeza + junção)
# MAGIC Silver = dados limpos e enriquecidos. Queremos uma tabela `silver_matriculas` que junte
# MAGIC matrículas com nome do aluno, disciplina, curso, departamento e professor — e que valide
# MAGIC as notas (0 a 10) e a frequência (0 a 100%).
# MAGIC
# MAGIC **Prompt sugerido para o Assistant:**
# MAGIC
# MAGIC > _"Crie uma tabela Delta `silver_matriculas` em PySpark juntando `bronze_matriculas` com
# MAGIC > `bronze_alunos` (por aluno_id), `bronze_disciplinas` (por disciplina_id),
# MAGIC > `bronze_cursos`, `bronze_departamentos` e `bronze_professores`. Inclua colunas legíveis
# MAGIC > (aluno_nome, disciplina_nome, curso_nome, professor_nome) e duas colunas booleanas
# MAGIC > `aprovado` e `reprovado` derivadas da coluna `situacao`. Descarte linhas com `situacao`
# MAGIC > inválida e me explique cada transformação."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · 🧞 SUA VEZ — Gold (tabelas de negócio)
# MAGIC Gold = tabelas agregadas, prontas para dashboards e ML. Sugestões de prompts:
# MAGIC
# MAGIC > _"A partir de `silver_matriculas`, crie `gold_desempenho_disciplina`: por disciplina e
# MAGIC > semestre, calcule total de alunos, taxa de aprovação (%), nota média, e frequência média."_
# MAGIC
# MAGIC > _"Crie `gold_desempenho_aluno`: por aluno e semestre, média do semestre, nº de aprovações/
# MAGIC > reprovações e o CRA acumulado (média móvel das médias por semestre)."_
# MAGIC
# MAGIC > _"Crie `gold_alunos_em_risco` para o semestre 2026/1: para cada aluno ativo, um
# MAGIC > `score_risco` (0-100) baseado em nota média baixa, frequência baixa e histórico de
# MAGIC > reprovações, e um `nivel_risco` ALTO/MEDIO/BAIXO."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · Dashboard AI/BI (na interface)
# MAGIC 1. Menu lateral → **Dashboards** → **Create dashboard**.
# MAGIC 2. Em **Data**, adicione suas tabelas `gold_*`.
# MAGIC 3. Em **Canvas**, clique em **Add a visualization** e descreva o gráfico em linguagem natural —
# MAGIC    ex.: _"taxa de aprovação média por departamento"_, _"top 10 disciplinas com menor aprovação"_,
# MAGIC    _"distribuição de alunos por nível de risco"_. O AI/BI gera a query e o gráfico.
# MAGIC 4. Monte 1 página com 3-4 visualizações que contem uma história.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 · Genie Space (perguntas em português)
# MAGIC 1. Menu lateral → **Genie** → **New** → selecione suas tabelas `gold_*` (e `silver_matriculas`).
# MAGIC 2. Faça perguntas em português:
# MAGIC    - _"Qual curso tem a maior taxa de reprovação?"_
# MAGIC    - _"Quantos alunos estão em risco ALTO no semestre 2026/1?"_
# MAGIC    - _"Mostre a evolução da nota média de Cálculo 1 ao longo dos semestres."_
# MAGIC 3. Se o Genie errar, adicione **Instructions** e **Example SQL** no Space para ensiná-lo —
# MAGIC    e veja a resposta melhorar. **Esse loop de ensinar o Genie é o aprendizado-chave da trilha.**

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você construiu um pipeline Medalhão completo + dashboard + assistente em linguagem natural.
# MAGIC **Bônus:** transforme as células Bronze/Silver/Gold em um *Lakeflow Declarative Pipeline*
# MAGIC (peça ao Assistant: _"converta estas tabelas em um pipeline declarativo usando @dp.table"_).
