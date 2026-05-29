# FAE Demo — Hands-on Databricks Free Edition 🧞

Atividade prática para estudantes na **Databricks Free Edition**, usando o
**Genie Code** (o copiloto de código dentro do notebook) para escrever o código com você.

São duas trilhas principais + uma opcional:
- **Trilha 1 — Data Engineering + AI/BI** sobre dados sintéticos de um **Sistema Acadêmico**
  (alunos, matrículas, notas, disciplinas).
- **Trilha 2 — Genie** sobre um dataset de **mercado financeiro** (AAPL, MSFT, AMZN): preços,
  participação de mercado e fatores de crescimento. Você monta e *ensina* um Genie Space.
- **Trilha 3 (opcional) — Machine Learning Clássico** sobre o mesmo dataset acadêmico da Trilha 1.

## 🚀 Como começar

1. Crie uma conta gratuita em **[https://www.databricks.com/learn/free-edition](https://login.databricks.com/?intent=FAE_visit)**.
2. No workspace: menu lateral → **Workspace** → **Repos / Git folder** → **Add** →
   cole a URL deste repositório:
   ```
   https://github.com/ffgdeo/fae-demo.git
   ```
3. Escolha sua trilha e abra os notebooks correspondentes:

| Trilha | Setup (rode primeiro) | Notebook(s) da trilha | O que você constrói |
|---|---|---|---|
| 1 · Data Engineering + AI/BI | `track1_dados_aibi/00_gerar_dados` | `track1_dados_aibi/01_dados_aibi` | Pipeline declarativo (streaming tables + materialized views) Bronze→Silver→Gold + dashboard AI/BI |
| 2 · Genie 🧞 | `track2_genie/00`, `01`, `02` | `track2_genie/03_construir_genie_space` | Um Genie Space que responde perguntas de mercado em português — e como **ensiná-lo** |
| 3 · ML Clássico *(opcional)* | `track1_dados_aibi/00_gerar_dados` | `track3_ml_classico_opcional/00_ml_classico` | Modelo de predição de reprovação com MLflow |

> 🎛️ Todos os notebooks têm widgets de **catalog** e **schema** no topo. As Trilhas 1 e 3 usam o
> padrão `workspace` / `sistema_academico`; a Trilha 2 usa `workspace` / `mercado_acoes`. Use os
> valores que quiser — só mantenha o **mesmo** catálogo/schema em todos os notebooks de uma trilha.

## 🧞 Genie Code vs. Genie Space

- **Genie Code** = o copiloto que **escreve código** pra você no notebook (ícone ✨ / `Cmd/Ctrl + I`).
- **Genie Space** = onde você **pergunta sobre os dados** em linguagem natural (Trilha 2).

Veja o guia **[PROMPTS.md](PROMPTS.md)** — saber pedir bem ao Genie Code é a habilidade do dia.

## 📁 Estrutura

```
notebooks/
  track1_dados_aibi/
    00_gerar_dados.py      # setup acadêmico — rode primeiro (também é pré-req da Trilha 3)
    01_dados_aibi.py       # Trilha 1 — pipeline + dashboard
  track2_genie/            # Trilha 2 — setup (00-02) + construir o Genie (03)
  track3_ml_classico_opcional/
    00_ml_classico.py      # Trilha 3 (opcional) — ML + MLflow
solutions/                 # gabarito completo — só espie se travar de verdade 😉
```

## 🧑‍🏫 Para facilitadores

Veja **[FACILITATOR.md](FACILITATOR.md)** — roteiro, tempos e como resolver problemas comuns.

---
*Databricks University Alliance · Free Edition (serverless).*
