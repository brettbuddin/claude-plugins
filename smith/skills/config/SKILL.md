---
name: config
description: >-
  This skill should be used when the user asks to configure Smith, set project
  preferences, customize agent behavior, or when any Smith command or agent
  needs to read project-local settings. It should also be used when the user
  asks "how do I configure Smith" or wants to change output paths.
---

# Config

Smith supports per-project configuration via a `.smith.local.yaml` file in the project root. This file is user-managed, not committed to git, and provides project-specific settings that Smith agents and commands read at runtime.

## File Location

```
project-root/
└── .smith.local.yaml
```

The file lives in the project root (the working directory), not inside `.claude/` or `docs/`.

## Gitignore

This file should be added to `.gitignore`:

```gitignore
.smith.local.yaml
```

Remind the user to add this entry when creating the file for the first time.

## Format

YAML

```yaml
# Smith project configuration

# Directory where Smith writes research, plans, and reports.
# Default: docs/
output_directory: docs/

# Automatically critique and revise plans after initial generation.
# Default: false
plan_auto_critique: false
```

All fields are optional. An empty file or a file with only some fields is valid.

## Schema

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `output_directory` | string | `docs/` | Base directory where Smith writes documents. Research files go to `<output_directory>/research/`, plans to `<output_directory>/plans/`, and reports to `<output_directory>/reports/`. |
| `plan_auto_critique` | boolean | `false` | When `true`, the `/plan` command automatically runs one round of critique (Critic agent) and revision (Planner agent) after producing the initial plan. |

The schema is intentionally open. Users may add additional keys as needed; agents should read what they recognize and ignore the rest.

## Reading Configuration

### From Commands

When a Smith command dispatches an agent, it should check for `.smith.local.yaml` in the working directory. If the file exists, read it and include relevant settings in the agent prompt.

**Procedure:**

1. Check if `.smith.local.yaml` exists in the working directory using Glob or Read.
2. If it exists, read the file contents.
3. Extract the fields relevant to the agent being dispatched.
4. Include them in the agent prompt as a "Project Configuration" section.

**Example prompt construction:**

```
The working directory is /path/to/project.

## Project Configuration (from .smith.local.yaml)

- **Output directory:** `design-docs/`

<rest of agent prompt>
```

### From Agents

Agents that write documents (Researcher, Planner, Reporter) should use the configured `output_directory` instead of the default `docs/` when the dispatching command provides it. For example, if `output_directory` is `design-docs/`, the Researcher writes to `design-docs/research/TOPIC.md` instead of `docs/research/TOPIC.md`.

### Fallback Behavior

If `.smith.local.yaml` does not exist, or a field is absent, agents use the defaults listed in the schema. Configuration is always optional; its absence must never block execution.

## Creating the Configuration File

When a user asks to configure Smith or set up project settings:

1. Ask what settings they want to configure (or suggest defaults based on the project).
2. Write `.smith.local.yaml` to the project root.
3. Check if `.smith.local.yaml` is already in `.gitignore`. If not, remind the user to add it.
4. Confirm the file was created and summarize the settings.

## When This Skill Applies

- User asks to configure Smith, set preferences, or customize agent behavior.
- User asks "how do I configure Smith" or similar setup questions.
- A Smith command or agent needs to read project settings before dispatching work.
- User wants to change the output directory or other settings.
