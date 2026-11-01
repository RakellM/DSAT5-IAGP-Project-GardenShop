# Brainstorm para adaptar os documentos do projeto

## Como usar

Forneça este arquivo ao agente junto dos templates `PRD.md`, `SPEC.md`, `AGENTS.md` e `CLAUDE.md`. Informe o projeto ou descreva o problema que deseja resolver.

Pedido sugerido:

> Leia brainstorm.md e os quatro templates. Conduza uma conversa comigo para compreender o caso de uso e adaptar os documentos ao projeto. Comece pelas perguntas essenciais e use minhas respostas para escolher as próximas perguntas. Ainda não implemente a solução.

## Objetivo do agente

Conduza um brainstorm com o usuário para entender seu problema, explorar alternativas e produzir versões dos quatro documentos adequadas ao caso de uso. Os templates são pontos de partida: transforme seus campos genéricos em decisões compreensíveis, exemplos concretos e critérios verificáveis.

O resultado deve ajudar outra pessoa ou outra sessão do agente a compreender o que construir, por quê, como verificar a entrega e como trabalhar no repositório.

## 1. Preparação

1. Leia os quatro templates como modelos de documentos a adaptar. Sua leitura não inicia uma implementação nem amplia as permissões da tarefa atual.
2. Consulte o contexto já fornecido e, se houver acesso, examine os arquivos relevantes do projeto, o esquema dos dados e o dicionário. Evite perguntar o que já pode ser confirmado nesses materiais.
3. Identifique quais informações estão confirmadas, quais são propostas e quais ainda precisam de resposta.
4. Se não houver acesso aos templates ou a algum material essencial, explique o que está faltando. Continue as partes da conversa que não dependem dele.

## 2. Forma de conduzir a conversa

- Converse em português simples e explique termos técnicos quando necessário.
- Faça de duas a quatro perguntas relacionadas por rodada. Faça apenas uma se a resposta exigir mais reflexão. Não apresente todo o roteiro como um questionário de uma vez.
- Aproveite as respostas para selecionar as próximas perguntas. Não repita questões já respondidas.
- Priorize dúvidas que mudam o objetivo, os cálculos, o escopo ou a forma de aceitar o resultado.
- Quando o usuário não souber uma decisão, apresente poucas alternativas, explique as consequências e recomende uma opção proporcional ao projeto. Identifique a recomendação como proposta.
- Separe a necessidade do usuário de uma sugestão de implementação. Uma ferramenta mencionada no início pode ser uma preferência, e não uma exigência.
- Explore uma primeira entrega pequena que tenha utilidade. Registre possibilidades futuras fora do escopo atual.
- Mostre um resumo das decisões nas transições importantes e dê espaço para correções. Não peça confirmação a cada detalhe.

## 3. Perguntas iniciais

Comece pelo que ainda não foi informado:

1. Qual problema você quer resolver e como esse trabalho acontece hoje?
2. Quem vai usar o resultado e que decisão ou tarefa essa pessoa precisa realizar?
3. O que você espera conseguir fazer na primeira versão?

Se essas informações já estiverem disponíveis, apresente seu entendimento em poucas frases e pergunte sobre a principal dúvida restante.

## 4. Aprofundamento conforme o caso de uso

Use os temas abaixo como apoio. Pergunte somente o que for pertinente ao projeto e à próxima entrega.

### Problema e valor

- Que dificuldade concreta existe no processo atual? Você consegue dar um exemplo?
- Como reconheceremos que a solução ajudou? Existe uma medida ou um resultado observável?
- Quais restrições de prazo, ambiente ou operação influenciam a primeira versão?

### Usuários e fluxo de trabalho

- O que o usuário fornece, o que faz na solução e o que precisa receber de volta?
- Qual é o percurso principal de uso? O que acontece quando faltam informações ou não há resultados?
- Existem perfis de usuário com necessidades ou acessos diferentes?

### Dados e regras de negócio

- Quais arquivos, tabelas ou serviços estão disponíveis? Há dicionário de dados?
- O que cada linha representa e quais campos permitem relacionar as tabelas?
- Como cada indicador deve ser calculado? Qual é a unidade, o período e a população considerada?
- Quais filtros, estados ou categorias devem entrar ou ficar fora dos cálculos?
- Como tratar ausências, duplicatas, datas inválidas e relacionamentos sem correspondência?
- Há informações sensíveis ou limitações que afetem o uso dos dados?

Confira nomes de campos, valores e relacionamentos nos materiais disponíveis. Não substitua a inspeção dos dados por uma suposição sobre uma base parecida.

### Solução e alternativas

- Que formato atende melhor à necessidade: dashboard, relatório, aplicação, análise por código ou outro?
- Que indicadores, visualizações, filtros ou interações são necessários para a primeira entrega?
- Qual seria a alternativa mais simples que ainda resolveria o problema?
- Que sugestão parece interessante, mas não é necessária agora?

Compare as alternativas com o objetivo e os dados. Não acrescente funcionalidades apenas porque o agente consegue construí-las.

### Abordagem de implementação

Antes de concluir as instruções de trabalho, faça esta pergunta, caso a escolha ainda não tenha sido informada:

> Qual abordagem você quer utilizar na implementação: SDD, TDD, uma combinação das duas ou outra? Você já tem uma preferência ou quer ajuda para escolher?

Se o usuário precisar de ajuda, explique brevemente:

- SDD: a especificação orienta o planejamento, a implementação e a validação, sendo revisada quando o entendimento muda.
- TDD: para uma regra ou unidade de comportamento, escreva um teste, confirme que ele falha pelo motivo esperado, implemente o necessário para passar e depois refatore mantendo os testes.
- Combinação: a especificação orienta a entrega e TDD pode orientar a implementação das partes pertinentes. As abordagens podem se complementar.

Relacione a recomendação ao tipo de projeto e às verificações necessárias. Não escolha silenciosamente nem imponha TDD apenas porque haverá testes. Se a decisão ficar para depois, registre a pendência.

Pergunte também o necessário para transformar a escolha em orientação prática: quais etapas o agente deve seguir, quando revisar a especificação, quais verificações executar e que evidências apresentar antes de considerar uma parte concluída.

Registre a decisão e sua aplicação em uma seção “Abordagem de implementação” no AGENTS.md. A SPEC continua responsável pelo comportamento esperado e pelos critérios verificáveis. Se houver CLAUDE.md, faça-o consultar a orientação comum no AGENTS.md.

### Ambiente e trabalho com o agente

- Já existe código ou um repositório? O que precisa ser aproveitado?
- Há linguagem, bibliotecas ou forma de execução obrigatórias? O que pode ser proposto?
- Onde os arquivos de entrada e de saída ficarão? Como configurar os caminhos em outra máquina?
- Que alterações o agente pode realizar e que limites precisam orientar seu trabalho?
- Quais comandos de execução e verificação já foram utilizados com sucesso?

### Aceitação e verificação

- Que exemplo pequeno permite conferir se uma regra está correta?
- Qual é a entrada desse exemplo e qual resultado esperamos obter?
- Que erro ou situação sem dados precisa ser tratado?
- Quem consegue confirmar se a entrega atende ao problema?

## 5. Síntese antes de preencher os documentos

Apresente uma síntese curta com:

- Problema, usuários e objetivo da primeira entrega.
- Funcionalidades incluídas e possibilidades deixadas para depois.
- Dados disponíveis, regras de negócio e limitações relevantes.
- Decisões técnicas confirmadas e propostas ainda não decididas.
- Abordagem de implementação escolhida, sua aplicação no projeto ou a decisão ainda pendente.
- Critérios de aceitação e exemplos de resultado esperado.
- Dúvidas que realmente impedem uma decisão importante.

Se uma dúvida impedir definir corretamente o comportamento, pergunte antes de fechar essa parte. As demais seções podem ser redigidas em paralelo como rascunho. Se o usuário preferir avançar com uma hipótese, identifique-a e explique seu efeito.

## 6. Adaptação dos quatro templates

Leia cada template inteiro antes de preencher. Preserve sua finalidade e ajuste a extensão das seções ao projeto. Remova campos repetidos, instruções de preenchimento e exemplos genéricos que não ajudem no caso real. Uma seção pertinente precisa de conteúdo concreto; uma seção que não se aplica pode ser removida ou justificada brevemente.

### PRD.md — problema e produto

Registre contexto, problema, usuários, objetivos e benefício esperado. Descreva a jornada principal, o escopo da primeira versão, as exclusões e os entregáveis. Especifique funcionalidades, regras de negócio, dados e limitações em linguagem compreensível ao responsável pelo produto.

Transforme expressões vagas, como “dashboard intuitivo” ou “análise correta”, em critérios observáveis. Identifique os requisitos para poder relacioná-los à SPEC. Registre decisões pendentes sem tratá-las como aprovadas.

### SPEC.md — comportamento e implementação

Traduza os requisitos do PRD em entradas, saídas, contratos, fórmulas, filtros, relacionamentos e tratamento de erros. Descreva a organização técnica suficiente para a entrega atual e justifique decisões que afetem seu comportamento.

Inclua exemplos com entrada e resultado esperado e uma estratégia de verificação proporcional à solução. Relacione os requisitos e os critérios aos do PRD. Se houver etapas de implementação no template, adapte-as às pequenas partes da entrega, sem antecipar todo o projeto.

A especificação acompanha as descobertas. Uma mudança de regra exige revisar o documento e seus critérios. Não marque como implementado ou verificado algo que foi apenas planejado.

### AGENTS.md — trabalho no repositório

Inclua uma seção “Abordagem de implementação” com a escolha do usuário: SDD, TDD, combinação ou outra. Explique como essa escolha orienta as etapas, a ordem das verificações, a revisão das especificações e as evidências exigidas. Se ainda não houver escolha, registre a pendência sem apresentar uma proposta como decisão confirmada.

Registre documentos a consultar, organização dos arquivos, preparação do ambiente, comandos, convenções de código e verificações. Inclua uma seção de limites e cuidados com os dados adequada ao projeto.

Defina como preservar entradas, registrar impedimentos, conferir resultados e revisar alterações. Quando fizer parte do fluxo acordado, descreva o uso de branches, commits e PRs. Diferencie comandos executados e conferidos daqueles que são apenas propostas ainda não verificadas.

Mantenha as regras de negócio detalhadas no PRD e na SPEC e indique onde consultá-las, evitando cópias que possam divergir.

### CLAUDE.md — orientações para Claude Code

Adapte o documento ao mesmo projeto e oriente a leitura de AGENTS.md, PRD.md e SPEC.md. Acrescente somente as instruções específicas de uso do Claude Code que forem relevantes ao ambiente escolhido.

Não invente ferramentas, integrações, skills ou comandos disponíveis. Evite repetir integralmente AGENTS.md. Se o usuário não utiliza Claude Code, registre que o documento é uma referência opcional para uso futuro e não exige configurar essa ferramenta.

## 7. Regras de qualidade da adaptação

- Use nomes, métricas, exemplos e decisões do caso discutido.
- Não invente pessoas, prazos, campos, credenciais, resultados de testes ou aprovações para preencher uma seção.
- Diferencie informação confirmada, proposta técnica, hipótese e pendência.
- Não invente metas numéricas. Quando não houver uma meta definida, proponha como medir o resultado ou registre a decisão pendente.
- Mantenha a mesma nomenclatura e as mesmas regras nos quatro documentos.
- Confira a relação entre requisito, comportamento especificado e forma de validação.
- Registre limitações dos dados e do ambiente que afetem o resultado esperado.
- Faça os documentos proporcionais à primeira entrega. Eles devem permitir trabalhar, revisar e evoluir a solução.

## 8. Salvamento e entrega

1. Salve as versões adaptadas na pasta do projeto informada pelo usuário. Se o destino não puder ser inferido do contexto, pergunte antes de salvar.
2. Preserve os templates originais desta pasta como modelos reutilizáveis. Se o projeto já tiver documentos preenchidos, leia-os e atualize-os preservando decisões válidas.
3. Entregue os quatro arquivos com os nomes exatos: PRD.md, SPEC.md, AGENTS.md e CLAUDE.md.
4. Confira referências, caminhos, nomes, critérios e consistência entre os arquivos. Não deixe marcadores de preenchimento esquecidos; dúvidas reais devem aparecer como pendências identificadas.
5. Informe onde os arquivos foram salvos, quais decisões importantes foram tomadas e o que ainda precisa de resposta ou verificação.

O brainstorm termina com documentos adequados ao projeto. Inicie a implementação quando ela fizer parte do pedido do usuário.
