# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 3 · RAG (Retrieval-Augmented Generation)
# MAGIC
# MAGIC **Objetivo:** construir um assistente que responde perguntas sobre **provas anteriores**
# MAGIC (12 PDFs reais de disciplinas), buscando os trechos relevantes e gerando a resposta com um LLM.
# MAGIC
# MAGIC **Pré-requisito:** rode o notebook `00_gerar_dados` antes deste (ele sobe os PDFs ao Volume).
# MAGIC
# MAGIC Este notebook já faz a **ingestão dos PDFs** (parsing → tabela de trechos).
# MAGIC Você constrói a busca + geração com o **Databricks Assistant** (células 🧞 **SUA VEZ**).

# COMMAND ----------

CATALOG = "workspace"
SCHEMA  = "sistema_academico"
EXAMS   = f"/Volumes/{CATALOG}/{SCHEMA}/staging/exams/"
spark.sql(f"USE {CATALOG}.{SCHEMA}")
display(dbutils.fs.ls(EXAMS))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Ingestão dos PDFs (FUNCIONAL) — parsing com `ai_parse_document`
# MAGIC Lemos os PDFs binários, extraímos o texto com a função de IA nativa do Databricks
# MAGIC e gravamos uma linha por prova na tabela `exam_chunks`. Esta é a "matéria-prima" do RAG.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE exam_chunks AS
# MAGIC WITH parsed AS (
# MAGIC   SELECT
# MAGIC     regexp_extract(path, '([^/]+)\\.pdf$', 1) AS exam_filename,
# MAGIC     path,
# MAGIC     CAST(ai_parse_document(content, map('mode', 'TEXT')) AS STRING) AS raw_json
# MAGIC   FROM read_files('/Volumes/workspace/sistema_academico/staging/exams/', format => 'binaryFile')
# MAGIC ),
# MAGIC extracted AS (
# MAGIC   SELECT exam_filename, path,
# MAGIC     concat_ws('\n\n', transform(
# MAGIC       from_json(raw_json, 'document STRUCT<elements ARRAY<STRUCT<content STRING, type STRING>>>').document.elements,
# MAGIC       x -> x.content
# MAGIC     )) AS full_text
# MAGIC   FROM parsed
# MAGIC )
# MAGIC SELECT monotonically_increasing_id() AS chunk_id, exam_filename, full_text AS chunk
# MAGIC FROM extracted WHERE length(full_text) > 50;

# COMMAND ----------

display(spark.sql("SELECT exam_filename, length(chunk) AS chars, left(chunk, 300) AS preview FROM exam_chunks ORDER BY exam_filename"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · 🧞 SUA VEZ — Caminho A (recomendado p/ workshop): RAG leve com embeddings em tabela
# MAGIC Rápido e sem depender de criar um endpoint de Vector Search (que demora ~10 min no Free Edition).
# MAGIC
# MAGIC **Prompts sugeridos** (Assistant: ✨ ou `Cmd/Ctrl + I`):
# MAGIC
# MAGIC > _"Para cada linha de `exam_chunks`, gere o embedding da coluna `chunk` usando o endpoint
# MAGIC > de foundation model `databricks-gte-large-en` via `ai_query`, e salve numa nova coluna
# MAGIC > `embedding` numa tabela `exam_embeddings`."_
# MAGIC
# MAGIC > _"Escreva uma função Python `buscar(pergunta, k=3)` que: gera o embedding da pergunta com o
# MAGIC > mesmo endpoint, calcula a similaridade de cosseno contra `exam_embeddings` e retorna os k
# MAGIC > trechos mais parecidos."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — Geração da resposta com LLM
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
# MAGIC ## 4 · 🧞 SUA VEZ (opcional / avançado) — Caminho B: Vector Search gerenciado
# MAGIC Versão "de produção" usando índice gerenciado. **Atenção:** criar o endpoint leva ~10 min.
# MAGIC
# MAGIC **Prompts sugeridos:**
# MAGIC
# MAGIC > _"Habilite Change Data Feed em `exam_chunks` e crie um Vector Search endpoint chamado
# MAGIC > `exam-search` e um Delta Sync Index `exam_chunks_vs_index` que faça o embedding automático
# MAGIC > da coluna `chunk` com `databricks-gte-large-en`."_
# MAGIC
# MAGIC > _"Consulte o índice com `similarity_search` para a pergunta X e me mostre os resultados."_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você construiu um pipeline RAG: documentos → parsing → embeddings → busca → resposta com LLM.
# MAGIC **Bônus:** peça ao Assistant para _"criar um app de chat em Gradio que usa a função
# MAGIC `responder`"_ e publique como um **Databricks App**.
