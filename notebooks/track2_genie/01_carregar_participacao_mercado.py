# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 2 · Genie — Setup 2/3: Participação de Mercado
# MAGIC ## AAPL, MSFT, AMZN (2021 – 2024)
# MAGIC
# MAGIC Carrega a **participação de mercado trimestral** das três empresas cujos preços você acabou de
# MAGIC carregar. Cada empresa atua em um ou mais segmentos de referência:
# MAGIC
# MAGIC | Ticker | Segmento | Fonte |
# MAGIC |--------|----------|-------|
# MAGIC | AAPL   | Smartphones (global, unidades) | IDC / Counterpoint / Statista |
# MAGIC | MSFT   | Infraestrutura de Nuvem        | Synergy Research Group        |
# MAGIC | MSFT   | Sistema Operacional Desktop    | StatCounter Global Stats      |
# MAGIC | AMZN   | E-commerce de Varejo (EUA)     | eMarketer / Insider Intelligence |
# MAGIC | AMZN   | Infraestrutura de Nuvem        | Synergy Research Group        |
# MAGIC
# MAGIC Os valores são percentuais do segmento, arredondados para uma casa decimal. Onde as fontes
# MAGIC primárias publicam apenas números anuais, os valores trimestrais são estimativas suavizadas
# MAGIC ancoradas no valor anual reportado.
# MAGIC
# MAGIC > 🎛️ Use o **mesmo** catálogo/schema dos outros notebooks de setup desta trilha.

# COMMAND ----------

# Parâmetros — definidos por widgets para o notebook ser reutilizável entre workspaces.
dbutils.widgets.text("catalog", "workspace",            "Catalog")
dbutils.widgets.text("schema",  "mercado_acoes",        "Schema")
dbutils.widgets.text("table",   "participacao_mercado", "Table")

CATALOG = dbutils.widgets.get("catalog")
SCHEMA  = dbutils.widgets.get("schema")
TABLE   = dbutils.widgets.get("table")
FQN     = f"{CATALOG}.{SCHEMA}.{TABLE}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

print(f"Vai gravar em: {FQN}")

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, to_date, concat, lit, when

# (ticker, company, segment, year, quarter, market_share_pct, segment_rank, segment_size_usd_billions, source)
rows = [
    # -------------------- AAPL — Smartphones global (unidades, IDC/Counterpoint) --------------------
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2021, 1, 17.0, 2, 100.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2021, 2, 14.1, 2,  83.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2021, 3, 15.2, 2,  90.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2021, 4, 22.0, 1, 130.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2022, 1, 18.0, 2, 101.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2022, 2, 15.5, 2,  80.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2022, 3, 17.5, 2,  91.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2022, 4, 23.0, 1, 120.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2023, 1, 20.5, 1,  90.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2023, 2, 17.0, 2,  77.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2023, 3, 17.7, 2,  89.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2023, 4, 24.7, 1, 125.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2024, 1, 17.3, 2,  94.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2024, 2, 15.8, 2,  86.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2024, 3, 17.7, 2,  96.0, "IDC"),
    ("AAPL", "Apple Inc.",      "Global Smartphones",         2024, 4, 23.0, 1, 128.0, "IDC"),

    # -------------------- MSFT — Infraestrutura de Nuvem (Synergy) --------------------
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2021, 1, 19.0, 2,  39.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2021, 2, 20.0, 2,  42.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2021, 3, 21.0, 2,  45.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2021, 4, 22.0, 2,  50.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2022, 1, 22.0, 2,  53.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2022, 2, 21.0, 2,  55.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2022, 3, 21.0, 2,  57.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2022, 4, 23.0, 2,  63.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2023, 1, 23.0, 2,  63.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2023, 2, 22.0, 2,  65.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2023, 3, 23.0, 2,  68.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2023, 4, 24.0, 2,  74.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2024, 1, 25.0, 2,  76.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2024, 2, 23.0, 2,  79.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2024, 3, 20.0, 2,  84.0, "Synergy Research"),
    ("MSFT", "Microsoft Corp.", "Cloud Infrastructure",       2024, 4, 21.0, 2,  91.0, "Synergy Research"),

    # -------------------- MSFT — Sistema Operacional Desktop (StatCounter) --------------------
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2021, 1, 76.6, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2021, 2, 75.8, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2021, 3, 75.0, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2021, 4, 75.5, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2022, 1, 75.1, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2022, 2, 74.3, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2022, 3, 73.9, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2022, 4, 74.0, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2023, 1, 73.5, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2023, 2, 73.0, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2023, 3, 72.1, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2023, 4, 72.8, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2024, 1, 72.7, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2024, 2, 72.1, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2024, 3, 73.1, 1, None, "StatCounter"),
    ("MSFT", "Microsoft Corp.", "Desktop Operating System",   2024, 4, 73.4, 1, None, "StatCounter"),

    # -------------------- AMZN — E-commerce de Varejo EUA (eMarketer) --------------------
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2021, 1, 41.4, 1, 200.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2021, 2, 41.8, 1, 210.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2021, 3, 41.5, 1, 215.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2021, 4, 41.0, 1, 260.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2022, 1, 40.0, 1, 225.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2022, 2, 39.5, 1, 235.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2022, 3, 39.3, 1, 240.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2022, 4, 39.0, 1, 290.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2023, 1, 37.8, 1, 250.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2023, 2, 37.6, 1, 260.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2023, 3, 37.4, 1, 270.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2023, 4, 37.6, 1, 320.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2024, 1, 39.8, 1, 278.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2024, 2, 40.2, 1, 288.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2024, 3, 40.5, 1, 298.0, "eMarketer"),
    ("AMZN", "Amazon.com Inc.", "US Retail E-commerce",       2024, 4, 40.4, 1, 350.0, "eMarketer"),

    # -------------------- AMZN — Infraestrutura de Nuvem (Synergy) --------------------
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2021, 1, 32.0, 1,  39.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2021, 2, 33.0, 1,  42.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2021, 3, 32.0, 1,  45.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2021, 4, 33.0, 1,  50.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2022, 1, 33.0, 1,  53.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2022, 2, 34.0, 1,  55.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2022, 3, 34.0, 1,  57.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2022, 4, 32.0, 1,  63.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2023, 1, 32.0, 1,  63.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2023, 2, 32.0, 1,  65.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2023, 3, 32.0, 1,  68.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2023, 4, 31.0, 1,  74.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2024, 1, 31.0, 1,  76.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2024, 2, 32.0, 1,  79.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2024, 3, 33.0, 1,  84.0, "Synergy Research"),
    ("AMZN", "Amazon.com Inc.", "Cloud Infrastructure",       2024, 4, 30.0, 1,  91.0, "Synergy Research"),
]

columns = [
    "ticker", "company", "segment", "year", "quarter",
    "market_share_pct", "segment_rank", "segment_size_usd_billions", "source",
]

df = spark.createDataFrame([Row(**dict(zip(columns, r))) for r in rows])

df = df.withColumn(
    "quarter_end_date",
    to_date(concat(
        col("year"), lit("-"),
        when(col("quarter") == 1, lit("03-31"))
         .when(col("quarter") == 2, lit("06-30"))
         .when(col("quarter") == 3, lit("09-30"))
         .otherwise(lit("12-31"))
    ))
)

df = df.select(
    "ticker", "company", "segment",
    "year", "quarter", "quarter_end_date",
    "market_share_pct", "segment_rank", "segment_size_usd_billions",
    "source",
)

display(df.orderBy("ticker", "segment", "year", "quarter"))

# COMMAND ----------

(df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(FQN))

spark.sql(f"COMMENT ON TABLE {FQN} IS 'Participação de mercado trimestral de AAPL, MSFT, AMZN nos seus segmentos de referência (2021-2024). Fontes: IDC, Synergy Research, StatCounter, eMarketer.'")

spark.sql(f"DESCRIBE EXTENDED {FQN}").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Tabela 2/3 pronta
# MAGIC Falta a **`02_carregar_fatores_crescimento`**. Depois, vá para **`03_construir_genie_space`**.
# MAGIC
# MAGIC ### Fontes
# MAGIC - Synergy Research Group — participação em nuvem: https://www.srgresearch.com/articles
# MAGIC - IDC — Smartphone Market Share Tracker: https://www.idc.com/promo/smartphone-market-share/
# MAGIC - Counterpoint Research — iPhone: https://counterpointresearch.com/en/insights/apple-iphone-market-share
# MAGIC - Statista — iPhone global 2007-2024: https://www.statista.com/statistics/216459/global-market-share-of-apple-iphone/
# MAGIC - eMarketer / Insider Intelligence — Amazon e-commerce EUA: https://www.emarketer.com/content/amazon-us-ecommerce-market
# MAGIC - StatCounter — Desktop OS: https://gs.statcounter.com/os-market-share/desktop/worldwide/
