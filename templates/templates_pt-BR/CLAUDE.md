# CLAUDE.md — Instruções para Claude Code

## 1. Objetivo

Este arquivo orienta o Claude Code na compreensão, no planejamento e na execução de tarefas neste repositório.

## 2. Documentos obrigatórios

Antes de alterar o código:

- Leia `AGENTS.md` e siga suas regras.
- Leia `PRD.md` para compreender os objetivos e os limites do produto.
- Leia `SPEC.md` para identificar os requisitos técnicos e os critérios de aceitação.
- Consulte instruções adicionais presentes nos diretórios relevantes.

O `SPEC.md` é a referência para o comportamento técnico aprovado. Não substitua requisitos definidos nele por suposições próprias.

## 3. Forma de atuação

### 3.1. Explore antes de implementar

- Inspecione a estrutura do repositório.
- Identifique arquivos de configuração, dependências, pontos de entrada e testes.
- Analise o código existente relacionado à tarefa.
- Procure reutilizar implementações e padrões já estabelecidos.
- Evite propor uma reescrita completa quando uma alteração localizada resolver o problema.

### 3.2. Planeje tarefas complexas

Antes de implementar mudanças que envolvam vários componentes, contratos, integrações ou decisões arquiteturais:

1. Resuma o problema.
2. Identifique os requisitos relacionados da `SPEC.md`.
3. Apresente a abordagem proposta.
4. Identifique os arquivos e componentes afetados.
5. Defina os testes necessários.
6. Destaque ambiguidades, riscos e decisões que dependem de aprovação.

Para correções pequenas e inequívocas, siga diretamente para a implementação, desde que seja seguro fazê-lo.

### 3.3. Implemente incrementalmente

- Faça alterações pequenas e coerentes.
- Verifique o resultado de cada etapa relevante.
- Evite modificar arquivos sem relação com a tarefa.
- Preserve as alterações preexistentes do usuário.
- Não introduza funcionalidades que não tenham sido solicitadas ou justificadas pela especificação.
- Não considere uma implementação concluída apenas porque o código foi escrito.

## 4. Desenvolvimento orientado a especificações (SDD)

Siga este fluxo de trabalho:

1. **Specify:** compreenda e refine os requisitos em `SPEC.md`.
2. **Plan:** defina a abordagem técnica e as etapas de implementação.
3. **Implement:** desenvolva o código de acordo com a especificação aprovada.
4. **Verify:** execute os testes e confira os critérios de aceitação.
5. **Update:** atualize a documentação e registre mudanças relevantes.

### Regras de conformidade

- Cada funcionalidade importante deve estar associada a um requisito identificável.
- Requisitos ambíguos devem ser esclarecidos antes de decisões de alto impacto.
- Se descobrir que a especificação está incorreta ou incompleta, proponha a correção antes de desviar dela.
- Não altere silenciosamente o escopo ou os contratos definidos.
- Se a implementação revelar uma restrição técnica inesperada, explique o problema e apresente alternativas.
- Quando houver mudança aprovada, mantenha a especificação, o código e os testes alinhados.

## 5. Execução de comandos

- Consulte os comandos documentados em `AGENTS.md` e nos arquivos de configuração.
- Utilize o ambiente virtual e as ferramentas de dependências existentes.
- Prefira comandos específicos à tarefa.
- Não execute comandos destrutivos sem autorização.
- Não instale dependências, altere configurações globais ou realize deploys sem necessidade e autorização adequadas.
- Se um comando falhar, examine a causa antes de tentar contornar o problema.
- Não afirme que testes passaram sem verificar o resultado.

## 6. Testes e validação

Após implementar:

1. Execute os testes relacionados à alteração.
2. Execute verificações adicionais pertinentes, como lint, formatação ou checagem de tipos.
3. Confira os critérios de aceitação da `SPEC.md`.
4. Verifique regressões e possíveis efeitos colaterais.
5. Registre os testes que falharam ou não puderam ser executados.

Adicione ou atualize testes quando necessário para demonstrar o comportamento esperado.

## 7. Segurança e permissões

- Nunca exponha credenciais, tokens ou dados sensíveis.
- Não remova mecanismos de segurança para facilitar a implementação.
- Não leia ou altere arquivos fora do escopo sem necessidade.
- Não execute ações externas irreversíveis sem autorização.
- Solicite aprovação quando a tarefa envolver riscos relevantes, perda de dados ou mudanças de escopo.

## 8. Uso de ferramentas e recursos do Claude Code

Quando disponíveis e apropriados:

- Utilize ferramentas de leitura para compreender o código antes de alterá-lo.
- Utilize buscas direcionadas para localizar implementações e referências.
- Utilize ferramentas de edição para mudanças localizadas e revisáveis.
- Utilize ferramentas de execução para validar o comportamento real.
- Utilize subagentes apenas quando a tarefa se beneficiar de trabalho paralelo claramente delimitado.
- Revise as alterações feitas por agentes auxiliares antes de integrá-las.
- Não presuma que uma ferramenta, skill, MCP ou integração esteja instalada: verifique sua disponibilidade.

## 9. Skills, agentes auxiliares e automações

Antes de criar uma skill ou um agente auxiliar:

- Verifique se já existe um recurso equivalente.
- Defina uma responsabilidade específica.
- Evite duplicar instruções de `AGENTS.md`, `SPEC.md` ou deste arquivo.
- Documente entradas, saídas, limitações e condições de uso quando necessário.

Automatizações não devem executar operações destrutivas ou externas sem as permissões exigidas.

## 10. Atualização da documentação

- Atualize `SPEC.md` quando mudanças aprovadas afetarem requisitos, contratos ou critérios de aceitação.
- Atualize `PRD.md` quando houver mudanças nos objetivos, no público-alvo ou no escopo do produto.
- Atualize `AGENTS.md` quando houver alterações duradouras nas convenções gerais de desenvolvimento.
- Mantenha este arquivo concentrado nas orientações relevantes para Claude Code.
- Não atualize documentos apenas para registrar detalhes transitórios da execução.

## 11. Critérios de conclusão

Antes de declarar a tarefa concluída, verifique:

- A implementação corresponde ao requisito solicitado.
- Os testes pertinentes foram executados.
- As falhas conhecidas foram tratadas ou documentadas.
- As alterações não relacionadas foram evitadas.
- A documentação afetada foi atualizada.
- O resultado e suas limitações foram comunicados.

## 12. Relatório final

Ao concluir, apresente:

### Implementação

[Resumo das alterações.]

### Arquivos afetados

[Arquivos criados ou modificados.]

### Validação

[Testes executados e resultados observados.]

### Pendências

[Limitações, decisões pendentes e próximos passos.]

## 13. Regra final

Priorize uma implementação correta, verificável, segura e consistente com a especificação. Se houver conflito entre a solução mais rápida e os requisitos aprovados, não sacrifique os requisitos sem apresentar e justificar a decisão.
