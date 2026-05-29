# 🧑‍🏫 Roteiro do Facilitador — FAE Demo

Atividade hands-on para estudantes na Databricks Free Edition. Duas trilhas principais
(**Data Engineering + AI/BI** e **Genie**) + uma opcional (**ML Clássico**). O gabarito completo
está em `solutions/`.

> 🧞 **Terminologia:** sempre **"Genie Code"** (o copiloto que escreve código no notebook) —
> não "Databricks Assistant". Distinga do **Genie Space** (Q&A de dados em linguagem natural, Trilha 2).

## ✅ Antes do evento (faça o dry-run!)
- [ ] **Crie uma conta Free Edition limpa** e rode as trilhas de ponta a ponta **antes da segunda**. Melhor seguro contra surpresas.
- [ ] **Trilha 2 — teste o `yfinance`:** o `00_carregar_precos_acoes` baixa preços da internet. Confirme que o **egress externo** funciona no Free Edition; se estiver bloqueado, prepare um Plano B (amostra estática de preços). As outras duas tabelas da Trilha 2 são hardcoded — não dependem de internet.
- [ ] **Trilha 1 / 3:** confirme que `00_gerar_dados` roda (Run all) e deixa os CSVs no Volume.
- [ ] Decida quais trilhas posicionar ao vivo. Sugestão: **Genie (Trilha 2)** como destaque + **Trilha 1** para quem curte engenharia de dados; **ML (Trilha 3)** fica como aprofundamento/casa.
- [ ] Tenha o link curto do repo e o link do Free Edition num slide.
- [ ] Decida: cada aluno usa a própria conta (recomendado) ou duplas.

## ⏱️ Sugestão de agenda (~2h)
| Tempo | Bloco |
|---|---|
| 0:00–0:15 | Abertura: posicionar as trilhas + criar conta Free Edition + importar o repo |
| 0:15–0:25 | Demo ao vivo do **Genie Code** (regras de ouro do `PROMPTS.md`) |
| 0:25–0:30 | Alunos escolhem a trilha |
| 0:30–1:40 | **Mão na massa** (facilitadores circulando) |
| 1:40–2:00 | Show & tell: 2-3 alunos mostram o que construíram + Q&A |

## 🎯 Os momentos "uau" pra garantir que cada um chegue
- **Trilha 1:** ver o **grafo do pipeline declarativo** materializar Bronze→Silver→Gold + um gráfico no dashboard AI/BI gerado em linguagem natural.
- **Trilha 2 (Genie):** fazer uma pergunta em português ao **Genie Space**, ver ele errar, **ensiná-lo** com uma Instruction/Example SQL e ver a resposta melhorar. 🧞
- **Trilha 3 (ML, opcional):** abrir **Experiments** e ver o run do MLflow com métricas e modelo rastreados.

Se o tempo apertar, priorize chegar nesses momentos — o resto é bônus.

## ⚠️ Particularidades do Free Edition (já validadas)
- **Serverless apenas** — sem clusters clássicos, sem Lakebase. Tudo roda em compute serverless.
- **`ai_query` funciona com modelos abertos** (Llama, GTE) — útil se quiser estender a Trilha 3.
- **Trilha 1 é um pipeline declarativo** — o notebook é a *definição*, não roda célula a célula
  (rodar interativo dá `cannot import name 'pipelines'` — esperado, não é limite do Free Edition).
  Fluxo: **Jobs & Pipelines → Create → ETL Pipeline** abre com um `.py` de exemplo vazio; os alunos
  vão em **Settings**, apontam **Root folder** + **Source code** para o notebook da trilha (removendo
  o arquivo de exemplo) e ajustam **Default catalog/schema**. Ingestão = **streaming tables** (Auto
  Loader); Silver/Gold = **materialized views**. Passo a passo no topo do notebook.
- **Trilha 2 (Genie):** os 3 setups gravam tabelas Delta direto (não é pipeline). Rodar `00`, `01`,
  `02` (Run all em cada) e só então `03`. O `00` precisa de internet (`yfinance`).
- **`00_gerar_dados` não cria tabelas** — só deixa CSVs no Volume (zona raw). Construir as tabelas é
  o exercício das Trilhas 1 e 3.

## 🩹 Problemas comuns e soluções
| Sintoma | Causa provável | Solução |
|---|---|---|
| `Table or view not found` na Trilha 1/3 | Não rodou o setup | Rode `00_gerar_dados` (Run all) primeiro |
| Trilha 2: tabelas não existem no Genie | Não rodou os 3 setups | Rode `track2_genie/00`, `01`, `02` (Run all em cada) antes do `03` |
| Trilha 2: `00` falha ao baixar preços | `yfinance` sem acesso à internet | Use o Plano B (amostra estática); as outras 2 tabelas independem de internet |
| Erro de `dp`/`pipelines` ao rodar a Trilha 1 no notebook | Tentou Run All | Trilha 1 não roda assim — crie um **Pipeline** apontando pro notebook e rode por lá |
| Pipeline não acha os CSVs | Usou catálogo/schema custom no setup | Em Advanced → Configuration, defina `fae.csv_base` pro Volume correto |
| Genie responde errado / não entende termo | Falta contexto | É o exercício! Adicione Instructions/synonyms/Example SQL (veja `solutions/track2_genie_gabarito.md`) |
| Geração de dados lenta | Cold start do serverless | Aguarde; é idempotente, pode reexecutar |
| Aluno "travado" no código | — | Mande prompar o **Genie Code** com o erro; só então abrir `solutions/` |

## 📚 Gabarito (`solutions/`)
- `track1_pipeline_completo.py` — pipeline declarativo Bronze→Silver→Gold completo
- `track2_genie_gabarito.md` — instruções, synonyms e Example SQL para o Genie Space de mercado
- `track3_ml_completo.py` — feature engineering + GradientBoosting + MLflow
- `dashboard_painel_academico.lvdash.json` — dashboard AI/BI de referência (Trilha 1)

> Origem: derivado do demo "Sistema Acadêmico Inteligente" (`github.com/ffgdeo/ufscar-demo`),
> já comprovado em Free Edition. Dataset de mercado da Trilha 2 cedido por Fernando de Come.
