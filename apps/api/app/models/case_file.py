from enum import Enum

from pydantic import BaseModel, Field, model_validator


class Visibility(str, Enum):
    PUBLIC = "public"
    HIDDEN = "hidden"


class LegalElement(BaseModel):
    id: str
    name: str
    description: str
    visibility: Visibility = Visibility.PUBLIC


class Charge(BaseModel):
    id: str
    name: str
    description: str
    legal_elements: list[LegalElement] = Field(min_length=1)


class WitnessStatement(BaseModel):
    id: str
    summary: str
    visibility: Visibility = Visibility.PUBLIC
    evidence_links: list[str] = Field(default_factory=list)
    timeline_event_links: list[str] = Field(default_factory=list)


class Witness(BaseModel):
    id: str
    name: str
    role: str
    bio: str
    visibility: Visibility = Visibility.PUBLIC
    statements: list[WitnessStatement] = Field(default_factory=list)


class Evidence(BaseModel):
    id: str
    title: str
    type: str
    description: str
    visibility: Visibility = Visibility.PUBLIC
    admissibility_status: str
    admissibility_visibility: Visibility = Visibility.PUBLIC
    witness_links: list[str] = Field(default_factory=list)
    timeline_event_links: list[str] = Field(default_factory=list)
    witness_statement_links: list[str] = Field(default_factory=list)


class TimelineEvent(BaseModel):
    id: str
    sequence: int
    timestamp: str
    description: str
    visibility: Visibility = Visibility.PUBLIC
    evidence_links: list[str] = Field(default_factory=list)
    witness_links: list[str] = Field(default_factory=list)


class Contradiction(BaseModel):
    id: str
    summary: str
    visibility: Visibility = Visibility.HIDDEN
    witness_statement_links: list[str] = Field(default_factory=list)
    evidence_links: list[str] = Field(default_factory=list)
    timeline_event_links: list[str] = Field(default_factory=list)
    legal_element_links: list[str] = Field(default_factory=list)


class CaseFile(BaseModel):
    id: str
    title: str
    summary: str
    jurisdiction: str
    status: str
    player_roles: list[str] = Field(min_length=1)
    charges: list[Charge] = Field(min_length=1)
    witnesses: list[Witness] = Field(min_length=1)
    evidence: list[Evidence] = Field(min_length=1)
    timeline: list[TimelineEvent] = Field(min_length=1)
    contradictions: list[Contradiction] = Field(default_factory=list)
    internal_notes: str | None = None

    @model_validator(mode="after")
    def validate_case_references(self) -> "CaseFile":
        charge_ids = _unique_ids("charge", [charge.id for charge in self.charges])
        witness_ids = _unique_ids("witness", [witness.id for witness in self.witnesses])
        evidence_ids = _unique_ids("evidence", [item.id for item in self.evidence])
        timeline_ids = _unique_ids("timeline event", [event.id for event in self.timeline])
        _unique_ids("contradiction", [item.id for item in self.contradictions])

        legal_element_ids: set[str] = set()
        statement_ids: set[str] = set()

        for charge in self.charges:
            for element in charge.legal_elements:
                _add_unique("legal element", element.id, legal_element_ids)

        for witness in self.witnesses:
            for statement in witness.statements:
                _add_unique("witness statement", statement.id, statement_ids)
                _validate_known_ids(
                    "witness statement",
                    statement.id,
                    statement.evidence_links,
                    "evidence",
                    evidence_ids,
                )
                _validate_known_ids(
                    "witness statement",
                    statement.id,
                    statement.timeline_event_links,
                    "timeline event",
                    timeline_ids,
                )

        for item in self.evidence:
            _validate_known_ids(
                "evidence", item.id, item.witness_links, "witness", witness_ids
            )
            _validate_known_ids(
                "evidence",
                item.id,
                item.timeline_event_links,
                "timeline event",
                timeline_ids,
            )
            _validate_known_ids(
                "evidence",
                item.id,
                item.witness_statement_links,
                "witness statement",
                statement_ids,
            )

        for event in self.timeline:
            _validate_known_ids(
                "timeline event", event.id, event.evidence_links, "evidence", evidence_ids
            )
            _validate_known_ids(
                "timeline event", event.id, event.witness_links, "witness", witness_ids
            )

        for contradiction in self.contradictions:
            _validate_known_ids(
                "contradiction",
                contradiction.id,
                contradiction.witness_statement_links,
                "witness statement",
                statement_ids,
            )
            _validate_known_ids(
                "contradiction",
                contradiction.id,
                contradiction.evidence_links,
                "evidence",
                evidence_ids,
            )
            _validate_known_ids(
                "contradiction",
                contradiction.id,
                contradiction.timeline_event_links,
                "timeline event",
                timeline_ids,
            )
            _validate_known_ids(
                "contradiction",
                contradiction.id,
                contradiction.legal_element_links,
                "legal element",
                legal_element_ids,
            )

        return self


def _unique_ids(label: str, ids: list[str]) -> set[str]:
    seen: set[str] = set()
    for item_id in ids:
        _add_unique(label, item_id, seen)
    return seen


def _add_unique(label: str, item_id: str, seen: set[str]) -> None:
    if item_id in seen:
        raise ValueError(f"Duplicate {label} id: {item_id}")
    seen.add(item_id)


def _validate_known_ids(
    owner_label: str,
    owner_id: str,
    refs: list[str],
    target_label: str,
    valid_ids: set[str],
) -> None:
    for ref in refs:
        if ref not in valid_ids:
            raise ValueError(
                f"{owner_label} '{owner_id}' references unknown {target_label} id: {ref}"
            )
