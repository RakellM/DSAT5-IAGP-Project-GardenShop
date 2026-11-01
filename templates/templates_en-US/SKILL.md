\---

name: skill-name

description: "\[Describe the specific task this skill performs and the situations in which it should be used.]"

\---



\# \[Skill name]



<!-- TEMPLATE TO ADAPT: replace the bracketed fields and remove comments and optional sections that are not useful. The name in the YAML must match the skill folder name. This file is an authoring template; copying it to templates/ does not install a skill. -->



\## 1. Task and expected result



Perform \[delimited task] for \[user or context], producing \[observable result].



\- \*\*Objective:\*\* \[What need the task addresses.]

\- \*\*Included:\*\* \[Which operations are part of the first version.]

\- \*\*Out of scope:\*\* \[Limits that help avoid misinterpretations, if necessary.]



\## 2. When to use



Use this skill when \[specific condition of use related to the task].



\[If there are very similar tasks, explain the distinction needed to choose this skill correctly. Avoid describing the skill as a solution for any request.]



\## 3. Inputs



| Input | Format or source | Required | How to use or validate |

| --- | --- | --- | --- |

| \[Main input] | \[Text, file, parameter, service, or other format] | \[Yes or no] | \[Validation rule] |

| \[Additional input, if necessary] | \[Format or source] | \[Yes or no] | \[Rule or default value explicitly agreed upon] |



When an input that changes the result is missing, \[question or action required]. For an invalid input, \[how to explain the problem or proceed without compromising the result].



\## 4. Output



\- \*\*Deliverable:\*\* \[Content that must be presented or produced.]

\- \*\*Format:\*\* \[Text, file, table, image, code change, or other.]

\- \*\*Destination:\*\* \[Location or way to define the destination with the user, if there is a file.]

\- \*\*Evidence:\*\* \[What allows the task to be checked: calculation, excerpt, reference, execution, or appropriate inspection.]



\[Define units, names, structure, or output conventions only when they matter to the recipient of the deliverable.]



\## 5. Task-specific rules



1\. \[Domain rule that changes how the agent must perform the task.]

2\. \[Restriction or convention needed to interpret inputs or produce the output.]

3\. \[Handling of a relevant exception, if any.]



\[For extensive rules, keep only the consultation guidance here and use a real relative reference. Do not duplicate the same rule across multiple files.]



\## 6. Procedure



\### Understand the request



1\. Identify \[objective, parameters, and relevant information from the request].

2\. Check the inputs and consult \[necessary documents or references].

3\. Resolve ambiguities that change the result. Use \[agreed default], when applicable, and state its use.



\### Perform the task



4\. \[Concrete action needed to produce the result.]

5\. \[Next action or relevant decision.]

6\. \[How to use a tool, script, or resource, if the task needs them. Otherwise, remove this step.]



\### Check the result



7\. Compare \[verifiable part of the output] with \[criterion, known example, or reference source].

8\. Check \[another aspect relevant to the quality of this task].

9\. If there is a discrepancy, identify the cause and \[corrective action]. Repeat the affected check. When it cannot be resolved, report the impediment and what remained unverified.



\### Deliver



10\. Present \[result and explanation needed by the user] in the defined format.

11\. State \[decisions, limitations, or pending items that affect the use of the deliverable].



\## 7. Supporting resources



<!-- If the skill does not need additional resources, remove this section. Create only the necessary files and replace the paths below with the real ones. -->



\- \*\*References:\*\* \[Relative link to rules or documentation] — consult when \[condition].

\- \*\*Scripts:\*\* \[Relative path to reusable code] — run when \[concrete need].

\- \*\*Assets:\*\* \[Path to template or file used in the deliverable] — use in \[part of the task].



Resolve resource paths from the skill folder. \[If inputs or outputs are outside that folder, explain how to provide their paths without depending on the author's machine.]



\## 8. Environment and tools



<!-- Remove what does not apply. A skill can work with only instructions and already available tools. Code, Python, MCP, or an API are not mandatory. -->



\- \*\*Required tools:\*\* \[Capabilities actually required by the task.]

\- \*\*Dependencies:\*\* \[Programs, libraries, or services, when necessary.]

\- \*\*Execution:\*\* \[Command or way to use, with inputs and parameters explained.]

\- \*\*If the resource is unavailable:\*\* \[How to report the impediment or use an appropriate and authorized alternative.]



Do not describe an operation as executed when it was only proposed. \[If there is a calculation or execution, specify the evidence the user must receive.]



\## 9. Scope limits



\- \*\*Preserve:\*\* \[Files, content, or decisions that this task must maintain.]

\- \*\*Expected changes:\*\* \[What executing this task may modify within the received request.]

\- \*\*Decisions to clarify:\*\* \[Questions that need an answer before a relevant action.]



\[Include only concrete limits of the task. The skill text does not replace environment permissions nor expand the user's request. If the project has an AGENTS.md, consult the applicable general rules, avoiding unnecessary copies.]



\## 10. Completion criteria



Consider the task complete when:



\- \[Observable criterion about the content or behavior of the deliverable.]

\- \[Relevant check performed and its result verified.]

\- \[File or response produced in the expected format and destination.]



If a criterion cannot be verified, state that limitation without presenting it as met.



\## 11. Usage examples



\### Relevant request



> \[Realistic request in which the skill should be used, with sufficient inputs.]



\*\*Expected result:\*\* \[Observable characteristics of the response or the file produced.]



\### Missing or invalid input



> \[Request that allows checking the handling of a relevant failure.]



\*\*Expected behavior:\*\* \[Question, message, or decision appropriate to the situation.]



\### Out-of-scope request



> \[Nearby request that does not need this skill.]



\*\*Expected behavior:\*\* \[How to recognize that this skill's procedure does not apply.]



<!-- Review the final length: extensive examples and test sets can go in supporting files, if necessary. The final version should contain what helps another agent perform the specific task, without carrying this entire filling-in guide. -->



