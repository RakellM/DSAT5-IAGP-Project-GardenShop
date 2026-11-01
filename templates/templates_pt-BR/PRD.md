# PRD — Product Requirements Document

> **Objetivo:** definir o problema, os usuários, os objetivos e os requisitos do produto antes de iniciar a implementação.

## 1. Identificação do projeto

- **Nome do projeto:** [Nome]
- **Versão do documento:** 1.0
- **Status:** Rascunho
- **Responsável:** [Responsável]
- **Data:** [AAAA-MM-DD]

## 2. Visão geral

### 2.1. Contexto

[Descreva o cenário atual, o processo existente e o contexto que motivou o projeto.]

### 2.2. Problema

[Explique qual problema precisa ser resolvido, quem é afetado e quais são as consequências de não resolvê-lo.]

### 2.3. Solução proposta

[Descreva a solução em termos de produto, sem antecipar detalhes desnecessários de implementação.]

### 2.4. Proposta de valor

[Explique o benefício principal que a solução entregará.]

## 3. Objetivos e resultados esperados

### 3.1. Objetivos

- [Objetivo 1]
- [Objetivo 2]
- [Objetivo 3]

### 3.2. Indicadores de sucesso

| Indicador     | Situação atual | Meta   | Como medir |
| ------------- | -------------- | ------ | ---------- |
| [Indicador 1] | [Valor atual]  | [Meta] | [Método]   |
| [Indicador 2] | [Valor atual]  | [Meta] | [Método]   |

### 3.3. Critérios de sucesso

- [Condição mensurável para considerar o produto bem-sucedido.]
- [Resultado esperado após a implantação.]

## 4. Usuários e necessidades

### 4.1. Público-alvo

[Identifique os usuários e seus contextos de utilização.]

### 4.2. Necessidades dos usuários

- Como [tipo de usuário], quero [necessidade], para [benefício].
- Como [tipo de usuário], quero [necessidade], para [benefício].

### 4.3. Jornada principal

1. [Como o usuário inicia o processo.]
2. [Qual ação realiza.]
3. [Qual resultado recebe.]
4. [Como confirma ou utiliza o resultado.]

## 5. Escopo do produto

### 5.1. Incluído no escopo

- [Funcionalidade ou capacidade 1]
- [Funcionalidade ou capacidade 2]
- [Funcionalidade ou capacidade 3]

### 5.2. Fora do escopo

- [Funcionalidade que não será implementada nesta versão.]
- [Integração ou capacidade reservada para uma versão futura.]

### 5.3. Premissas

- [Condição considerada verdadeira para o planejamento.]
- [Recurso, sistema ou dado que estará disponível.]

### 5.4. Restrições

- **Orçamento:** [Limites, se aplicável.]
- **Prazo:** [Prazo, se aplicável.]
- **Infraestrutura:** [Ambiente disponível.]
- **Tecnologia:** [Restrições tecnológicas.]
- **Operação:** [Outras limitações.]

## 6. Requisitos funcionais

| ID     | Requisito           | Prioridade | Critério de aceitação  |
| ------ | ------------------- | ---------- | ---------------------- |
| RF-001 | [O sistema deve...] | Must       | [Condição verificável] |
| RF-002 | [O sistema deve...] | Should     | [Condição verificável] |
| RF-003 | [O sistema deve...] | Could      | [Condição verificável] |

Prioridades sugeridas: Must (obrigatório), Should (importante), Could (desejável).

Os critérios de aceitação devem descrever resultados observáveis, não apenas intenções.

## 7. Requisitos não funcionais

| ID      | Categoria        | Requisito                        | Critério de verificação |
| ------- | ---------------- | -------------------------------- | ----------------------- |
| RNF-001 | Desempenho       | [Tempo de resposta esperado]     | [Teste ou medição]      |
| RNF-002 | Segurança        | [Controle de acesso necessário]  | [Verificação]           |
| RNF-003 | Confiabilidade   | [Comportamento em caso de falha] | [Teste]                 |
| RNF-004 | Manutenibilidade | [Requisito de manutenção]        | [Verificação]           |
| RNF-005 | Usabilidade      | [Necessidade de uso]             | [Avaliação]             |

Preencha somente as categorias pertinentes ao projeto.

## 8. Dados e integrações

- **Fontes de dados:** [Arquivos, bancos, APIs ou sistemas.]
- **Entradas:** [Dados fornecidos ao produto.]
- **Saídas:** [Relatórios, arquivos, respostas ou ações.]
- **Integrações:** [Sistemas externos.]
- **Dados sensíveis:** [Se existem e como devem ser protegidos.]
- **Retenção e descarte:** [Regras aplicáveis.]

## 9. Regras de negócio

- **RN-001:** [Regra de negócio.]
- **RN-002:** [Regra de negócio.]
- **RN-003:** [Regra de negócio.]

As regras devem ser independentes dos detalhes de implementação sempre que possível.

## 10. Fluxos e exceções

### 10.1. Fluxo principal

[Descreva o caminho esperado desde a entrada até o resultado.]

### 10.2. Fluxos alternativos

[Descreva situações válidas diferentes do caminho principal.]

### 10.3. Tratamento de erros

[Descreva erros esperados, comportamento desejado e mensagens relevantes.]

## 11. Experiência e interface

- **Plataforma:** [Web, desktop, CLI, API ou outra.]
- **Referências visuais:** [Links ou exemplos, se houver.]
- **Acessibilidade:** [Necessidades aplicáveis.]
- **Estados da interface:** [Carregamento, sucesso, vazio, erro.]
- **Compatibilidade:** [Navegadores, dispositivos ou ambientes.]

## 12. Riscos e dependências

| Risco ou dependência | Impacto            | Mitigação |
| -------------------- | ------------------ | --------- |
| [Descrição]          | [Alto/Médio/Baixo] | [Ação]    |

## 13. Entregáveis

- [Aplicação, biblioteca, automação ou serviço.]
- [Documentação necessária.]
- [Testes e validações.]
- [Procedimento de instalação e execução.]

## 14. Critérios de conclusão do produto

O produto estará pronto quando:

- Os requisitos obrigatórios tiverem sido implementados.
- Os critérios de aceitação tiverem sido verificados.
- Os testes pertinentes tiverem sido executados.
- A documentação necessária estiver atualizada.
- Os riscos críticos tiverem sido tratados.
- O procedimento de execução tiver sido validado.

## 15. Relação com os documentos técnicos

- **Especificação de referência:** `SPEC.md`
- **Instruções gerais para agentes:** `AGENTS.md`
- **Instruções para Claude Code:** `CLAUDE.md`

## 16. Decisões pendentes

| ID     | Questão              | Responsável   | Status   |
| ------ | -------------------- | ------------- | -------- |
| DP-001 | [Decisão necessária] | [Responsável] | Pendente |

## 17. Histórico de alterações

| Versão | Data         | Alteração       |
| ------ | ------------ | --------------- |
| 1.0    | [AAAA-MM-DD] | Criação inicial |
