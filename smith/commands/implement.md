---
description: >-
  Dispatch the Implementer agent to execute an approved implementation plan
  (notes/plans/GOAL.md).
---

# Implement

Dispatch the Implementer agent to execute an approved plan.

## Args

None.

## Steps

1. Glob for `notes/plans/*.md` in the working directory. If none exist, tell the user to run `/plan` first and stop.
2. Use the Task tool with `subagent_type: "Implementer"`. **Set `run_in_background: false`.**
   The Implementer needs interactive Bash permission prompts, which only work in the foreground.
3. Prompt the agent to execute the plan.
4. After completion, summarize what was done.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
