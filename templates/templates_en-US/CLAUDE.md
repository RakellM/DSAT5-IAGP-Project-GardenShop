# CLAUDE.md: Instructions for Claude Code

## 1. Purpose
This file guides Claude Code in understanding, planning, and executing tasks in this repository.

## 2. Mandatory Documents
Before changing code:
- Read `AGENTS.md` and follow its rules.
- Read `PRD.md` to understand the product's objectives and limits.
- Read `SPEC.md` to identify technical requirements and acceptance criteria.
- Consult additional instructions present in the relevant directories.

`SPEC.md` is the reference for approved technical behavior. Do not replace requirements defined in it with your own assumptions.

## 3. How to Act

### 3.1. Explore before implementing
- Inspect the repository structure.
- Identify configuration files, dependencies, entry points, and tests.
- Analyze existing code related to the task.
- Seek to reuse established implementations and patterns.
- Avoid proposing a complete rewrite when a localized change solves the problem.

### 3.2. Plan complex tasks
Before implementing changes involving multiple components, contracts, integrations, or architectural decisions:
1. Summarize the problem.
2. Identify related requirements from `SPEC.md`.
3. Present the proposed approach.
4. Identify affected files and components.
5. Define necessary tests.
6. Highlight ambiguities, risks, and decisions that depend on approval.

For small, unambiguous fixes, proceed directly to implementation, provided it is safe to do so.

### 3.3. Implement incrementally
- Make small, coherent changes.
- Verify the result of each relevant step.
- Avoid modifying files unrelated to the task.
- Preserve the user's pre-existing changes.
- Do not introduce features that were not requested or justified by the specification.
- Do not consider an implementation complete just because the code was written.

## 4. Specification-Driven Development (SDD)
Follow this workflow:
1. **Specify:** understand and refine the requirements in `SPEC.md`.
2. **Plan:** define the technical approach and implementation steps.
3. **Implement:** develop the code according to the approved specification.
4. **Verify:** run tests and check acceptance criteria.
5. **Update:** update documentation and record relevant changes.

### Compliance rules
- Each important feature must be associated with an identifiable requirement.
- Ambiguous requirements must be clarified before high-impact decisions.
- If you discover that the specification is incorrect or incomplete, propose the correction before deviating from it.
- Do not silently change the scope or defined contracts.
- If the implementation reveals an unexpected technical constraint, explain the problem and present alternatives.
- When there is an approved change, keep the specification, code, and tests aligned.

## 5. Command Execution
- Consult the commands documented in `AGENTS.md` and in configuration files.
- Use the existing virtual environment and dependency tools.
- Prefer task-specific commands.
- Do not run destructive commands without authorization.
- Do not install dependencies, change global configurations, or perform deploys without necessity and appropriate authorization.
- If a command fails, examine the cause before trying to work around the problem.
- Do not claim that tests passed without verifying the result.

## 6. Tests and Validation
After implementing:
1. Run the tests related to the change.
2. Run additional pertinent checks, such as lint, formatting, or type checking.
3. Check the acceptance criteria of `SPEC.md`.
4. Verify regressions and possible side effects.
5. Record tests that failed or could not be run.

Add or update tests when necessary to demonstrate the expected behavior.

## 7. Security and Permissions
- Never expose credentials, tokens, or sensitive data.
- Do not remove security mechanisms to facilitate implementation.
- Do not read or change files outside the scope without necessity.
- Do not perform irreversible external actions without authorization.
- Request approval when the task involves relevant risks, data loss, or scope changes.

## 8. Use of Claude Code Tools and Resources
When available and appropriate:
- Use reading tools to understand the code before changing it.
- Use targeted searches to locate implementations and references.
- Use editing tools for localized and reviewable changes.
- Use execution tools to validate actual behavior.
- Use subagents only when the task benefits from clearly delimited parallel work.
- Review changes made by auxiliary agents before integrating them.
- Do not assume that a tool, skill, MCP, or integration is installed: verify its availability.

## 9. Skills, Auxiliary Agents, and Automations
Before creating a skill or auxiliary agent:
- Verify whether an equivalent resource already exists.
- Define a specific responsibility.
- Avoid duplicating instructions from `AGENTS.md`, `SPEC.md`, or this file.
- Document inputs, outputs, limitations, and usage conditions when necessary.

Automations must not perform destructive or external operations without the required permissions.

## 10. Documentation Update
- Update `SPEC.md` when approved changes affect requirements, contracts, or acceptance criteria.
- Update `PRD.md` when there are changes to objectives, target audience, or product scope.
- Update `AGENTS.md` when there are lasting changes to general development conventions.
- Keep this file focused on guidance relevant to Claude Code.
- Do not update documents just to record transient execution details.

## 11. Completion Criteria
Before declaring the task complete, verify:
- The implementation corresponds to the requested requirement.
- The pertinent tests were run.
- Known failures were handled or documented.
- Unrelated changes were avoided.
- Affected documentation was updated.
- The result and its limitations were communicated.

## 12. Final Report
Upon completion, present:

### Implementation
[Summary of changes.]

### Affected Files
[Files created or modified.]

### Validation
[Tests run and observed results.]

### Pending Items
[Limitations, pending decisions, and next steps.]

## 13. Final Rule
Prioritize a correct, verifiable, secure implementation consistent with the specification. If there is a conflict between the fastest solution and the approved requirements, do not sacrifice the requirements without presenting and justifying the decision.
