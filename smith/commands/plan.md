---
description: >-
  Dispatch the Planner agent to produce a detailed implementation plan from
  research findings. Produces an <output_directory>/plans/GOAL.md file.
---

# Plan

Dispatch the Planner agent to produce an implementation plan.

## Args

`<specific goal description>` (required). If no description is provided, reply with a short usage summary and stop.

## Steps

0. Use the `smith:config` skill to read project configuration. Use the `output_directory` value (default: `docs/`) wherever `<output_directory>` appears below. Note the `plan_auto_critique` value (default: `false`) for step 4.
1. Glob for `<output_directory>/research/*.md` in the working directory.
2. Use the Task tool with `subagent_type: "Planner"` and `run_in_background: false`.
3. Prompt the agent with:
   - The specific goal description provided by the user
   - Which research file(s) exist (let the planner pick the right one per its own instructions)
4. If `plan_auto_critique` is `true`:
   a. Use the Task tool with `subagent_type: "Critic"` and `run_in_background: false`. Prompt the agent with the working directory path so it can find and annotate the plan file that was just created.
   b. After the Critic completes, use the Task tool with `subagent_type: "Planner"` and `run_in_background: false`. Prompt the agent with the working directory path and instruct it to read the plan file and address any inline annotations from the Critic.
5. After completion:
   - If auto-critique ran: tell the user the plan has been critiqued and revised, provide the file path, and suggest they review it. Mention they can run `/critique-plan` and `/revise-plan` for additional rounds, or proceed to `/implement`.
   - If auto-critique did not run: tell the user the plan file path (which will be `<output_directory>/plans/GOAL.md`) and suggest they review/annotate it, then run `/critique-plan`, `/revise-plan`, or `/implement`.

## Prompting the Agent

When constructing the prompt for the Task tool, include:

- The user's description
- The working directory path so the agent knows where to find/write files
- Any additional context the user provided in the conversation

Do NOT paste the agent's own instructions into the prompt; the agent definitions are already loaded by the Task tool via `subagent_type`.
