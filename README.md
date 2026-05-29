# FAE Demo — Hands-on Databricks Free Edition 🧞

Atividade prática para estudantes: construir **3 soluções de dados e IA** na
[Databricks Free Edition](https://www.databricks.com/learn/free-edition), usando o
**Databricks Assistant** para escrever o código com você.

Todas as trilhas partem de um mesmo conjunto de dados sintéticos: o **Sistema Acadêmico**
de uma universidade brasileira (alunos, matrículas, notas, disciplinas e provas).

## 🚀 Como começar

1. Crie uma conta gratuita em **[databricks.com/learn/free-edition](https://www.databricks.com/learn/free-edition)**.
2. No workspace: menu lateral → **Workspace** → **Repos / Git folder** → **Add** →
   cole a URL deste repositório:
   ```
   https://github.com/ffgdeo/fae-demo.git
   ```
3. Abra `notebooks/00_gerar_dados` e clique em **Run all** (~3-5 min). ⚠️ **Faça isso primeiro.**
4. Escolha **uma trilha** e abra o notebook correspondente:

| Trilha | Notebook | O que você constrói |
|---|---|---|
| 1 · Data Engineering + AI/BI + Genie | `notebooks/track1_dados_aibi_genie` | Pipeline Bronze→Silver→Gold, dashboard e Genie |
| 2 · Machine Learning Clássico | `notebooks/track2_ml_classico` | Modelo de predição de reprovação com MLflow |
| 3 · RAG | `notebooks/track3_rag` | Assistente de Q&A sobre provas (busca + LLM) |

## 🧞 Como prompar o Assistant

Veja o guia **[PROMPTS.md](PROMPTS.md)** — a habilidade mais importante do dia.

## 📁 Estrutura

```
notebooks/   # ponto de partida de cada trilha (rode estes)
data/exams/  # 12 PDFs de provas (usados pela Trilha 3)
solutions/   # gabarito completo — só espie se travar de verdade 😉
```

## 🧑‍🏫 Para facilitadores

Veja **[FACILITATOR.md](FACILITATOR.md)** — roteiro, tempos e como resolver problemas comuns.

---
*Databricks University Alliance · Free Edition (serverless).*
