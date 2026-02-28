---
description: >-
  Re-dispatch the Reporter agent to address inline annotations left
  by the reviewer on a docs/reports/*.md file.
---

# Revise Report

Re-dispatch the Reporter agent to address reviewer annotations on an RFD document.

## Args

None.

## Steps

1. Glob for `docs/reports/*.md` in the working directory. If none exist, tell the user to run `/report` first and stop.
2. Use the Task tool with `subagent_type: "Reporter"` and `run_in_background: false`.
3. Prompt the agent to read the report file and address any inline annotations from the reviewer.
4. After completion, tell the user the report has been revised and they can review again or run `/revise-report` again.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
