# 🧞 Guia de Prompts — falando com o Databricks Assistant

O **Databricks Assistant** é o copiloto de código dentro do notebook. Hoje, **você não
decora sintaxe — você aprende a pedir bem.** Esta é a habilidade que leva pra vida.

> Abra o Assistant com o ícone **✨** no canto da célula, ou **`Cmd/Ctrl + I`**.
> Não confunda com o **Genie** (que responde perguntas sobre *dados* em linguagem natural) —
> o **Assistant** escreve *código* pra você.

## As 5 regras de ouro

1. **Aponte para algo real.** Cite o nome exato da tabela, coluna ou função.
   ❌ _"limpe os dados"_ → ✅ _"remova linhas de `bronze_matriculas` onde `nota_p1` é nula"_
2. **Peça um passo de cada vez.** Construa incrementalmente; rode; só então peça o próximo.
3. **Cole o erro de volta.** Deu erro? Copie a mensagem inteira no Assistant e peça pra corrigir.
4. **Peça para explicar.** _"explique linha por linha o que esse código faz"_ — você aprende mais.
5. **Itere.** A primeira resposta raramente é a final. _"agora faça X também"_, _"deixe mais rápido"_.

## Anatomia de um bom prompt

> **[contexto]** Tenho a tabela `silver_matriculas` com colunas aluno_id, nota_final, situacao.
> **[tarefa]** Crie uma tabela Delta `gold_desempenho_aluno` agregando por aluno e semestre.
> **[detalhes]** Calcule média do semestre, nº de aprovações e o CRA acumulado.
> **[formato]** Use PySpark e me explique cada transformação.

## Prompts de partida por trilha

### Trilha 1 — Data Engineering + AI/BI + Genie
- _"Seguindo o padrão da célula `bronze_matriculas`, crie as tabelas Bronze para alunos, disciplinas, cursos, departamentos e professores."_
- _"Crie `silver_matriculas` juntando todas as Bronze, com nomes legíveis e colunas `aprovado`/`reprovado`."_
- _"Crie `gold_desempenho_disciplina` com taxa de aprovação e nota média por disciplina e semestre."_
- No **Genie**: _"Qual curso tem a maior taxa de reprovação?"_ → se errar, ensine com Instructions + Example SQL.

### Trilha 2 — Machine Learning
- _"Crie atributos por aluno: CRA, total de disciplinas, reprovações anteriores e taxa de aprovação."_
- _"Treine um GradientBoostingClassifier para prever `reprovou`, com `mlflow.sklearn.autolog()`."_
- _"Plote a importância das features e a curva ROC."_

### Trilha 3 — RAG
- _"Crie um Vector Search endpoint `exam-search` (STANDARD) se ainda não existir, sem bloquear esperando ficar ONLINE."_ ⏱️ dispare cedo (~10 min)
- _"Crie um Delta Sync Index `exam_chunks_vs_index` no endpoint `exam-search` a partir de `exam_chunks`, com embedding gerenciado da coluna `chunk` usando `databricks-gte-large-en`."_
- _"Escreva `buscar(pergunta, k=3)` usando o `similarity_search` do índice."_
- _"Escreva `responder(pergunta)` que usa os trechos como contexto e gera a resposta com `ai_query` e o modelo `databricks-meta-llama-3-3-70b-instruct`."_

## Quando travar
1. Releia a mensagem de erro — ela quase sempre diz o que fazer.
2. Cole o erro no Assistant: _"recebi este erro: <cole aqui>. Como corrijo?"_
3. Peça uma versão mais simples: _"faça a versão mais simples possível que funcione"_.
4. Último recurso: espie a pasta `solutions/` — mas tente sozinho primeiro. 😉
