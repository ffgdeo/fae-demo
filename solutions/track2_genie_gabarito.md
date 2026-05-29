# Gabarito — Trilha 2 · Genie (Mercado AAPL/MSFT/AMZN)

Referência para facilitadores. O exercício do aluno é **construir** o Genie Space na interface
sobre as 3 tabelas e aprender a **ensiná-lo**. Aqui vão as instruções, sinônimos e queries de
exemplo que fazem o Space responder bem.

## Tabelas (schema `mercado_acoes`)
- `precos_acoes` — diário: `Date`, `ticker`, `Price` (abertura, USD)
- `participacao_mercado` — trimestral: `ticker`, `company`, `segment`, `year`, `quarter`, `quarter_end_date`, `market_share_pct`, `segment_rank`, `segment_size_usd_billions`, `source`
- `fatores_crescimento` — trimestral: `ticker`, `company`, `year`, `quarter`, `quarter_end_date`, `revenue_usd_billions`, `net_income_usd_billions`, `diluted_eps`, `rd_spending_usd_billions`, `effective_fed_funds_rate_pct`, `event_category`, `key_event`, `commentary`

Chave de junção entre as três tabelas: **`ticker`** (e `year`+`quarter` entre as duas trimestrais).

## Instructions (General) sugeridas para colar no Space
```
As tabelas cobrem três empresas: 'Apple'/'Apple Inc.' = AAPL, 'Microsoft'/'Microsoft Corp.' = MSFT,
'Amazon'/'Amazon.com Inc.' = AMZN.
- market_share_pct: participação de mercado em % do segmento.
- revenue_usd_billions / net_income_usd_billions / rd_spending_usd_billions: valores em US$ bilhões.
- diluted_eps: lucro por ação diluído (USD).
- effective_fed_funds_rate_pct: taxa básica de juros dos EUA (Fed) no fim do trimestre, em %.
- 'Nuvem'/'cloud' = segmento 'Cloud Infrastructure'. 'Smartphones' = 'Global Smartphones'.
  'E-commerce'/'varejo online' = 'US Retail E-commerce'. 'Sistema operacional'/'OS' = 'Desktop Operating System'.
- Em precos_acoes, Price é o preço de ABERTURA diário. Para "preço médio", use AVG(Price).
- Para variação anual de preço, compare o primeiro e o último pregão do ano.
```

## Sinônimos úteis (synonyms)
- "faturamento", "receita" → `revenue_usd_billions`
- "lucro" → `net_income_usd_billions`
- "juros", "taxa do Fed" → `effective_fed_funds_rate_pct`
- "participação", "share" → `market_share_pct`

## Perguntas de exemplo (com SQL de referência)

**Preço médio de abertura da Apple em 2024**
```sql
SELECT AVG(Price) AS preco_medio_abertura
FROM precos_acoes
WHERE ticker = 'AAPL' AND YEAR(Date) = 2024;
```

**Participação em nuvem: Microsoft vs. Amazon por trimestre**
```sql
SELECT year, quarter, ticker, market_share_pct
FROM participacao_mercado
WHERE segment = 'Cloud Infrastructure' AND ticker IN ('MSFT','AMZN')
ORDER BY year, quarter, ticker;
```

**Trimestre de prejuízo da Amazon + evento associado**
```sql
SELECT year, quarter, net_income_usd_billions, key_event, commentary
FROM fatores_crescimento
WHERE ticker = 'AMZN' AND net_income_usd_billions < 0
ORDER BY year, quarter;
```

**Receita trimestral da Microsoft junto com a taxa do Fed**
```sql
SELECT year, quarter, revenue_usd_billions, effective_fed_funds_rate_pct
FROM fatores_crescimento
WHERE ticker = 'MSFT'
ORDER BY year, quarter;
```

**Crescimento de receita YoY (cruzando o mesmo trimestre do ano anterior)**
```sql
SELECT a.ticker, a.year, a.quarter,
       a.revenue_usd_billions AS receita_atual,
       b.revenue_usd_billions AS receita_ano_anterior,
       ROUND(100 * (a.revenue_usd_billions - b.revenue_usd_billions) / b.revenue_usd_billions, 1) AS crescimento_yoy_pct
FROM fatores_crescimento a
JOIN fatores_crescimento b
  ON a.ticker = b.ticker AND a.quarter = b.quarter AND a.year = b.year + 1
ORDER BY a.ticker, a.year, a.quarter;
```

**Empresa líder no e-commerce de varejo nos EUA (por ano)**
```sql
SELECT year, ticker, AVG(market_share_pct) AS share_medio
FROM participacao_mercado
WHERE segment = 'US Retail E-commerce'
GROUP BY year, ticker
ORDER BY year;
```

## Momento "uau" da trilha
O aluno faz uma pergunta que o Genie erra (ex.: confunde "nuvem" com o segmento errado, ou não acha
"faturamento") → adiciona uma Instruction/synonym/Example SQL → refaz e vê acertar. Esse loop de
**ensinar o Genie** é o aprendizado central.
