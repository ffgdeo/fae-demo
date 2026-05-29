# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 2 · Machine Learning Clássico
# MAGIC
# MAGIC **Objetivo:** treinar um modelo que prevê se um aluno vai **reprovar** uma disciplina,
# MAGIC usando engenharia de atributos + scikit-learn, e rastrear tudo com **MLflow**.
# MAGIC
# MAGIC **Pré-requisito:** rode o notebook `00_gerar_dados` antes deste.
# MAGIC
# MAGIC Este notebook te entrega os dados prontos e um exemplo de atributo.
# MAGIC Você constrói o modelo com o **Databricks Assistant** (células 🧞 **SUA VEZ**).

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
dbutils.widgets.text("schema", "sistema_academico", "Schema")
CATALOG = dbutils.widgets.get("catalog")
SCHEMA  = dbutils.widgets.get("schema")
spark.sql(f"USE {CATALOG}.{SCHEMA}")
print(f"Usando {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0 · Conheça os dados
# MAGIC A tabela `matriculas` tem uma linha por (aluno, disciplina) com notas, frequência e `situacao`.

# COMMAND ----------

display(spark.table("matriculas").limit(10))

# COMMAND ----------

# Distribuição do alvo: quem aprovou vs. reprovou
display(spark.sql("""
  SELECT situacao, COUNT(*) AS n
  FROM matriculas
  WHERE situacao != 'trancado'
  GROUP BY situacao ORDER BY n DESC
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Defina o alvo (target)
# MAGIC Vamos prever **reprovação**: `reprovou = 1` se `situacao` começa com "reprovado", senão `0`.

# COMMAND ----------

import pandas as pd

df = spark.sql("""
  SELECT
    matricula_id, aluno_id, disciplina_id, nota_p1, frequencia_pct,
    CASE WHEN situacao LIKE 'reprovado%' THEN 1 ELSE 0 END AS reprovou
  FROM matriculas
  WHERE situacao != 'trancado' AND nota_p1 IS NOT NULL
""").toPandas()

print(f"Linhas: {len(df)} | Taxa de reprovação: {df.reprovou.mean():.1%}")
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · 🧞 SUA VEZ — Engenharia de atributos
# MAGIC Notas e frequência da própria matrícula são fortes, mas o **histórico do aluno** ajuda muito.
# MAGIC
# MAGIC **Prompt sugerido para o Assistant** (✨ ou `Cmd/Ctrl + I`):
# MAGIC
# MAGIC > _"A partir da tabela `matriculas` (ignorando situacao='trancado'), crie um DataFrame de
# MAGIC > atributos por aluno com: CRA acumulado (média de nota_final), total de disciplinas cursadas,
# MAGIC > total de reprovações anteriores e taxa de aprovação pessoal. Depois junte esses atributos
# MAGIC > de aluno ao DataFrame `df` desta célula, pela coluna aluno_id."_
# MAGIC
# MAGIC 💡 Junte tudo num pandas DataFrame chamado `dataset` com a coluna `reprovou` como alvo.

# COMMAND ----------

# 👇 monte aqui o `dataset` final (atributos + alvo)


# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — Treine o modelo com MLflow
# MAGIC
# MAGIC **Prompt sugerido:**
# MAGIC
# MAGIC > _"Usando o DataFrame `dataset` (alvo = coluna `reprovou`), faça train/test split,
# MAGIC > treine um GradientBoostingClassifier do scikit-learn, e registre TUDO no MLflow com
# MAGIC > `mlflow.sklearn.autolog()`: parâmetros, métricas (accuracy, ROC AUC), e o modelo.
# MAGIC > Imprima o classification_report."_
# MAGIC
# MAGIC 💡 Depois de rodar, clique em **Experiments** (menu lateral) para ver o run rastreado.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · 🧞 SUA VEZ — Interprete o modelo
# MAGIC
# MAGIC **Prompts sugeridos:**
# MAGIC
# MAGIC > _"Plote a importância das features do modelo treinado, da maior para a menor."_
# MAGIC
# MAGIC > _"Plote a curva ROC no conjunto de teste."_
# MAGIC
# MAGIC > _"Quais 10 alunos ativos têm a maior probabilidade prevista de reprovar no próximo semestre?"_

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você treinou e rastreou um modelo de ML de ponta a ponta.
# MAGIC **Bônus:** peça ao Assistant para _"registrar o modelo no Unity Catalog e servi-lo num
# MAGIC endpoint de Model Serving"_, ou para _"comparar GradientBoosting com RandomForest e
# MAGIC LogisticRegression no MLflow"_.
