---
description: >-
  Dispatch the Planner agent to produce a detailed implementation plan from
  research findings. Produces a notes/plans/GOAL.md file.
---

# Plan

Dispatch the Planner agent to produce an implementation plan.

## Args

`<specific goal description>` (required). If no description is provided, reply with a short usage summary and stop.

## Steps

1. Glob for `notes/research/*.md` in the working directory.
2. Use the Task tool with `subagent_type: "Planner"` and `run_in_background: false`.
3. Prompt the agent with:
   - The specific goal description provided by the user
   - Which research file(s) exist (let the planner pick the right one per its own instructions)
4. After completion, tell the user the plan file path (which will be `notes/plans/GOAL.md`) and suggest they review/annotate it, then run `/revise-plan` or `/implement`.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The user's description
- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
