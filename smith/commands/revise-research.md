---
description: >-
  Re-dispatch the Researcher agent to address inline annotations left by the
  reviewer on an <output_directory>/research/TOPIC.md file.
---

# Revise Research

Re-dispatch the Researcher agent to address reviewer annotations on a research report.

## Args

None.

## Steps

### Configuration

0. Use the `smith:config` skill to read project configuration. Use the `output_directory` value (default: `docs/`) wherever `<output_directory>` appears below.

### Phase 1: Revise Research

1. Glob for `<output_directory>/research/*.md` in the working directory. If none exist, tell the user to run `/research` first and stop.
2. Use the Task tool with `subagent_type: "Researcher"` and `run_in_background: false`.
3. Prompt the agent to read the research file and address any inline annotations from the reviewer.

### Phase 2: Re-run Historian (if needed)

4. After the Researcher completes, read the revised research file and check for a `> **Stale History:**` marker above the `## Historical Analysis` section.
5. If the marker is present:
   - Extract key file and directory paths from the revised **Key Components** and **Architecture** sections.
   - Use the Task tool with `subagent_type: "Historian"` and `run_in_background: false`. Prompt it with the research file path and the updated key paths. The Historian will need to replace the existing `## Historical Analysis` section; instruct it to remove the old section (including the stale-history marker) before appending the new one.
6. If no marker is present, skip this phase.

### Wrap-Up

7. Tell the user the research has been revised and they can review again, run `/revise-research` again, or proceed to `/plan <goal>`. If the Historian was re-run, mention that the historical analysis was also refreshed.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
