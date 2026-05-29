# Databricks notebook source

# MAGIC %md
# MAGIC # Trilha 2 · Genie — Construa e *ensine* o seu Genie Space
# MAGIC ## Pergunte ao mercado em português 🧞
# MAGIC
# MAGIC **Objetivo:** transformar 3 tabelas de mercado (AAPL, MSFT, AMZN) em um **Genie Space** que
# MAGIC responde perguntas de negócio em **linguagem natural** — e aprender o ciclo de **ensinar o Genie**
# MAGIC com instruções e exemplos quando ele erra.
# MAGIC
# MAGIC **Pré-requisito:** rode os 3 setups desta pasta antes
# MAGIC (`00_carregar_precos_acoes`, `01_carregar_participacao_mercado`, `02_carregar_fatores_crescimento`).
# MAGIC
# MAGIC > 💡 Não confunda os dois "Genie":
# MAGIC > - **Genie Code** = o copiloto que **escreve código** pra você no notebook (ícone ✨ / `Cmd/Ctrl + I`).
# MAGIC > - **Genie Space** = onde você **pergunta sobre os dados** em linguagem natural. É o que você constrói aqui.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace",     "Catalog")
dbutils.widgets.text("schema",  "mercado_acoes", "Schema")
CATALOG = dbutils.widgets.get("catalog")
SCHEMA  = dbutils.widgets.get("schema")
spark.sql(f"USE {CATALOG}.{SCHEMA}")
print(f"Usando {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0 · Confira que as 3 tabelas existem
# MAGIC Você deve ver `precos_acoes`, `participacao_mercado` e `fatores_crescimento`.

# COMMAND ----------

display(spark.sql("SHOW TABLES"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · As 3 tabelas e como elas se conectam
# MAGIC Todas têm a coluna **`ticker`** (AAPL/MSFT/AMZN) — é por ela que o Genie cruza as tabelas.
# MAGIC
# MAGIC | Tabela | Grão | Para que serve |
# MAGIC |---|---|---|
# MAGIC | `precos_acoes` | diário, por ticker | evolução do preço de abertura |
# MAGIC | `participacao_mercado` | trimestral, por ticker + segmento | share por segmento (nuvem, smartphones, e-commerce, OS) |
# MAGIC | `fatores_crescimento` | trimestral, por ticker | receita, lucro, EPS, P&D, taxa do Fed e o evento-chave do trimestre |
# MAGIC
# MAGIC > 🧞 Use o **Genie Code** (✨) se quiser explorar: _"mostre o preço médio de abertura por ano e ticker em `precos_acoes`"_.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Crie o Genie Space (na interface)
# MAGIC 1. Menu lateral → **Genie** → **New**.
# MAGIC 2. Em **Tables / Data**, adicione as 3 tabelas do schema `mercado_acoes`:
# MAGIC    `precos_acoes`, `participacao_mercado`, `fatores_crescimento`.
# MAGIC 3. Dê um nome ao Space (ex.: *Mercado — AAPL/MSFT/AMZN*) e abra o chat.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · 🧞 SUA VEZ — pergunte em português
# MAGIC Comece pelo simples e vá subindo a complexidade (perguntas que cruzam tabelas são as mais legais):
# MAGIC
# MAGIC - _"Qual foi o preço de abertura médio da Apple em 2024?"_
# MAGIC - _"Compare a participação da Microsoft e da Amazon em Infraestrutura de Nuvem ao longo dos trimestres."_
# MAGIC - _"Em que trimestre a Amazon teve prejuízo e qual foi o evento associado?"_
# MAGIC - _"Mostre a receita trimestral da Microsoft junto com a taxa do Fed."_
# MAGIC - _"Qual empresa liderava o e-commerce de varejo nos EUA em 2023?"_
# MAGIC
# MAGIC > Reparou que algumas colunas estão em inglês (`market_share_pct`, `revenue_usd_billions`)?
# MAGIC > Faz parte do desafio — é aí que entram as **instruções** do próximo passo.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · 🧞 SUA VEZ — ENSINE o Genie (o aprendizado-chave da trilha)
# MAGIC Quando o Genie erra ou não entende um termo, **você o ensina** — esse loop é o ponto da trilha.
# MAGIC
# MAGIC No Genie Space, use:
# MAGIC - **Instructions (General):** explique o domínio em português. Ex.:
# MAGIC   > _"`market_share_pct` é a participação de mercado em %. `revenue_usd_billions` é a receita em US$ bilhões.
# MAGIC   > 'Apple'=AAPL, 'Microsoft'=MSFT, 'Amazon'=AMZN. 'Nuvem' refere-se ao segmento 'Cloud Infrastructure'."_
# MAGIC - **Example SQL (queries de exemplo):** para perguntas que o Genie erra, salve a consulta certa
# MAGIC   como exemplo. Ex.: variação anual do preço, ou crescimento de receita YoY.
# MAGIC - **Trusted assets / synonyms:** ensine sinônimos (ex.: "faturamento" = `revenue_usd_billions`).
# MAGIC
# MAGIC **Roteiro do exercício:** faça uma pergunta que o Genie erre → adicione uma Instruction ou um
# MAGIC Example SQL → refaça a pergunta → veja melhorar. Repita 2-3 vezes. 🎯

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · (Bônus) Dashboard AI/BI sobre as mesmas tabelas
# MAGIC 1. Menu lateral → **Dashboards** → **Create dashboard** → adicione as 3 tabelas em **Data**.
# MAGIC 2. Em **Canvas** → **Add a visualization**, descreva em linguagem natural:
# MAGIC    _"preço de abertura médio por ano e empresa"_, _"participação em nuvem por trimestre"_,
# MAGIC    _"receita vs. taxa do Fed ao longo do tempo"_.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Pronto!
# MAGIC Você montou um Genie Space sobre dados reais de mercado e — o mais importante — **aprendeu a
# MAGIC ensiná-lo**. Esse ciclo (perguntar → corrigir com instruções/exemplos → melhorar) é exatamente
# MAGIC como se constrói um Genie confiável na vida real.
