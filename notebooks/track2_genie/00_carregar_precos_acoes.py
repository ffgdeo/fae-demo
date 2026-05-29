# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 2 · Genie — Setup 1/3: Preços de Ações
# MAGIC ## AAPL, MSFT, AMZN (2021 – 2024)
# MAGIC
# MAGIC Carrega os **preços diários de abertura** de Apple, Microsoft e Amazon (via Yahoo Finance)
# MAGIC e grava numa tabela Delta em formato longo. É a primeira das **3 tabelas** que vão alimentar
# MAGIC o seu **Genie Space** nesta trilha.
# MAGIC
# MAGIC | Coluna   | Tipo   | Descrição                         |
# MAGIC |----------|--------|-----------------------------------|
# MAGIC | Date     | date   | Pregão (dia de negociação)        |
# MAGIC | ticker   | string | AAPL, MSFT ou AMZN                 |
# MAGIC | Price    | double | Preço de abertura em USD          |
# MAGIC
# MAGIC > Usamos a coluna `ticker` (e não `Stock`) para que esta tabela **junte** de forma limpa com
# MAGIC > `participacao_mercado` e `fatores_crescimento` dentro do mesmo Genie Space.
# MAGIC >
# MAGIC > 🎛️ Catálogo e schema são definidos por **widgets** no topo (padrão: `workspace` /
# MAGIC > `mercado_acoes`). Use os mesmos valores nos 3 notebooks de setup desta trilha.
# MAGIC >
# MAGIC > ⚠️ Esta célula baixa dados da internet (`yfinance`). Se o acesso externo estiver bloqueado
# MAGIC > no seu workspace, fale com o facilitador — há uma amostra estática de reserva (Plano B).

# COMMAND ----------

# MAGIC %pip install -q yfinance

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# Parâmetros — definidos por widgets para o notebook ser reutilizável entre workspaces.
dbutils.widgets.text("catalog",    "workspace",      "Catalog")
dbutils.widgets.text("schema",     "mercado_acoes",  "Schema")
dbutils.widgets.text("table",      "precos_acoes",   "Table")
dbutils.widgets.text("start_date", "2021-01-01",     "Data inicial (YYYY-MM-DD)")
dbutils.widgets.text("end_date",   "2024-12-31",     "Data final (YYYY-MM-DD)")
dbutils.widgets.text("tickers",    "AAPL,MSFT,AMZN", "Tickers (separados por vírgula)")

CATALOG    = dbutils.widgets.get("catalog")
SCHEMA     = dbutils.widgets.get("schema")
TABLE      = dbutils.widgets.get("table")
START_DATE = dbutils.widgets.get("start_date")
END_DATE   = dbutils.widgets.get("end_date")
TICKERS    = [t.strip().upper() for t in dbutils.widgets.get("tickers").split(",") if t.strip()]
FQN        = f"{CATALOG}.{SCHEMA}.{TABLE}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

print(f"Vai gravar em: {FQN}")
print(f"Tickers:       {TICKERS}")
print(f"Período:       {START_DATE} → {END_DATE}")

# COMMAND ----------

import yfinance as yf
import pandas as pd

frames = []
for ticker in TICKERS:
    raw = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    raw = raw.reset_index()[["Date", "Open"]]
    raw.columns = ["Date", "Price"]
    raw["ticker"] = ticker
    frames.append(raw)

df_acoes = pd.concat(frames, ignore_index=True)[["Date", "ticker", "Price"]]
df_acoes["Date"] = pd.to_datetime(df_acoes["Date"]).dt.date
df_acoes["Price"] = df_acoes["Price"].astype(float)

df_acoes.head()

# COMMAND ----------

df_acoes_spark = spark.createDataFrame(df_acoes)

(df_acoes_spark.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(FQN))

spark.sql(
    f"COMMENT ON TABLE {FQN} IS 'Preços diários de abertura de AAPL, MSFT, AMZN (formato longo). Fonte: Yahoo Finance via yfinance.'"
)

display(spark.table(FQN).orderBy("ticker", "Date"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Tabela 1/3 pronta
# MAGIC Agora rode **`01_carregar_participacao_mercado`** e **`02_carregar_fatores_crescimento`**,
# MAGIC e depois siga para **`03_construir_genie_space`** para montar e *ensinar* o seu Genie.
# MAGIC
# MAGIC ### Fontes
# MAGIC - Yahoo Finance via `yfinance`: https://pypi.org/project/yfinance/
