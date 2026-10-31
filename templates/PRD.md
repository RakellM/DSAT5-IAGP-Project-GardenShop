# PRD: <feature name>

**Author:** <you>
**Status:** Draft · In review · Approved · Shipped
**Last updated:** <date>

## Problem

<One paragraph. What is broken or missing today, and for whom? Use a real
example, not an abstraction. If you can't name who hurts and how, stop here —
you don't have a problem yet.>

## Goals

<What does success look like? Two to four bullets, each a single outcome.>

- <e.g. A person can export their data in under 10 seconds>
- <e.g. Support stops fielding "where's my export" tickets>

## Non-goals

<What you are deliberately NOT doing in this piece of work. This is the most
useful section and the one people skip. It kills scope creep before it starts.>

- <e.g. Scheduled or recurring exports — later>
- <e.g. Exporting other people's data — out of scope>

## User stories

<Who does what, and why. One line each. Keep them small.>

- As a <role>, I want to <action> so that <outcome>.
- As a <role>, I want to <action> so that <outcome>.

## Requirements

<The actual behavior to build. Number them so you can reference them in review
and in tickets. Split must-have from nice-to-have.>

**Must have**

1. <Precise, testable statement. "The export button is disabled while an export
   is running," not "handle concurrent exports gracefully.">
2. <...>

**Nice to have**

- <...>

## Success metrics

<How you'll know it worked, in numbers, after it ships. Name the metric and the
target. If you can't measure it, say how you'll judge it instead.>

- <e.g. 80% of exports complete in under 10s>
- <e.g. Export-related support tickets drop by half within a month>

## Rollout

<How this reaches people. Flag, phased, all at once? What has to be true before
you ship, and what's the plan if it goes wrong?>

- **Ship behind:** <feature flag / percentage rollout / straight to everyone>
- **Before launch:** <docs, migration, comms>
- **Rollback:** <how you turn it off>
