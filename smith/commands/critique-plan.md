---
description: >-
  Dispatch the Critic agent to critically review a plan, adding inline
  annotations that surface gaps, risks, and unclear reasoning. Run
  /revise-plan afterward to address the annotations.
---

# Critique Plan

Dispatch the Critic agent to review and annotate a plan.

## Args

None.

## Steps

0. Check for `.smith.local.yaml` in the working directory. If it exists, read the `output_directory` value. If absent, default to `docs/`. Use this value wherever `<output_directory>` appears below.
1. Glob for `<output_directory>/plans/*.md` in the working directory. If none exist, tell the user to run `/plan` first and stop.
2. Use the Task tool with `subagent_type: "Critic"` and `run_in_background: false`.
3. Prompt the agent to review the plan file(s) found and add inline annotations.
4. After completion, tell the user the plan has been annotated and suggest they review the annotations, then run `/revise-plan` to have the Planner address them.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
