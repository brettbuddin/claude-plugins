---
description: >-
  Dispatch the Reporter agent to synthesize research and plan documents
  into an RFD-style document at notes/report/REPORT_TOPIC.md.
---

# Report

Dispatch the Reporter agent to produce an RFD-style document.

## Args

`<topic description>` (optional). If no description is provided and multiple research files exist, reply with a short usage summary listing available topics and stop. If exactly one research file exists, use it automatically.

## Steps

1. Glob for `notes/research/*.md` in the working directory. If none exist, tell the user to run `/research` first and stop.
2. If a topic description was provided, match it to the appropriate research file. If ambiguous, list matches and stop.
3. If no topic description was provided and exactly one research file exists, use it. If multiple exist, list them and stop.
4. Glob for `notes/plans/*.md`. If none exist, tell the user to run `/plan` first and stop. By default, use the most recently modified plan. If the user requests specific plans, use those. If multiple plans exist and the user did not specify which to use, the agent will disambiguate.
5. Use the Task tool with `subagent_type: "Reporter"` and `run_in_background: false`.
6. Prompt the agent with the selected research topic and plan file path(s).
7. After completion, tell the user the report file path and suggest they review it, annotate it if needed and run `/revise-report`, or share it with stakeholders.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The selected research topic or file path
- The specific plan file path(s) to synthesize (e.g., `notes/plans/goal-name.md`)
- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
