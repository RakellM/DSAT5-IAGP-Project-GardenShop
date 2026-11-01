# PRD — Product Requirements Document

> **Objective:** define the problem, users, objectives, and product requirements before starting implementation.

## 1. Project Identification
- **Project name:** [Name]
- **Document version:** 1.0
- **Status:** Draft
- **Owner:** [Owner]
- **Date:** [YYYY-MM-DD]

## 2. Overview

### 2.1. Context
[Describe the current scenario, the existing process, and the context that motivated the project.]

### 2.2. Problem
[Explain what problem needs to be solved, who is affected, and what the consequences of not solving it are.]

### 2.3. Proposed Solution
[Describe the solution in product terms, without anticipating unnecessary implementation details.]

### 2.4. Value Proposition
[Explain the main benefit the solution will deliver.]

## 3. Objectives and Expected Results

### 3.1. Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

### 3.2. Success Indicators

|Indicator|Current Situation|Target|How to Measure|
|---|---|---|---|
|[Indicator 1]|[Current value]|[Target]|[Method]|
|[Indicator 2]|[Current value]|[Target]|[Method]|

### 3.3. Success Criteria
- [Measurable condition to consider the product successful.]
- [Expected result after deployment.]

## 4. Users and Needs

### 4.1. Target Audience
[Identify the users and their usage contexts.]

### 4.2. User Needs
- As a [user type], I want [need], so that [benefit].
- As a [user type], I want [need], so that [benefit].

### 4.3. Main Journey
1. [How the user starts the process.]
2. [What action they perform.]
3. [What result they receive.]
4. [How they confirm or use the result.]

## 5. Product Scope

### 5.1. Included in Scope
- [Feature or capability 1]
- [Feature or capability 2]
- [Feature or capability 3]

### 5.2. Out of Scope
- [Feature that will not be implemented in this version.]
- [Integration or capability reserved for a future version.]

### 5.3. Assumptions
- [Condition considered true for planning.]
- [Resource, system, or data that will be available.]

### 5.4. Constraints
- **Budget:** [Limits, if applicable.]
- **Deadline:** [Deadline, if applicable.]
- **Infrastructure:** [Available environment.]
- **Technology:** [Technological restrictions.]
- **Operation:** [Other limitations.]

## 6. Functional Requirements

|ID|Requirement|Priority|Acceptance Criteria|
|---|---|---|---|
|FR-001|[The system must...]|Must|[Verifiable condition]|
|FR-002|[The system must...]|Should|[Verifiable condition]|
|FR-003|[The system must...]|Could|[Verifiable condition]|

Suggested priorities: Must (mandatory), Should (important), Could (desirable).

Acceptance criteria should describe observable results, not just intentions.

## 7. Non-Functional Requirements

|ID|Category|Requirement|Verification Criteria|
|---|---|---|---|
|NFR-001|Performance|[Expected response time]|[Test or measurement]|
|NFR-002|Security|[Required access control]|[Verification]|
|NFR-003|Reliability|[Behavior in case of failure]|[Test]|
|NFR-004|Maintainability|[Maintenance requirement]|[Verification]|
|NFR-005|Usability|[Usage need]|[Evaluation]|

Fill in only the categories pertinent to the project.

## 8. Data and Integrations
- **Data sources:** [Files, databases, APIs, or systems.]
- **Inputs:** [Data provided to the product.]
- **Outputs:** [Reports, files, responses, or actions.]
- **Integrations:** [External systems.]
- **Sensitive data:** [Whether they exist and how they should be protected.]
- **Retention and disposal:** [Applicable rules.]

## 9. Business Rules
- **BR-001:** [Business rule.]
- **BR-002:** [Business rule.]
- **BR-003:** [Business rule.]

Rules should be independent of implementation details whenever possible.

## 10. Flows and Exceptions
### 10.1. Main Flow
[Describe the expected path from input to result.]

### 10.2. Alternative Flows
[Describe valid situations different from the main path.]

### 10.3. Error Handling
[Describe expected errors, desired behavior, and relevant messages.]

## 11. Experience and Interface
- **Platform:** [Web, desktop, CLI, API, or other.]
- **Visual references:** [Links or examples, if any.]
- **Accessibility:** [Applicable needs.]
- **Interface states:** [Loading, success, empty, error.]
- **Compatibility:** [Browsers, devices, or environments.]

## 12. Risks and Dependencies

|Risk or Dependency|Impact|Mitigation|
|---|---|---|
|[Description]|[High/Medium/Low]|[Action]|

## 13. Deliverables
- [Application, library, automation, or service.]
- [Required documentation.]
- [Tests and validations.]
- [Installation and execution procedure.]

## 14. Product Completion Criteria
The product will be ready when:
- Mandatory requirements have been implemented.
- Acceptance criteria have been verified.
- Pertinent tests have been run.
- Required documentation is up to date.
- Critical risks have been addressed.
- The execution procedure has been validated.

## 15. Relationship with Technical Documents
- **Reference specification:** `SPEC.md`
- **General instructions for agents:** `AGENTS.md`
- **Instructions for Claude Code:** `CLAUDE.md`

## 16. Pending Decisions

|ID|Question|Owner|Status|
|---|---|---|---|
|PD-001|[Required decision]|[Owner]|Pending|

## 17. Change History

|Version|Date|Change|
|---|---|---|
|1.0|[YYYY-MM-DD]|Initial creation|
