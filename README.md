# Objection!

Objection! is an AI-powered courtroom strategy game currently in development.

Players take the role of either a defense lawyer or prosecutor in fictional criminal trials. The core gameplay is built around cross-examining witnesses, challenging evidence, raising objections, exposing contradictions, and persuading the court through logical argumentation.

## Vision

The long-term goal is to build a highly replayable legal strategy simulator powered by multi-agent AI. The courtroom should feel alive, but the game must remain fair, consistent, and grounded in a locked case file.

Objection! is designed around one core principle:

```text
Structured courtroom logic first, LLM dialogue generation second.
```

That means the AI can generate natural courtroom dialogue, but all facts, evidence, witness statements, timelines, and contradictions must come from a controlled case-state engine. Agents should not invent new evidence or rewrite the facts of the case during play.

## Planned MVP

The first playable version will focus on one handcrafted criminal case and include:

- Player as defense or prosecution
- AI judge and witnesses
- Locked case file and evidence system
- Cross-examination flow
- Objection handling
- Contradiction detection
- Verdict generation
- Web-based game interface

## Development Status

This project is in early development. The current focus is building the foundation:

1. Case and evidence models
2. Courtroom state-machine logic
3. Witness and judge reasoning systems
4. Web game interface
5. LLM-based dialogue agents after the core rules are working

See the full phased roadmap in [docs/implementation-plan.md](docs/implementation-plan.md).

## Local Development

Phase 0 uses a Next.js frontend and FastAPI backend.

```bash
npm install
cd apps/api
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd ../..
npm run dev
```

The web app runs at [http://localhost:3000](http://localhost:3000).
The API health endpoint runs at [http://localhost:8000/health](http://localhost:8000/health).