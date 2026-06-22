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

Phase 1 is complete. The project now has a locked, JSON-backed case file schema validated by Pydantic, with one handcrafted demo case: **The Missing Ledger**.

The backend currently provides player-safe case data only:

- UUID-backed case IDs
- Charges and legal elements
- Public witness profiles and statements
- Public evidence and timeline data
- Hidden facts, contradictions, and internal notes retained in the locked case file but excluded from public responses

The web app displays this public case overview as a read-only dashboard. Trial flow, questioning, evidence presentation, objections, scoring, verdicts, and LLM dialogue are intentionally deferred to later phases.

See the full phased roadmap in [docs/implementation-plan.md](docs/implementation-plan.md).

## Local Development

The project uses a Next.js frontend and FastAPI backend.

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

## Current API

The demo case currently uses the UUID `d6f8a523-4163-4c94-a83b-b9c7f11e9a02`.

- `GET /health`
- `GET /cases`
- `GET /cases/{case_id}/overview`
- `GET /cases/{case_id}/witnesses`
- `GET /cases/{case_id}/witnesses/{witness_id}`
- `GET /cases/{case_id}/evidence`
- `GET /cases/{case_id}/evidence/{evidence_id}`

All case endpoints expose public data only. Requests for hidden witness or evidence details return `404`.

## Verification

```bash
npm run test:api
npm run lint:web
npm run build:web
```

`npm run test:api` validates case-file schema rules, reference integrity, UUID case IDs, API error handling, and redaction of hidden facts.
