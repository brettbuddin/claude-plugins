---
description: >-
  Dispatch the Researcher agent to deeply read and analyze the codebase for a
  given topic. Produces a notes/research/TOPIC.md report.
---

# Research

Dispatch the Researcher agent to produce a research report.

## Args

`<topic/area description>` (required). If no description is provided, reply with a short usage summary and stop.

## Steps

1. Use the Task tool with `subagent_type: "Researcher"` and `run_in_background: false`.
2. Prompt the agent with the topic/area description provided by the user.
3. After completion, tell the user the research file path and suggest they review it, annotate it if needed and run `/revise-research`, or proceed to `/plan <goal>`.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The user's description
- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
