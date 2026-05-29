# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 3 · RAG (Retrieval-Augmented Generation)
# MAGIC
# MAGIC **Objetivo:** construir um assistente que responde perguntas sobre **provas anteriores**
# MAGIC (12 PDFs reais de disciplinas), buscando os trechos relevantes com **Vector Search** e
# MAGIC gerando a resposta com um LLM.
# MAGIC
# MAGIC **Pré-requisito:** rode o notebook `00_gerar_dados` antes deste (ele sobe os PDFs ao Volume).
# MAGIC
# MAGIC Este notebook já faz a **ingestão dos PDFs** (parsing → tabela de trechos).
# MAGIC Você constrói o índice de busca + geração com o **Databricks Assistant** (células 🧞 **SUA VEZ**).
# MAGIC
# MAGIC > ⏱️ **Comece pela célula 2 logo no início:** criar o Vector Search endpoint leva ~10 min.
# MAGIC > Dispare a criação, e enquanto ele sobe você avança no resto.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
dbutils.widgets.text("schema", "sistema_academico", "Schema")
CATALOG = dbutils.widgets.get("catalog")
SCHEMA  = dbutils.widgets.get("schema")
EXAMS   = f"/Volumes/{CATALOG}/{SCHEMA}/staging/exams/"
spark.sql(f"USE {CATALOG}.{SCHEMA}")
print(f"Usando {CATALOG}.{SCHEMA}")
display(dbutils.fs.ls(EXAMS))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Ingestão dos PDFs (FUNCIONAL) — parsing com `ai_parse_document`
# MAGIC Lemos os PDFs binários, extraímos o texto com a função de IA nativa do Databricks
# MAGIC e gravamos uma linha por prova na tabela `exam_chunks`. Esta é a "matéria-prima" do RAG.
# MAGIC O índice de Vector Search precisa de **Change Data Feed** ligado, então já habilitamos aqui.

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE exam_chunks AS
WITH parsed AS (
  SELECT
    regexp_extract(path, '([^/]+)\\\\.pdf$', 1) AS exam_filename,
    path,
    CAST(ai_parse_document(content, map('mode', 'TEXT')) AS STRING) AS raw_json
  FROM read_files('{EXAMS}', format => 'binaryFile')
),
extracted AS (
  SELECT exam_filename, path,
    concat_ws('\\n\\n', transform(
      from_json(raw_json, 'document STRUCT<elements ARRAY<STRUCT<content STRING, type STRING>>>').document.elements,
      x -> x.content
    )) AS full_text
  FROM parsed
)
SELECT monotonically_increasing_id() AS chunk_id, exam_filename, full_text AS chunk
FROM extracted WHERE length(full_text) > 50
""")

# Vector Search (Delta Sync Index) exige Change Data Feed
spark.sql("ALTER TABLE exam_chunks SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
print("✅ exam_chunks criada")

# COMMAND ----------

display(spark.sql("SELECT exam_filename, length(chunk) AS chars, left(chunk, 300) AS preview FROM exam_chunks ORDER BY exam_filename"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · 🧞 SUA VEZ — Crie o Vector Search endpoint (dispare AGORA, leva ~10 min)
# MAGIC O endpoint é a infra que serve o índice. Crie-o **primeiro** e siga em frente enquanto sobe.
# MAGIC
# MAGIC **Prompt sugerido** (Assistant: ✨ ou `Cmd/Ctrl + I`):
# MAGIC
# MAGIC > _"Usando o pacote `databricks-vectorsearch`, crie um Vector Search endpoint chamado
# MAGIC > `exam-search` do tipo STANDARD, se ele ainda não existir. Não bloqueie esperando ficar
# MAGIC > ONLINE — só dispare a criação e me mostre o status atual."_
# MAGIC
# MAGIC 💡 Você pode acompanhar o status em **Compute → Vector Search** na interface.

# COMMAND ----------

# 👇 gere aqui a criação do endpoint


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — Crie o índice (Delta Sync com embeddings gerenciados)
# MAGIC O índice faz o embedding automático da coluna `chunk` e mantém sincronia com a tabela Delta.
# MAGIC
# MAGIC **Prompt sugerido:**
# MAGIC
# MAGIC > _"No catálogo e schema atuais (variáveis `CATALOG` e `SCHEMA` já definidas neste notebook),
# MAGIC > crie um Delta Sync Index `{CATALOG}.{SCHEMA}.exam_chunks_vs_index` no endpoint `exam-search`,
# MAGIC > a partir da tabela `{CATALOG}.{SCHEMA}.exam_chunks`. Use `chunk_id` como primary key, faça o
# MAGIC > embedding gerenciado da coluna `chunk` com o modelo `databricks-gte-large-en`, e configure
# MAGIC > pipeline_type TRIGGERED. Espere o índice ficar pronto."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · 🧞 SUA VEZ — Busca semântica no índice
# MAGIC
# MAGIC **Prompt sugerido:**
# MAGIC
# MAGIC > _"Escreva uma função `buscar(pergunta, k=3)` que usa o `similarity_search` do índice
# MAGIC > `exam_chunks_vs_index` para retornar os k trechos mais relevantes (colunas
# MAGIC > `exam_filename` e `chunk`). Teste com a pergunta 'tópicos de banco de dados'."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · 🧞 SUA VEZ — Geração da resposta com LLM
# MAGIC
# MAGIC **Prompt sugerido:**
# MAGIC
# MAGIC > _"Escreva uma função `responder(pergunta)` que chama `buscar(pergunta)`, monta um prompt
# MAGIC > com os trechos recuperados como contexto, e gera a resposta em português usando `ai_query`
# MAGIC > com o modelo `databricks-meta-llama-3-3-70b-instruct`. Peça ao modelo para responder apenas
# MAGIC > com base no contexto e citar de qual prova veio a informação."_
# MAGIC
# MAGIC Teste com perguntas como:
# MAGIC - _"Quais tópicos caíram na prova de Banco de Dados?"_
# MAGIC - _"Mostre uma questão de Cálculo 1 sobre derivadas."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Plano B (só se o endpoint demorar demais) — RAG leve sem Vector Search
# MAGIC Se o endpoint não ficar ONLINE a tempo, dá pra fazer a busca sem ele e não travar o exercício:
# MAGIC
# MAGIC > _"Sem usar Vector Search: gere embeddings da coluna `chunk` de `exam_chunks` com `ai_query`
# MAGIC > e o endpoint `databricks-gte-large-en`, salve numa tabela, e reescreva `buscar(pergunta, k=3)`
# MAGIC > usando similaridade de cosseno em Python."_
# MAGIC
# MAGIC O resto (célula 5, geração com LLM) continua igual.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você construiu um pipeline RAG: documentos → parsing → índice Vector Search → busca → resposta com LLM.
# MAGIC **Bônus:** peça ao Assistant para _"criar um app de chat em Gradio que usa a função
# MAGIC `responder`"_ e publique como um **Databricks App**.
