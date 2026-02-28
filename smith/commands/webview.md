---
description: >-
  Render a docs Markdown document (research, plan, or report) in the
  browser as styled HTML.
---

# Webview

Render a docs Markdown document in the browser.

## Args

`<file path, topic description, or "serve">` (optional). If provided, it can be:

- `serve` to start a local auto-refreshing server for all Markdown files in the working directory
- A direct file path (e.g., `docs/research/auth-flow.md`)
- A topic name (e.g., `auth-flow`)
- A file type keyword: `research`, `plan`, or `report`

If no argument is provided and only one docs Markdown file exists, it is
used automatically. If multiple exist, list the available files and stop.

## Steps

1. If the argument is `serve`, locate the rendering script (the plugin root
   is the directory two levels above this command file; the script path is
   `<plugin-root>/bin/mdview`). Use the Bash tool with
   `run_in_background: true` to run:
   `<plugin-root>/bin/mdview --serve`
   The server picks a random available port automatically. Tell the user to
   check the background task output for the URL, then stop.
2. If the user provided a direct file path that exists, use it. Skip to step 5.
3. Glob for `docs/research/*.md`, `docs/plans/*.md`, and
   `docs/reports/*.md` in the working directory. If none exist, tell
   the user no docs documents were found and stop.
4. Disambiguate the target file:
   - If a topic name was given, filter to files whose base name matches the
     topic. If a file type keyword was also given, filter further by
     subdirectory (`docs/research/`, `docs/plans/`, or
     `docs/reports/`). If exactly one file matches, select it. Otherwise
     list matches and stop.
   - If only a file type keyword was given (`research`, `plan`, or `report`),
     filter to files in the matching subdirectory. If exactly one matches,
     select it. Otherwise list matches and stop.
   - If no argument was given: if exactly one docs Markdown file exists,
     select it. Otherwise list all available files grouped by subdirectory and
     stop.
5. Locate the rendering script: the plugin root is the directory two levels
   above this command file. The script path is
   `<plugin-root>/bin/mdview`. Use the Bash tool to run:
   `<plugin-root>/bin/mdview <resolved-file-path>`
6. Tell the user the file has been opened in their browser.
