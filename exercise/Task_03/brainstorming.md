# Brainstorm to help create the skill

## How to use

Provide the agent with the three files in this folder: problema.md, brainstorm.md, and SKILL.md. The problem describes the initial objective; this script guides the conversation; SKILL.md is the template that will be adapted. Inform the project folder and the data source, when available.

Suggested request:

> Read problema.md, brainstorm.md, and the SKILL.md template. Help me create a skill for the problem presented. Ask questions about the use case, the data, the rules, the tools, and the expected result. After clarifying the essential decisions, create the adapted skill and the necessary resources in the project. Start with the conversation, without inventing decisions to fill in the template.

## Agent objective

Help the user transform the problem described in problema.md into a reusable skill. The initial case in this folder is a copilot for data analysis. The skill should explain when to act, what information to use, how to execute the work, and how to recognize a correct delivery.

The template is generic to allow adaptation. The final skill should be specific and useful for the chosen task. Do not produce just a file with phrases like "follow best practices" or "do it correctly."

## 1. Preparation

1. Read problema.md to understand the objective and SKILL.md to learn the template. Consult the context already provided by the user. Use the problem as a starting point, without confusing it with a ready-made skill or with all decisions already resolved.
2. Consult the instructions applicable to the project and the relevant materials, when available.
3. Identify what is already confirmed, what can be proposed, and what requires a response from the user.
4. Check which tools and resources exist in the environment. The skill guides their use, but does not grant access or install dependencies by itself.
5. If any essential material is not accessible, explain the impediment. Continue the parts of the discussion that do not depend on it.

## 2. How to conduct the conversation

- Use simple Portuguese and explain technical terms when necessary.
- Ask two to four related questions per round. Ask only one when the answer requires more reflection.
- Use the answers to choose the next topic. Do not send this entire script as a single questionnaire at once.
- Avoid asking for information that is already clear in the request or in the available materials.
- Explore alternatives when there is a real decision, explain their consequences, and identify your recommendation as a proposal.
- Prioritize doubts that change the execution or the way the result is accepted.
- Keep a first version small that solves the task. Leave future improvements out of the current scope.
- Present short summaries at important transitions and leave room for corrections, without asking for confirmation on every detail.

## 3. Initial questions

Start with what has not yet been informed:

1. What task do you want to repeat with the help of the skill, and who will use it?
2. In which situations should it act? Give an example of a real request.
3. What do you expect to receive as a result, and how will you know it is correct?

If these answers are already available, summarize your understanding and ask about the main remaining doubt.

## 4. Deepening according to the use case

### Task and scope

- How does this work happen today? What knowledge or procedure usually needs to be explained again?
- What goes into the first version, and what should be left for later?
- Is there a similar task where this skill should not be used?

### Inputs

- What information, files, or parameters does the user need to provide?
- Which inputs are mandatory? Are there already agreed default values?
- How do you recognize a missing, invalid, or incompatible input?
- Where are the materials located, and how do you inform their path or address?

### Rules and domain knowledge

- Which decisions or conventions change the way the task is executed?
- Is there a dictionary, manual, standard, or other relevant reference?
- Which exceptions really matter for the first delivery?
- Which terms may be ambiguous and need a definition?

Check the rules in the available materials. Do not invent requirements, fields, formulas, or decisions to complete the template.

### Output and acceptance

- What content does the user need to receive, and in what format?
- If there are files, where should they be saved, and how should an existing output be handled?
- What small example allows comparing the expected result with the obtained one?
- What evidence helps verify the delivery without relying only on the agent's statement?

### Execution and tools

- Can the task be performed with the instructions and tools already available?
- Does any operation require code, file access, a browser, an API, or another resource?
- If there is code, what dependencies and commands are needed? What has already been executed and checked?
- Would a repeated step benefit from a reusable script?
- What concrete limits must be respected during execution?

Do not assume that every skill needs scripts, Python, MCP, internet access, or external services. Choose resources based on the task and the user's environment. If there is a code implementation, clarify the work process only to the extent necessary for the project and the existing instructions.

### Behavior verification

- Which normal request should activate the skill and produce a known result?
- Which missing or invalid input allows checking the handling of a problem?
- Which out-of-scope request allows checking whether the skill is being selected excessively?
- Which aspects of the result require an independent comparison or human review?

## 5. Synthesis before adapting the template

Present:

- Task, audience, conditions of use, and limits.
- Inputs, rules, and confirmed references.
- Output, destination, and acceptance criteria.
- Proposed procedure and tools actually needed.
- Test cases and expected results.
- Pending decisions that affect execution.

Ask before closing a part that depends on critical information. The others can be written as a draft. Identify hypotheses and proposals without presenting them as confirmed decisions.

## 6. Creating the skill with support from the template

After clarifying the essential decisions, produce the skill files in the chosen project. Do not limit yourself to returning questions or copying the template with open fields. If a part depends on critical information that is still missing, identify the pending item and proceed only with what does not depend on it.

1. Choose a short name using lowercase letters, numbers, and hyphens. Use the same name in the name field and in the skill folder.
2. Write a specific description, indicating the task and when to apply it. This field helps with skill selection.
3. Fill in the body with the inputs, rules, steps, and criteria discussed. Include only details that help the agent execute the task.
4. Replace all fields in square brackets and remove the filling comments. Do not leave generic template instructions in the final skill.
5. Remove sections and lines that do not apply. A complete template does not require a long skill.
6. Place extensive documentation in references/, reusable code in scripts/, and output templates in assets/, only when these resources are necessary.
7. Use valid relative references and explain when to consult each resource. Do not create empty folders or links to nonexistent files.
8. Take advantage of existing project resources and conventions. Keep general guidelines in AGENTS.md, when present, avoiding copies that may diverge.

## 7. Tests and review

Check the file structure and the skill's behavior separately. A valid name and correct YAML do not prove that the procedure works.

In the authorized environment, run the pertinent cases and compare the results with the agreed criteria. Test explicit selection and, when the tool allows it, automatic selection. Include an out-of-scope request.

If there is new code, verify its execution and important behaviors. If the task does not use code, check the results using criteria appropriate to the type of delivery.

Fix the cause of failures and repeat the affected checks. Identify passed, failed, and not verified. Do not report a planned verification as executed.

## 8. Saving and delivery

- Preserve problema.md, brainstorm.md, and SKILL.md in this folder as authoring materials. Save the adapted skill in the project folder, keeping the mandatory SKILL.md name in the final package.
- Check the discovery directory of the chosen tool. In the local project examples from the class, use .agents/skills/skill-name/ in Codex or .claude/skills/skill-name/ in Claude Code.
- If the project or destination cannot be inferred, ask before saving.
- Deliver SKILL.md and only the resources that support its operation, with instructions for use and verification.
- Report the files, decisions, evidence, and relevant pending items. Use the repository's review flow when it is part of the activity.

The result is a skill created for the concrete case, with the necessary resources and identified verifications, that another person can use and check. These authoring files do not need to be copied into the installed skill, unless one of them has a concrete function in the final procedure.
