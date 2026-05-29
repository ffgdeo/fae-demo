# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 1 · Data Engineering + AI/BI + Genie
# MAGIC ## (com **Lakeflow Spark Declarative Pipelines**)
# MAGIC
# MAGIC **Objetivo:** transformar os CSVs brutos da universidade em tabelas confiáveis
# MAGIC (arquitetura **Medalhão**: Bronze → Silver → Gold) usando um **pipeline declarativo**,
# MAGIC e depois construir um **dashboard AI/BI** e um **Genie Space**.
# MAGIC
# MAGIC **Pré-requisito:** rode o notebook `00_gerar_dados` antes (ele deixa os CSVs no Volume).

# COMMAND ----------

# MAGIC %md
# MAGIC # 🛑 PARE E LEIA ANTES DE TUDO — configure o Pipeline primeiro
# MAGIC
# MAGIC Este notebook é a **definição de um pipeline declarativo**. Ele **não roda célula a célula**
# MAGIC (se você apertar *Run*, vai dar erro `cannot import name 'pipelines'` — isso é esperado, e
# MAGIC **não** é limitação do Free Edition: `pyspark.pipelines` só existe dentro de um Pipeline).
# MAGIC
# MAGIC ### ➡️ Passo 0 — crie o Pipeline ANTES de escrever ou rodar qualquer código:
# MAGIC 1. Menu lateral → **Jobs & Pipelines** → **Create** → **ETL Pipeline** (Spark Declarative Pipeline).
# MAGIC 2. O editor abre com uma **pasta e um arquivo `.py` vazios** (um exemplo em branco). **Ignore** —
# MAGIC    a gente vai apontar o pipeline para ESTE notebook em vez do arquivo de exemplo.
# MAGIC 3. Abra **Settings** (⚙️ / *Pipeline settings*) e ajuste:
# MAGIC    - **Root folder:** aponte para a pasta deste repositório (onde está a pasta `notebooks/`).
# MAGIC    - **Source code / Paths:** aponte para **ESTE notebook** (`notebooks/track1_dados_aibi_genie`)
# MAGIC      e **remova** o arquivo `.py` de exemplo que veio por padrão.
# MAGIC    - **Default catalog** e **Default schema:** escolha onde as tabelas serão criadas
# MAGIC      (ex.: `workspace` / `sistema_academico` — os mesmos do `00_gerar_dados`).
# MAGIC 4. (Opcional) Se usou catálogo/schema diferente no `00_gerar_dados`, em **Advanced → Configuration**
# MAGIC    adicione `fae.csv_base = /Volumes/<seu_catalogo>/<seu_schema>/staging/csvs`.
# MAGIC 5. **Salve** as settings. Deixe a janela do Pipeline aberta.
# MAGIC
# MAGIC ### Depois disso, o ciclo de trabalho é:
# MAGIC - Você **edita/completa** as definições de tabela aqui (com ajuda do **Databricks Assistant**).
# MAGIC - Volta na tela do Pipeline e clica em **Start** (ou **Validate**) para rodar.
# MAGIC - Vê o **grafo** Bronze → Silver → Gold se materializar e corrige o que precisar.
# MAGIC
# MAGIC > No modelo declarativo você só **descreve as tabelas** (com `@dp.table`); o Databricks
# MAGIC > descobre a ordem, as dependências e a execução incremental por você.

# COMMAND ----------

from pyspark import pipelines as dp
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Caminho da zona raw. Default = schema padrão do 00_gerar_dados.
# Se você usou outro catálogo/schema, adicione nas configs do pipeline:
#   fae.csv_base = /Volumes/<seu_catalogo>/<seu_schema>/staging/csvs
CSV_BASE = spark.conf.get("fae.csv_base", "/Volumes/workspace/sistema_academico/staging/csvs")
SCHEMA_BASE = CSV_BASE.rsplit("/csvs", 1)[0] + "/_schemas"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Dois tipos de tabela no pipeline declarativo
# MAGIC - **Streaming Table** (tabela de streaming): para **ingestão incremental**. A consulta lê de
# MAGIC   uma fonte com `spark.readStream` (ex.: Auto Loader). Processa só o que é novo a cada run.
# MAGIC   → **Use no Bronze.**
# MAGIC - **Materialized View** (visão materializada): resultado de uma consulta **batch** sobre
# MAGIC   outras tabelas; o Databricks recalcula de forma eficiente quando os dados mudam.
# MAGIC   → **Use no Silver e no Gold.**

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Bronze = Streaming Table (EXEMPLO FUNCIONAL) — copie este padrão
# MAGIC Ingestão com **Auto Loader** (`cloudFiles`) via `spark.readStream`. Por ser uma consulta de
# MAGIC streaming, o `@dp.table` materializa isto como uma **streaming table** (ingestão incremental).

# COMMAND ----------

@dp.table(name="bronze_matriculas", comment="Matrículas brutas ingeridas via Auto Loader.")
def bronze_matriculas():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", f"{SCHEMA_BASE}/bronze_matriculas")
        .option("header", True)
        .option("inferSchema", True)
        .load(f"{CSV_BASE}/matriculas")
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · 🧞 SUA VEZ — as outras tabelas Bronze
# MAGIC Faltam: `bronze_alunos`, `bronze_disciplinas`, `bronze_cursos`,
# MAGIC `bronze_departamentos`, `bronze_professores` (os CSVs têm esses mesmos nomes).
# MAGIC
# MAGIC **Prompt para o Assistant** (✨ ou `Cmd/Ctrl + I`):
# MAGIC
# MAGIC > _"Seguindo exatamente o mesmo padrão da função `bronze_matriculas` (decorator `@dp.table`,
# MAGIC > Auto Loader com cloudFiles lendo de `{CSV_BASE}/<nome>` e schemaLocation em
# MAGIC > `{SCHEMA_BASE}/<nome>`), gere uma função `@dp.table` para cada um destes CSVs: alunos,
# MAGIC > disciplinas, cursos, departamentos, professores."_

# COMMAND ----------

# 👇 gere aqui as demais tabelas @dp.table de Bronze


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — Silver = Materialized View (limpeza + junção + qualidade)
# MAGIC Silver = dados limpos e enriquecidos, como uma **materialized view** (consulta batch sobre as
# MAGIC tabelas Bronze). Aproveite as **expectativas de qualidade** (`@dp.expect`) para validar.
# MAGIC
# MAGIC **Prompt sugerido:**
# MAGIC
# MAGIC > _"Crie uma **materialized view** `silver_matriculas` no pipeline declarativo que lê
# MAGIC > `bronze_matriculas` (leitura batch) e junta com `bronze_alunos` (aluno_id),
# MAGIC > `bronze_disciplinas` (disciplina_id), `bronze_cursos`, `bronze_departamentos` e
# MAGIC > `bronze_professores`. Inclua nomes legíveis (aluno_nome, disciplina_nome, curso_nome,
# MAGIC > professor_nome) e colunas booleanas `aprovado`/`reprovado` derivadas de `situacao`.
# MAGIC > Adicione expectativas com `@dp.expect` para nota_p1, nota_p2 (0 a 10) e frequencia_pct
# MAGIC > (0 a 100), e `@dp.expect_or_drop` para descartar situações inválidas."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · 🧞 SUA VEZ — Gold = Materialized Views (tabelas de negócio)
# MAGIC Gold = visões materializadas agregadas, prontas para dashboards/Genie. Sugestões de prompts:
# MAGIC
# MAGIC > _"Crie uma **materialized view** `gold_desempenho_disciplina`: a partir de `silver_matriculas`,
# MAGIC > por disciplina e semestre, calcule total de alunos, taxa de aprovação (%), nota média e
# MAGIC > frequência média."_
# MAGIC
# MAGIC > _"Crie a materialized view `gold_desempenho_aluno`: por aluno e semestre, média do semestre,
# MAGIC > nº de aprovações/reprovações e o CRA acumulado (média móvel com Window)."_
# MAGIC
# MAGIC > _"Crie a materialized view `gold_alunos_em_risco` para o semestre 2026/1: para cada aluno
# MAGIC > ativo, um `score_risco` (0-100) e um `nivel_risco` ALTO/MEDIO/BAIXO."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · Rode o Pipeline (você já o criou no Passo 0)
# MAGIC 1. Volte para a tela do **Pipeline** que você criou no início.
# MAGIC 2. Clique em **Start** (rodar tudo) ou **Validate** (só checar sem materializar).
# MAGIC 3. Acompanhe o **grafo** Bronze → Silver → Gold ficar verde; clique em cada tabela para ver
# MAGIC    contagem de linhas e métricas das expectativas de qualidade.
# MAGIC 4. Deu erro em alguma tabela? Ajuste a definição aqui, salve, e clique em **Start** de novo.
# MAGIC 5. Quando terminar, suas tabelas estarão no catálogo/schema escolhido. 🎉

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 · Dashboard AI/BI (na interface)
# MAGIC 1. Menu lateral → **Dashboards** → **Create dashboard**.
# MAGIC 2. Em **Data**, adicione suas tabelas `gold_*`.
# MAGIC 3. Em **Canvas** → **Add a visualization**, descreva o gráfico em linguagem natural:
# MAGIC    _"taxa de aprovação média por departamento"_, _"top 10 disciplinas com menor aprovação"_,
# MAGIC    _"distribuição de alunos por nível de risco"_. O AI/BI gera a query e o gráfico.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7 · Genie Space (perguntas em português)
# MAGIC 1. Menu lateral → **Genie** → **New** → selecione suas tabelas `gold_*` (e `silver_matriculas`).
# MAGIC 2. Pergunte em português:
# MAGIC    - _"Qual curso tem a maior taxa de reprovação?"_
# MAGIC    - _"Quantos alunos estão em risco ALTO no semestre 2026/1?"_
# MAGIC    - _"Mostre a evolução da nota média de Cálculo 1 ao longo dos semestres."_
# MAGIC 3. Se o Genie errar, adicione **Instructions** e **Example SQL** no Space para ensiná-lo.
# MAGIC    **Esse loop de ensinar o Genie é o aprendizado-chave da trilha.**

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você construiu um pipeline declarativo Bronze→Silver→Gold + dashboard + assistente em
# MAGIC linguagem natural. **Bônus:** ative o **scheduling** do pipeline ou explore o modo
# MAGIC **streaming contínuo** para ingestão em tempo real.
