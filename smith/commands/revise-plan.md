---
description: >-
  Re-dispatch the Planner agent to address inline annotations left by the
  reviewer on a docs/plans/GOAL.md file.
---

# Revise Plan

Re-dispatch the Planner agent to address reviewer annotations on a plan.

## Args

None.

## Steps

1. Glob for `docs/plans/*.md` in the working directory. If none exist, tell the user to run `/plan` first and stop.
2. Use the Task tool with `subagent_type: "Planner"` and `run_in_background: false`.
3. Prompt the agent to read the plan file and address any inline annotations from the reviewer.
4. After completion, tell the user the plan has been revised and they can review again, run `/revise-plan` again, or `/implement`.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
