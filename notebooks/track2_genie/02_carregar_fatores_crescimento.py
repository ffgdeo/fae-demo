# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 2 · Genie — Setup 3/3: Fatores de Crescimento
# MAGIC ## AAPL, MSFT, AMZN (2021 – 2024)
# MAGIC
# MAGIC Carrega um dataset trimestral de fatores que ajudam a **explicar o movimento do preço** das
# MAGIC ações de Apple, Microsoft e Amazon:
# MAGIC
# MAGIC - **Fundamentos** — receita, lucro líquido, EPS diluído, gastos com P&D (em US$ bilhões, exceto o EPS).
# MAGIC - **Macro** — taxa efetiva dos Fed Funds no fim do trimestre.
# MAGIC - **Narrativa** — o evento de empresa/mercado mais relevante do trimestre (virada do Fed,
# MAGIC   ChatGPT, Vision Pro, split 20:1, marcação a mercado da Rivian etc.).
# MAGIC
# MAGIC Os trimestres são trimestres-calendário. Apple e Microsoft usam anos fiscais defasados; aqui os
# MAGIC números foram remapeados para o trimestre-calendário correspondente.
# MAGIC
# MAGIC > 🎛️ Use o **mesmo** catálogo/schema dos outros notebooks de setup desta trilha.

# COMMAND ----------

# Parâmetros — definidos por widgets para o notebook ser reutilizável entre workspaces.
dbutils.widgets.text("catalog", "workspace",             "Catalog")
dbutils.widgets.text("schema",  "mercado_acoes",         "Schema")
dbutils.widgets.text("table",   "fatores_crescimento",   "Table")

CATALOG = dbutils.widgets.get("catalog")
SCHEMA  = dbutils.widgets.get("schema")
TABLE   = dbutils.widgets.get("table")
FQN     = f"{CATALOG}.{SCHEMA}.{TABLE}"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

print(f"Vai gravar em: {FQN}")

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.functions import col, to_date, concat, lit, when

# Taxa efetiva dos Fed Funds no fim do trimestre (%), série DFF do FRED.
fed_rate_by_quarter = {
    (2021, 1): 0.08, (2021, 2): 0.08, (2021, 3): 0.08, (2021, 4): 0.08,
    (2022, 1): 0.33, (2022, 2): 1.58, (2022, 3): 3.08, (2022, 4): 4.33,
    (2023, 1): 4.83, (2023, 2): 5.08, (2023, 3): 5.33, (2023, 4): 5.33,
    (2024, 1): 5.33, (2024, 2): 5.33, (2024, 3): 4.83, (2024, 4): 4.33,
}

# (ticker, company, year, quarter, revenue_b, net_income_b, diluted_eps, rd_spend_b, event_category, key_event, commentary)
rows = [
    # ============================ APPLE ============================
    ("AAPL", "Apple Inc.", 2021, 1,  89.58, 23.63, 1.40, 5.26, "Earnings",
     "Fiscal Q2'21: record March quarter driven by iPhone 12 5G upgrade cycle and Services growth",
     "Revenue +54% YoY; Services hits all-time high; $90B buyback authorized in April"),
    ("AAPL", "Apple Inc.", 2021, 2,  81.43, 21.74, 1.30, 5.72, "Supply",
     "Global chip shortage starts to constrain iPhone and iPad production",
     "Tim Cook warns of $3B-$4B supply-constraint headwind for September quarter"),
    ("AAPL", "Apple Inc.", 2021, 3,  83.36, 20.55, 1.24, 6.22, "Product",
     "iPhone 13 launch (September 14, 2021)",
     "Supply constraints cost ~$6B in revenue in the quarter; demand robust despite shortages"),
    ("AAPL", "Apple Inc.", 2021, 4, 123.95, 34.63, 2.10, 6.31, "Earnings",
     "Record holiday quarter: first quarter above $120B revenue",
     "iPhone revenue $71.6B; Services $19.5B; market cap briefly tops $3T in January"),

    ("AAPL", "Apple Inc.", 2022, 1,  97.28, 25.01, 1.52, 6.39, "Earnings",
     "Strong March quarter despite macro headwinds",
     "Supply impact eases; Services revenue at new high; board raises dividend 5%"),
    ("AAPL", "Apple Inc.", 2022, 2,  82.96, 19.44, 1.20, 6.80, "Macro",
     "Tech selloff amid Fed tightening; Apple down ~23% YTD at June low",
     "China COVID lockdowns and FX headwinds weigh on results"),
    ("AAPL", "Apple Inc.", 2022, 3,  90.15, 20.72, 1.29, 6.76, "Product",
     "iPhone 14 launch (September 16, 2022); Pro-mix strength",
     "Services decelerates; production issues at Zhengzhou Foxconn facility late Q3"),
    ("AAPL", "Apple Inc.", 2022, 4, 117.15, 29.99, 1.88, 7.71, "Supply",
     "Foxconn Zhengzhou COVID disruption cuts ~$5B off iPhone Pro shipments",
     "First YoY revenue decline since Q1 2020; stock slides into year-end"),

    ("AAPL", "Apple Inc.", 2023, 1,  94.84, 24.16, 1.52, 7.46, "Earnings",
     "Revenue -3% YoY; iPhone returns to growth despite macro softness",
     "Services reaches new all-time high; installed base of devices crosses 2B active units"),
    ("AAPL", "Apple Inc.", 2023, 2,  81.80, 19.88, 1.26, 7.44, "Product",
     "Apple Vision Pro unveiled at WWDC (June 5, 2023)",
     "First major new product category since Apple Watch; mixed analyst reception"),
    ("AAPL", "Apple Inc.", 2023, 3,  89.50, 22.96, 1.46, 7.51, "Product",
     "iPhone 15 / 15 Pro launch (September 22, 2023); USB-C transition",
     "Pro models supply-constrained; stock flat YTD vs Magnificent-7 peers"),
    ("AAPL", "Apple Inc.", 2023, 4, 119.58, 33.92, 2.18, 7.70, "Earnings",
     "Holiday quarter beat; Services revenue +11% YoY",
     "Management guides flat Q1 revenue; China iPhone concerns build"),

    ("AAPL", "Apple Inc.", 2024, 1,  90.75, 23.64, 1.53, 7.70, "Product",
     "Apple Vision Pro launches in US (February 2, 2024)",
     "iPhone revenue -10% YoY in Greater China on Huawei resurgence; stock underperforms"),
    ("AAPL", "Apple Inc.", 2024, 2,  85.78, 21.45, 1.40, 7.85, "AI",
     "Apple Intelligence unveiled at WWDC 2024 (June 10, 2024)",
     "AI strategy reframes upgrade-cycle narrative; stock rallies ~15% post-WWDC"),
    ("AAPL", "Apple Inc.", 2024, 3,  94.93, 14.74, 0.97, 7.77, "Macro",
     "iPhone 16 launch (September 20, 2024); one-time EU State Aid tax charge of ~$10.2B",
     "Reported net income depressed by Ireland tax ruling; ex-charge EPS tracks higher"),
    ("AAPL", "Apple Inc.", 2024, 4, 124.30, 36.33, 2.40, 8.26, "AI",
     "Apple Intelligence features begin rolling out on iPhone 16 / 15 Pro",
     "Record revenue quarter; Services +14% YoY; market cap tops $3.9T in December"),

    # ============================ MICROSOFT ============================
    ("MSFT", "Microsoft Corp.", 2021, 1, 41.71, 15.46, 2.03, 5.22, "Earnings",
     "Fiscal Q3'21: Azure revenue +50% YoY in constant currency",
     "Cloud momentum accelerates; gaming up on Xbox Series X/S"),
    ("MSFT", "Microsoft Corp.", 2021, 2, 46.15, 16.46, 2.17, 5.26, "M&A",
     "Nuance Communications acquisition announced ($19.7B, April 2021)",
     "Fiscal Q4'21 beat; healthcare AI strategic bet"),
    ("MSFT", "Microsoft Corp.", 2021, 3, 45.32, 20.51, 2.71, 5.80, "Product",
     "Windows 11 released (October 5, 2021)",
     "Azure growth remains ~50%; Microsoft 365 subs cross 54M consumer seats"),
    ("MSFT", "Microsoft Corp.", 2021, 4, 51.73, 18.77, 2.48, 6.31, "M&A",
     "Activision Blizzard acquisition announced ($68.7B, January 18, 2022)",
     "Largest tech acquisition in history; gaming long-term bet"),

    ("MSFT", "Microsoft Corp.", 2022, 1, 49.36, 16.73, 2.22, 6.31, "Macro",
     "Fed begins rate hikes; tech multiple compression begins",
     "Azure +46% in constant currency; Commercial bookings +28%"),
    ("MSFT", "Microsoft Corp.", 2022, 2, 51.87, 16.74, 2.23, 6.84, "Earnings",
     "FY22 closes with $198B revenue, +18% YoY",
     "FX headwinds mount; management guidance cautious for FY23"),
    ("MSFT", "Microsoft Corp.", 2022, 3, 50.12, 17.56, 2.35, 6.77, "Macro",
     "Strong dollar cuts ~$2.3B off revenue; PC market softens",
     "First quarter with Azure growth decelerating to ~35%"),
    ("MSFT", "Microsoft Corp.", 2022, 4, 52.75, 16.43, 2.20, 6.95, "AI",
     "ChatGPT launch (November 30, 2022); Microsoft discloses deepened OpenAI partnership",
     "10,000 layoffs announced in January 2023; pivot to AI cost discipline"),

    ("MSFT", "Microsoft Corp.", 2023, 1, 52.86, 18.30, 2.45, 6.98, "AI",
     "$10B OpenAI investment confirmed; Bing Chat launches (February 7, 2023)",
     "First AI-enabled Bing; search index refresh; GitHub Copilot crosses 1M users"),
    ("MSFT", "Microsoft Corp.", 2023, 2, 56.19, 20.08, 2.69, 6.98, "AI",
     "Microsoft 365 Copilot announced (March 16, 2023); GPT-4 integrations",
     "Cloud revenue tops $30B/quarter; AI narrative supports re-rating"),
    ("MSFT", "Microsoft Corp.", 2023, 3, 56.52, 22.29, 2.99, 6.66, "Product",
     "Microsoft 365 Copilot enterprise GA (November 1, 2023, $30/seat/month)",
     "Activision deal closes (October 13, 2023) after regulatory overhang"),
    ("MSFT", "Microsoft Corp.", 2023, 4, 62.02, 21.87, 2.93, 7.51, "Earnings",
     "Azure +30% in constant currency; ~6 points from AI services",
     "Market cap briefly surpasses Apple in January 2024 as largest public company"),

    ("MSFT", "Microsoft Corp.", 2024, 1, 61.86, 21.94, 2.94, 7.96, "AI",
     "Copilot Pro consumer tier launches ($20/month, January 2024)",
     "AI contribution to Azure growth rises to ~7 points; capex ramp begins"),
    ("MSFT", "Microsoft Corp.", 2024, 2, 64.73, 22.04, 2.95, 7.48, "Capex",
     "Annual capex jumps to ~$56B (FY24) led by AI datacenter buildout",
     "Street debates AI ROI timing; margins slightly pressured by depreciation"),
    ("MSFT", "Microsoft Corp.", 2024, 3, 65.59, 24.67, 3.30, 7.54, "Capex",
     "FY25 Q1 capex $20B+; AI infrastructure commitments accelerating",
     "Stock range-bound through summer; investors worry AI capex runs ahead of monetization"),
    ("MSFT", "Microsoft Corp.", 2024, 4, 69.63, 24.11, 3.23, 7.63, "AI",
     "AI business run-rate surpasses $13B; Azure AI revenue inflects",
     "Management guides strong FY25 H2 as datacenter capacity comes online"),

    # ============================ AMAZON ============================
    ("AMZN", "Amazon.com Inc.", 2021, 1, 108.52,  8.11, 0.79, 14.84, "Earnings",
     "AWS revenue $13.5B, +32% YoY; operating margin 30.8%",
     "Final quarter of Jeff Bezos as CEO; Andy Jassy transitions July 5, 2021"),
    ("AMZN", "Amazon.com Inc.", 2021, 2, 113.08,  7.78, 0.76, 15.18, "Leadership",
     "Andy Jassy becomes CEO (July 5, 2021)",
     "Post-pandemic e-commerce deceleration begins; guidance below Street"),
    ("AMZN", "Amazon.com Inc.", 2021, 3, 110.81,  3.16, 0.31, 14.38, "Macro",
     "Labor and freight cost pressures; $2B in excess costs flagged",
     "First quarter of material e-commerce overbuild becoming visible"),
    ("AMZN", "Amazon.com Inc.", 2021, 4, 137.41, 14.32, 1.39, 14.65, "One-off",
     "Rivian IPO (Nov 10, 2021); Amazon records $11.8B pre-tax gain on its stake",
     "Reported net income inflated by Rivian mark-to-market gain"),

    ("AMZN", "Amazon.com Inc.", 2022, 1, 116.44, -3.84,-0.38, 16.49, "One-off",
     "$7.6B pre-tax Rivian mark-to-market LOSS; first quarterly loss since 2015",
     "Concerns about e-commerce overbuild and fulfillment overcapacity mount"),
    ("AMZN", "Amazon.com Inc.", 2022, 2, 121.23, -2.03,-0.20, 18.07, "Corporate",
     "20-for-1 stock split takes effect (June 6, 2022)",
     "Second consecutive net loss on Rivian mark-down; AWS remains strong engine"),
    ("AMZN", "Amazon.com Inc.", 2022, 3, 127.10,  2.87, 0.28, 18.30, "Macro",
     "Advertising revenue +30% (ex-FX); cloud spend optimization visible in AWS",
     "Retail segment swings back to modest profitability"),
    ("AMZN", "Amazon.com Inc.", 2022, 4, 149.20,  0.28, 0.03, 20.35, "Layoffs",
     "18,000 layoffs announced (January 2023); largest in company history",
     "AWS growth decelerates to ~20%; stock bottoms near $84 in December 2022"),

    ("AMZN", "Amazon.com Inc.", 2023, 1, 127.36,  3.17, 0.31, 20.45, "Cost",
     "Cost-out program underway; another 9,000 layoffs announced (March 2023)",
     "AWS growth slows to 16%; management warns of continued optimization headwind"),
    ("AMZN", "Amazon.com Inc.", 2023, 2, 134.38,  6.75, 0.65, 21.31, "Logistics",
     "Regionalized US fulfillment network complete; delivery speed at record highs",
     "Retail operating income inflects positive; advertising +22% YoY"),
    ("AMZN", "Amazon.com Inc.", 2023, 3, 143.08,  9.88, 0.94, 21.20, "AI",
     "Bedrock GA announced; $4B Anthropic investment disclosed (September 25, 2023)",
     "AWS growth stabilizes at 12%; gen-AI pipeline cited as multi-billion revenue run-rate"),
    ("AMZN", "Amazon.com Inc.", 2023, 4, 169.96, 10.62, 1.00, 22.66, "AI",
     "Amazon Q (enterprise AI assistant) announced at re:Invent 2023 (November 28, 2023)",
     "Record holiday; AWS reaccelerates; stock +80% in 2023"),

    ("AMZN", "Amazon.com Inc.", 2024, 1, 143.31, 10.43, 0.98, 22.14, "Earnings",
     "AWS +17% YoY; operating income more than 3x vs prior-year Q1",
     "Additional $2.75B Anthropic investment completes total $4B commitment"),
    ("AMZN", "Amazon.com Inc.", 2024, 2, 147.98, 13.49, 1.26, 22.34, "AI",
     "Gen-AI workloads at AWS at multi-billion-dollar revenue run-rate",
     "Advertising +20%; retail margin expansion continues"),
    ("AMZN", "Amazon.com Inc.", 2024, 3, 158.88, 15.33, 1.43, 22.62, "Capex",
     "AWS capex ramps; management signals $75B+ capex for 2024",
     "Operating margin at record 11%; stock consolidates on capex concerns"),
    ("AMZN", "Amazon.com Inc.", 2024, 4, 187.79, 20.00, 1.86, 21.44, "Earnings",
     "Record $187.8B revenue quarter; AWS run-rate crosses $115B",
     "Advertising exits 2024 at ~$69B run-rate; Amazon ends year near all-time highs"),
]

columns = [
    "ticker", "company", "year", "quarter",
    "revenue_usd_billions", "net_income_usd_billions", "diluted_eps",
    "rd_spending_usd_billions",
    "event_category", "key_event", "commentary",
]

enriched = [
    r + (fed_rate_by_quarter[(r[2], r[3])],)
    for r in rows
]
columns_full = columns + ["effective_fed_funds_rate_pct"]

df = spark.createDataFrame(
    [Row(**dict(zip(columns_full, r))) for r in enriched]
)

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
    "ticker", "company",
    "year", "quarter", "quarter_end_date",
    "revenue_usd_billions", "net_income_usd_billions", "diluted_eps",
    "rd_spending_usd_billions",
    "effective_fed_funds_rate_pct",
    "event_category", "key_event", "commentary",
)

display(df.orderBy("ticker", "year", "quarter"))

# COMMAND ----------

(df.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(FQN))

spark.sql(
    f"COMMENT ON TABLE {FQN} IS 'Fatores de crescimento trimestrais de AAPL, MSFT, AMZN (2021-2024): fundamentos financeiros, taxa Fed Funds e um evento narrativo por trimestre. Fontes: arquivamentos 10-K/10-Q, Macrotrends, FRED.'"
)

spark.sql(f"DESCRIBE EXTENDED {FQN}").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ As 3 tabelas estão prontas!
# MAGIC Agora abra **`03_construir_genie_space`** para montar o seu Genie Space sobre `precos_acoes`,
# MAGIC `participacao_mercado` e `fatores_crescimento` — e aprender a **ensiná-lo**.
# MAGIC
# MAGIC ### Fontes
# MAGIC - Apple IR: https://investor.apple.com/investor-relations/default.aspx
# MAGIC - Microsoft IR: https://www.microsoft.com/en-us/investor/earnings/
# MAGIC - Amazon IR: https://ir.aboutamazon.com/quarterly-results/
# MAGIC - Macrotrends (AAPL/MSFT/AMZN revenue): https://www.macrotrends.net/stocks/charts/AAPL/apple/revenue
# MAGIC - FRED — Effective Federal Funds Rate (DFF): https://fred.stlouisfed.org/series/DFF
