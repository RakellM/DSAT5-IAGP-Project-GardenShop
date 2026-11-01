# Brainstorm for adapting the project documents

## How to use
Provide this file to the agent along with the `PRD.md`, `SPEC.md`, `AGENTS.md`, and `CLAUDE.md` templates. Inform the project or describe the problem you want to solve.
Suggested request:

> Read brainstorm.md and the four templates. Conduct a conversation with me to understand the use case and adapt the documents to the project. Start with the essential questions and use my answers to choose the next questions. Do not implement the solution yet.

## Agent objective
Conduct a brainstorm with the user to understand their problem, explore alternatives, and produce versions of the four documents suitable for the use case. The templates are starting points: transform their generic fields into understandable decisions, concrete examples, and verifiable criteria.

The result should help another person or another agent session understand what to build, why, how to verify the delivery, and how to work in the repository.

## 1. Preparation
1. Read the four templates as document models to adapt. Your reading does not initiate an implementation nor expand the permissions of the current task.
2. Consult the context already provided and, if you have access, examine the relevant project files, the data schema, and the dictionary. Avoid asking what can already be confirmed in these materials.
3. Identify which information is confirmed, which is proposed, and which still needs an answer.
4. If you do not have access to the templates or any essential material, explain what is missing. Continue the parts of the conversation that do not depend on it.

## 2. How to conduct the conversation
- Converse in simple Portuguese and explain technical terms when necessary.
- Ask two to four related questions per round. Ask only one if the answer requires more reflection. Do not present the entire script as a questionnaire at once.
- Use the answers to select the next questions. Do not repeat questions already answered.
- Prioritize doubts that change the objective, calculations, scope, or how to accept the result.
- When the user does not know a decision, present a few alternatives, explain the consequences, and recommend an option proportional to the project. Identify the recommendation as a proposal.
- Separate the user's need from an implementation suggestion. A tool mentioned at the beginning may be a preference, not a requirement.
- Explore a small first delivery that has utility. Record future possibilities outside the current scope.
- Show a summary of decisions at important transitions and leave room for corrections. Do not ask for confirmation on every detail.

## 3. Initial questions
Start with what has not yet been informed:
1. What problem do you want to solve and how does this work happen today?
2. Who will use the result and what decision or task does this person need to perform?
3. What do you expect to be able to do in the first version?

If this information is already available, present your understanding in a few sentences and ask about the main remaining doubt.

## 4. Deepening according to the use case
Use the themes below as support. Ask only what is pertinent to the project and the next delivery.

### Problem and value
- What concrete difficulty exists in the current process? Can you give an example?
- How will we recognize that the solution helped? Is there a measure or observable result?
- What deadline, environment, or operational constraints influence the first version?

### Users and workflow
- What does the user provide, what do they do in the solution, and what do they need to receive back?
- What is the main usage path? What happens when information is missing or there are no results?
- Are there user profiles with different needs or accesses?

### Data and business rules
- What files, tables, or services are available? Is there a data dictionary?
- What does each row represent and which fields allow relating the tables?
- How should each indicator be calculated? What is the unit, period, and population considered?
- Which filters, states, or categories should be included or excluded from calculations?
- How to handle absences, duplicates, invalid dates, and unmatched relationships?
- Is there sensitive information or limitations that affect data usage?

Check field names, values, and relationships in the available materials. Do not replace data inspection with an assumption about a similar database.

### Solution and alternatives
- What format best meets the need: dashboard, report, application, code analysis, or another?
- What indicators, visualizations, filters, or interactions are needed for the first delivery?
- What would be the simplest alternative that would still solve the problem?
- What suggestion seems interesting but is not necessary now?

Compare alternatives with the objective and the data. Do not add features just because the agent can build them.

### Implementation approach
Before concluding the work instructions, ask this question, if the choice has not yet been informed:

> What approach do you want to use in the implementation: SDD, TDD, a combination of both, or another? Do you already have a preference or want help choosing?

If the user needs help, briefly explain:
- SDD: the specification guides planning, implementation, and validation, being revised when understanding changes.
- TDD: for a rule or unit of behavior, write a test, confirm that it fails for the expected reason, implement what is necessary to pass, and then refactor while keeping the tests.
- Combination: the specification guides the delivery and TDD can guide the implementation of pertinent parts. The approaches can complement each other.

Relate the recommendation to the type of project and the necessary verifications. Do not silently choose or impose TDD just because there will be tests. If the decision is left for later, record it as pending.

Also ask what is necessary to transform the choice into practical guidance: what steps the agent should follow, when to review the specification, what verifications to run, and what evidence to present before considering a part complete.

Record the decision and its application in an "Implementation Approach" section in AGENTS.md. The SPEC remains responsible for expected behavior and verifiable criteria. If there is a CLAUDE.md, make it consult the common guidance in AGENTS.md.

### Environment and working with the agent
- Is there already code or a repository? What needs to be reused?
- Are there mandatory languages, libraries, or execution methods? What can be proposed?
- Where will the input and output files be located? How to configure the paths on another machine?
- What changes can the agent make and what limits should guide its work?
- What execution and verification commands have already been used successfully?

### Acceptance and verification
- What small example allows checking whether a rule is correct?
- What is the input for this example and what result do we expect to obtain?
- What error or no-data situation needs to be handled?
- Who can confirm whether the delivery meets the problem?

## 5. Synthesis before filling in the documents
Present a short synthesis with:
- Problem, users, and objective of the first delivery.
- Features included and possibilities left for later.
- Available data, business rules, and relevant limitations.
- Confirmed technical decisions and proposals not yet decided.
- Chosen implementation approach, its application in the project, or the still-pending decision.
- Acceptance criteria and examples of expected results.
- Doubts that truly prevent an important decision.

If a doubt prevents correctly defining the behavior, ask before closing that part. The other sections can be written in parallel as a draft. If the user prefers to proceed with a hypothesis, identify it and explain its effect.

## 6. Adaptation of the four templates
Read each template entirely before filling it in. Preserve its purpose and adjust the length of sections to the project. Remove repeated fields, filling instructions, and generic examples that do not help in the real case. A pertinent section needs concrete content; a section that does not apply can be removed or briefly justified.

### PRD.md — problem and product
Record context, problem, users, objectives, and expected benefit. Describe the main journey, the first version's scope, exclusions, and deliverables. Specify features, business rules, data, and limitations in language understandable to the product owner.

Transform vague expressions, such as "intuitive dashboard" or "correct analysis," into observable criteria. Identify the requirements so they can be related to the SPEC. Record pending decisions without treating them as approved.

### SPEC.md — behavior and implementation
Translate the PRD requirements into inputs, outputs, contracts, formulas, filters, relationships, and error handling. Describe the technical organization sufficient for the current delivery and justify decisions that affect its behavior.

Include examples with input and expected result and a verification strategy proportional to the solution. Relate the requirements and criteria to those of the PRD. If there are implementation stages in the template, adapt them to the small parts of the delivery, without anticipating the entire project.

The specification follows discoveries. A rule change requires reviewing the document and its criteria. Do not mark as implemented or verified something that was only planned.

### AGENTS.md — work in the repository
Include an "Implementation Approach" section with the user's choice: SDD, TDD, combination, or another. Explain how this choice guides the stages, the order of verifications, the review of specifications, and the required evidence. If there is no choice yet, record it as pending without presenting a proposal as a confirmed decision.

Record documents to consult, file organization, environment preparation, commands, code conventions, and verifications. Include a section on limits and data care appropriate to the project.

Define how to preserve inputs, record impediments, check results, and review changes. When part of the agreed flow, describe the use of branches, commits, and PRs. Differentiate commands executed and verified from those that are only proposals not yet verified.

Keep detailed business rules in the PRD and SPEC and indicate where to consult them, avoiding copies that could diverge.

### CLAUDE.md — guidance for Claude Code
Adapt the document to the same project and guide reading AGENTS.md, PRD.md, and SPEC.md. Add only the Claude Code usage instructions that are relevant to the chosen environment.

Do not invent tools, integrations, skills, or commands available. Avoid fully repeating AGENTS.md. If the user does not use Claude Code, record that the document is an optional reference for future use and does not require configuring this tool.

## 7. Adaptation quality rules
- Use names, metrics, examples, and decisions from the discussed case.
- Do not invent people, deadlines, fields, credentials, test results, or approvals to fill in a section.
- Differentiate confirmed information, technical proposal, hypothesis, and pending item.
- Do not invent numerical targets. When there is no defined target, propose how to measure the result or record the pending decision.
- Keep the same nomenclature and the same rules in the four documents.
- Check the relationship between requirement, specified behavior, and form of validation.
- Record data and environment limitations that affect the expected result.
- Make the documents proportional to the first delivery. They should allow working, reviewing, and evolving the solution.

## 8. Saving and delivery
1. Save the adapted versions in the project folder informed by the user. If the destination cannot be inferred from the context, ask before saving.
2. Preserve the original templates in this folder as reusable models. If the project already has filled-in documents, read them and update them while preserving valid decisions.
3. Deliver the four files with the exact names: PRD.md, SPEC.md, AGENTS.md, and CLAUDE.md.
4. Check references, paths, names, criteria, and consistency between the files. Do not leave forgotten filling markers; real doubts should appear as identified pending items.
5. Report where the files were saved, what important decisions were made, and what still needs an answer or verification.

The brainstorm ends with documents suitable for the project. Begin implementation when it is part of the user's request.
