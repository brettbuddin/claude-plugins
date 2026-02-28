---
description: >-
  Dispatch the Researcher agent to deeply read and analyze the codebase for a
  given topic. Produces a docs/research/TOPIC.md report.
---

# Research

Dispatch the Researcher agent to produce a research report, then run git history analysis on the key paths it identified.

## Args

`<topic/area description>` (required). If no description is provided, reply with a short usage summary and stop.

## Steps

### Phase 1: Research

1. Use the Task tool with `subagent_type: "Researcher"` and `run_in_background: false`.
2. Prompt the agent with the topic/area description provided by the user.
3. After completion, note the research file path (e.g., `docs/research/TOPIC.md`).

### Phase 2: History

4. Read the research file produced in Phase 1. Extract the key file and directory paths from the **Key Components** and **Architecture** sections.
5. Use the Task tool with `subagent_type: "Historian"` and `run_in_background: false`.
6. Prompt the agent with:
   - The absolute path to the research file.
   - The list of key paths extracted in step 4.

### Wrap-Up

7. Tell the user the research file path and suggest they review it, annotate it if needed and run `/revise-research`, or proceed to `/plan <goal>`.

## Prompting the Agents

When constructing the prompt for the Task tool, include:

- The user's description (Phase 1) or key paths (Phase 2)
- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
