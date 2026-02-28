---
description: >-
  Re-dispatch the Researcher agent to address inline annotations left by the
  reviewer on a docs/research/TOPIC.md file.
---

# Revise Research

Re-dispatch the Researcher agent to address reviewer annotations on a research report.

## Args

None.

## Steps

1. Glob for `docs/research/*.md` in the working directory. If none exist, tell the user to run `/research` first and stop.
2. Use the Task tool with `subagent_type: "Researcher"` and `run_in_background: false`.
3. Prompt the agent to read the research file and address any inline annotations from the reviewer.
4. After completion, tell the user the research has been revised and they can review again, run `/revise-research` again, or proceed to `/plan <goal>`.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
