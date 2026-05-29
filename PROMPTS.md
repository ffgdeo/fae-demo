# 🧞 Guia de Prompts — falando com o Genie Code

O **Genie Code** é o copiloto de código dentro do notebook. Hoje, **você não
decora sintaxe — você aprende a pedir bem.** Esta é a habilidade que leva pra vida.

> Abra o Genie Code com o ícone **✨** no canto da célula, ou **`Cmd/Ctrl + I`**.
> Não confunda com o **Genie Space** (que responde perguntas sobre *dados* em linguagem natural,
> na Trilha 2) — o **Genie Code** escreve *código* pra você.

## As 5 regras de ouro

1. **Aponte para algo real.** Cite o nome exato da tabela, coluna ou função.
   ❌ _"limpe os dados"_ → ✅ _"remova linhas de `bronze_matriculas` onde `nota_p1` é nula"_
2. **Peça um passo de cada vez.** Construa incrementalmente; rode; só então peça o próximo.
3. **Cole o erro de volta.** Deu erro? Copie a mensagem inteira no Genie Code e peça pra corrigir.
4. **Peça para explicar.** _"explique linha por linha o que esse código faz"_ — você aprende mais.
5. **Itere.** A primeira resposta raramente é a final. _"agora faça X também"_, _"deixe mais rápido"_.

## Anatomia de um bom prompt

> **[contexto]** Tenho a tabela `silver_matriculas` com colunas aluno_id, nota_final, situacao.
> **[tarefa]** Crie uma tabela Delta `gold_desempenho_aluno` agregando por aluno e semestre.
> **[detalhes]** Calcule média do semestre, nº de aprovações e o CRA acumulado.
> **[formato]** Use PySpark e me explique cada transformação.

## Prompts de partida por trilha

### Trilha 1 — Data Engineering + AI/BI (pipeline declarativo)
- _"Seguindo o padrão da `@dp.table` `bronze_matriculas` (streaming table via Auto Loader), crie as streaming tables Bronze para alunos, disciplinas, cursos, departamentos e professores."_
- _"Crie a materialized view `silver_matriculas` juntando todas as Bronze, com nomes legíveis, colunas `aprovado`/`reprovado` e expectativas `@dp.expect`."_
- _"Crie a materialized view `gold_desempenho_disciplina` com taxa de aprovação e nota média por disciplina e semestre."_
- No **dashboard AI/BI**: descreva o gráfico em linguagem natural — _"taxa de aprovação média por departamento"_.

> ⚠️ A Trilha 1 é a **definição** de um pipeline. Você não roda célula a célula — cria um
> **Pipeline** apontando pro notebook e roda por lá (passo a passo no fim do notebook).

### Trilha 2 — Genie 🧞
Aqui você usa o **Genie Code** só para os 3 notebooks de setup (carregar as tabelas) — depois o
trabalho é no **Genie Space**, em linguagem natural. Perguntas para fazer ao Space:
- _"Qual foi o preço de abertura médio da Apple em 2024?"_
- _"Compare a participação da Microsoft e da Amazon em Infraestrutura de Nuvem ao longo dos trimestres."_
- _"Em que trimestre a Amazon teve prejuízo e qual foi o evento associado?"_
- _"Mostre a receita trimestral da Microsoft junto com a taxa do Fed."_

> 🎯 Quando o Genie errar, **ensine-o**: adicione *Instructions*, *synonyms* e *Example SQL* no Space.
> Esse loop é o aprendizado-chave da trilha (veja `solutions/track2_genie_gabarito.md`).

### Trilha 3 (opcional) — Machine Learning
- _"Crie atributos por aluno: CRA, total de disciplinas, reprovações anteriores e taxa de aprovação."_
- _"Treine um GradientBoostingClassifier para prever `reprovou`, com `mlflow.sklearn.autolog()`."_
- _"Plote a importância das features e a curva ROC."_

## Quando travar
1. Releia a mensagem de erro — ela quase sempre diz o que fazer.
2. Cole o erro no Genie Code: _"recebi este erro: <cole aqui>. Como corrijo?"_
3. Peça uma versão mais simples: _"faça a versão mais simples possível que funcione"_.
4. Último recurso: espie a pasta `solutions/` — mas tente sozinho primeiro. 😉
