# 🧑‍🏫 Roteiro do Facilitador — FAE Demo

Atividade hands-on para estudantes na Databricks Free Edition. Tudo parte de um dataset
acadêmico sintético; o gabarito completo (testado) está em `solutions/`.

## ✅ Antes do evento (faça o dry-run!)
- [ ] **Crie uma conta Free Edition limpa** e rode as 3 trilhas de ponta a ponta **antes da segunda**. É o melhor seguro contra surpresas.
- [ ] Confirme que os endpoints de foundation model existem no workspace de teste: `databricks-gte-large-en` (embeddings) e `databricks-meta-llama-3-3-70b-instruct` (geração). Se algum nome mudar, ajuste em `track3_rag.py` e `PROMPTS.md`.
- [ ] Garanta que os 12 PDFs estão no repo (`data/exams/`) — a Trilha 3 depende deles.
- [ ] Tenha o link curto do repo e o link do Free Edition num slide.
- [ ] Decida: cada aluno usa a própria conta (recomendado) ou duplas.

## ⏱️ Sugestão de agenda (~2h)
| Tempo | Bloco |
|---|---|
| 0:00–0:15 | Abertura: posicionar as 3 trilhas + criar conta Free Edition + importar o repo |
| 0:15–0:25 | Demo ao vivo do Assistant (regras de ouro do `PROMPTS.md`) + rodar `00_gerar_dados` juntos |
| 0:25–0:30 | Alunos escolhem a trilha |
| 0:30–1:40 | **Mão na massa** (facilitadores circulando) |
| 1:40–2:00 | Show & tell: 2-3 alunos mostram o que construíram + Q&A |

## 🎯 Os 3 momentos "uau" pra garantir que cada um chegue
- **Trilha 1:** ver o **grafo do pipeline declarativo** materializar Bronze→Silver→Gold e, depois, perguntar em português no **Genie**.
- **Trilha 2:** abrir **Experiments** e ver o run do MLflow com métricas e modelo rastreados.
- **Trilha 3:** o assistente **respondendo uma pergunta sobre uma prova** citando o PDF de origem.

Se o tempo apertar, priorize chegar nesses momentos — o resto é bônus.

## ⚠️ Particularidades do Free Edition (já validadas)
- **Serverless apenas** — sem clusters clássicos, sem Lakebase. Tudo roda em compute serverless.
- **`ai_query` funciona com modelos abertos** (Llama, GTE) — base das Trilhas 2/3.
- **Vector Search demora ~10 min** pra subir o endpoint. A Trilha 3 usa **Vector Search gerenciado
  como caminho padrão** — oriente os alunos a **dispararem a criação do endpoint logo na célula 2**
  e seguirem no resto enquanto sobe. Há um **Plano B** no fim do notebook (embeddings em Delta +
  cosseno) caso o endpoint não fique ONLINE a tempo.
- **AutoML** pode não estar disponível na UI → Trilha 2 usa scikit-learn + MLflow direto.
- **Trilha 1 é um pipeline declarativo** — o notebook é a *definição*, não roda célula a célula
  (rodar interativo dá `cannot import name 'pipelines'` — esperado, não é limite do Free Edition).
  Fluxo atual: **Jobs & Pipelines → Create → ETL Pipeline** abre com um `.py` de exemplo vazio;
  os alunos vão em **Settings**, apontam **Root folder** + **Source code** para o notebook da trilha
  (removendo o arquivo de exemplo) e ajustam **Default catalog/schema**. Ingestão = **streaming
  tables** (Auto Loader); Silver/Gold = **materialized views**. Passo a passo no topo do notebook.
- **`00_gerar_dados` não cria tabelas** — só deixa CSVs e PDFs no Volume (zona raw). Construir as
  tabelas é o exercício de cada trilha.

## 🩹 Problemas comuns e soluções
| Sintoma | Causa provável | Solução |
|---|---|---|
| `Table or view not found` numa trilha | Não rodou o setup | Rode `00_gerar_dados` (Run all) primeiro |
| Erro de `dp`/`pipelines` ao rodar a Trilha 1 no notebook | Tentou Run All | Trilha 1 não roda assim — crie um **Pipeline** apontando pro notebook e rode por lá |
| Pipeline não acha os CSVs | Usou catálogo/schema custom no setup | Em Advanced → Configuration, defina `fae.csv_base` pro Volume correto |
| PDFs não encontrados na Trilha 3 | Repo importado sem `data/exams/` | Reimporte o Git folder; confira a pasta |
| `ai_query` falha / endpoint não existe | Nome do modelo diferente no workspace | Liste em **Serving** e ajuste o nome no prompt |
| Geração de dados lenta | Cold start do serverless | Aguarde; é idempotente, pode reexecutar |
| Aluno "travado" no código | — | Mande prompar o Assistant com o erro; só então abrir `solutions/` |

## 📚 Gabarito (`solutions/`)
- `track1_pipeline_completo.py` — pipeline declarativo Bronze→Silver→Gold completo
- `track2_ml_completo.py` — feature engineering + GradientBoosting + MLflow
- `track3_rag_completo.py` — parsing + Vector Search + Llama 3.3 70B
- `dashboard_painel_academico.lvdash.json` — dashboard AI/BI de referência
- `genie_space.json` — definição do Genie Space de referência

> Origem: derivado do demo "Sistema Acadêmico Inteligente" (`github.com/ffgdeo/ufscar-demo`),
> já comprovado em Free Edition.
