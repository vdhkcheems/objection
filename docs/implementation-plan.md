# Objection! Implementation Plan

Objection! is an AI-powered courtroom strategy game where the player acts as either the defense lawyer or prosecutor in fictional criminal trials.

The guiding principle for the MVP is:

```text
Structured courtroom logic first, LLM dialogue generation second.
```

The case file is locked. Facts, evidence, witness statements, timelines, contradictions, and legal elements are predefined. AI agents may generate natural dialogue, but they must not invent facts or evidence.

## Recommended MVP Stack

- Frontend: Next.js, React, TypeScript
- Backend: Python FastAPI
- Data validation: Pydantic
- Database later: PostgreSQL
- ORM later: SQLAlchemy or SQLModel
- AI layer later: OpenAI API through the backend only
- Early case storage: JSON or YAML case files

## Phase 0: Project Setup

Goal: create the foundation.

Build:

- Repo structure
- Next.js web app
- FastAPI backend
- Shared development scripts
- Basic health check endpoint
- Simple homepage/game shell

Test:

- Frontend runs locally
- Backend runs locally
- Frontend can call backend health endpoint

Exit criteria:

```text
Open web app -> see Objection! shell -> backend status is connected
```

## Phase 1: Locked Case File Schema

Goal: define the truth layer.

Build:

- JSON/YAML case file format
- Case IDs must be UUIDs (not human-readable names)
- Pydantic models for validation
- One handcrafted demo case
- Evidence model
- Witness model
- Timeline model
- Contradiction model
- Charges and legal elements model

Test:

- Invalid case files fail validation
- Valid case loads successfully
- Backend can return case overview without leaking hidden facts

Exit criteria:

```text
Backend loads one locked case and exposes only player-safe data
```

## Phase 2: Courtroom State Machine

Goal: make the trial function as a game, even without AI.

Build:

- Trial phases:
  - Opening
  - Direct examination
  - Cross-examination
  - Evidence presentation
  - Closing
  - Verdict
- Turn system
- Active speaker tracking
- Transcript log
- Allowed player actions
- Trial session state

Test:

- Start trial
- Advance phase
- Submit player action
- Transcript updates
- Illegal phase actions are rejected

Exit criteria:

```text
A full trial can move from start to verdict using placeholder text
```

## Phase 3: Witness Answer Engine

Goal: witnesses answer only from locked knowledge.

Build:

- Witness knowledge boundaries
- Question parser/classifier
- Answer selection from case facts
- Uncertainty/refusal behavior
- Contradiction hooks
- Scripted fallback responses

Test:

- Witness answers known facts
- Witness refuses unknown facts
- Witness does not reveal hidden facts
- Repeated questions stay consistent

Exit criteria:

```text
Player can cross-examine a witness and receive controlled, consistent answers
```

## Phase 4: Evidence System

Goal: make evidence usable as gameplay.

Build:

- Evidence inventory
- Admissibility metadata
- Present evidence action
- Evidence-to-statement links
- Contradiction detection
- Evidence inspection UI

Test:

- Player can inspect evidence
- Player can present evidence during valid phases
- Irrelevant evidence has no effect
- Relevant evidence can expose contradiction

Exit criteria:

```text
Player can present evidence that meaningfully changes the trial state
```

## Phase 5: Objection System

Goal: add the core "Objection!" mechanic.

Build:

- Objection types:
  - Relevance
  - Hearsay
  - Speculation
  - Leading
  - Argumentative
  - Asked and answered
  - Lack of foundation
- Objection validation rules
- Judge ruling engine
- Sustained/overruled outcomes
- Penalties/rewards for correct/incorrect objections

Test:

- Valid objection gets sustained
- Invalid objection gets overruled
- Objection affects transcript/trial score
- Objection only works during valid moments

Exit criteria:

```text
Player can object, judge rules, and the ruling affects courtroom momentum
```

## Phase 6: Basic Web Game UI

Goal: make it feel playable.

Build:

- Courtroom screen
- Witness panel
- Judge panel
- Player input box
- Evidence drawer
- Transcript
- Objection controls
- Phase/status bar
- Role selection: defense/prosecution

Test:

- Complete one trial through UI
- No hidden facts exposed
- Clear active phase/action options
- Transcript readable

Exit criteria:

```text
Someone can play the whole MVP case in the browser without touching the API directly
```

## Phase 7: Verdict Engine

Goal: turn performance into outcome.

Build:

- Scoring model
- Credibility changes
- Contradiction impact
- Objection impact
- Evidence impact
- Verdict generation
- Post-trial summary

Test:

- Better play improves outcome
- Contradictions affect witness credibility
- Irrelevant actions do not randomly change verdict
- Verdict explains major reasons

Exit criteria:

```text
Trial ends with a reasoned guilty/not guilty result and performance breakdown
```

## Phase 8: LLM Dialogue Layer

Goal: make the courtroom feel alive without breaking truth.

Build:

- LLM wrapper service
- Prompt templates
- Judge dialogue agent
- Witness dialogue agent
- Response validator
- Fact-grounding layer
- Fallback to rule-based answer if unsafe

Test:

- AI dialogue stays inside locked facts
- Invented facts are rejected
- Witness tone/personality works
- Judge rulings remain rule-driven
- Game works if LLM fails

Exit criteria:

```text
AI makes dialogue natural, but the rules engine still controls truth and outcomes
```

## Phase 9: Save Sessions And Accounts

Goal: persistence.

Build:

- PostgreSQL database
- Trial sessions table
- Transcript storage
- User accounts, optional at first
- Resume trial
- Replay completed trial

Test:

- Refresh does not lose session
- Completed trial can be reviewed
- Case file remains immutable
- User only sees their sessions

Exit criteria:

```text
Players can start, pause, resume, and review trials
```

## Phase 10: Polish And Playtesting

Goal: make it fun and understandable.

Build:

- Better pacing
- Clearer feedback
- Improved witness personalities
- Better evidence UX
- Difficulty tuning
- Tutorial prompts
- Trial result screen
- Bug fixes from playtests

Test:

- New user can understand what to do
- Trial feels fair
- No soft-locks
- No obvious AI hallucinations
- Repeat playthroughs expose different strategies

Exit criteria:

```text
The MVP is playable, coherent, and ready for outside testers
```

## Implementation Order

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10
```

The project should avoid adding LLM-driven behavior before Phase 8. Until then, use deterministic placeholder logic so the courtroom engine can be tested independently from language generation.
