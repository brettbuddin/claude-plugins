# Smith

A structured agent pipeline for Claude Code. Research a codebase, plan changes, and implement them through a human-in-the-loop workflow.

All artifacts are persisted as Markdown in a `notes/` directory within your project.

## Pipeline

```
/smith:research <topic>     ->  notes/research/TOPIC.md
/smith:plan <goal>          ->  notes/plans/GOAL.md
/smith:implement            ->  code changes
```

Each stage produces a document you review before proceeding. Annotate any document inline and re-dispatch the agent to address your feedback:

```
/smith:revise-research
/smith:revise-plan
```

## Optional Commands

| Command | Description |
|---------|-------------|
| `/smith:report [topic]` | Synthesize research and plans into an RFD-style document for stakeholder review |
| `/smith:revise-report` | Revise a report based on inline annotations |
| `/smith:webview [file]` | Render a notes document in the browser |

## Install

```
/plugin install smith
```

## Resources

Articles who's methodologies inspired aspects of this work.

- [Red-Green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/) (Willison, 2026)
- [How I Use Claude Code](https://boristane.com/blog/how-i-use-claude-code/) (Boris Tane, 2026)
- [Engineering Rigor in the LLM Age](https://oxide-and-friends.transistor.fm/episodes/engineering-rigor-in-the-llm-age) (Oxide and Friends, 2026)
- [Here’s how I use LLMs to help me write code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) (Willison, 2025)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Anthropic, 2025)
- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) (Willison)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) (Anthropic)
- [Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (Anthropic)
