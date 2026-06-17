import json
from functools import lru_cache
from pathlib import Path
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from app.models import CaseFile, Visibility


class CaseNotFoundError(LookupError):
    pass


class CaseRepository:
    def __init__(self, case_dir: Path | None = None) -> None:
        self.case_dir = case_dir or Path(__file__).resolve().parents[1] / "data" / "cases"

    def list_cases(self) -> list[dict[str, Any]]:
        return [self._case_summary(case_file) for case_file in self._load_cases()]

    def get_public_overview(self, case_id: UUID) -> dict[str, Any]:
        case_file = self.get_case(case_id)
        return {
            "id": str(case_file.id),
            "title": case_file.title,
            "summary": case_file.summary,
            "jurisdiction": case_file.jurisdiction,
            "status": case_file.status,
            "player_roles": case_file.player_roles,
            "charges": [
                {
                    "id": charge.id,
                    "name": charge.name,
                    "description": charge.description,
                    "legal_elements": [
                        {
                            "id": element.id,
                            "name": element.name,
                            "description": element.description,
                        }
                        for element in charge.legal_elements
                        if element.visibility == Visibility.PUBLIC
                    ],
                }
                for charge in case_file.charges
            ],
            "witnesses": [
                {
                    "id": witness.id,
                    "name": witness.name,
                    "role": witness.role,
                    "bio": witness.bio,
                    "statement_count": len(_public_items(witness.statements)),
                }
                for witness in case_file.witnesses
                if witness.visibility == Visibility.PUBLIC
            ],
            "evidence": [
                {
                    "id": item.id,
                    "title": item.title,
                    "type": item.type,
                    "description": item.description,
                    "admissibility_status": (
                        item.admissibility_status
                        if item.admissibility_visibility == Visibility.PUBLIC
                        else None
                    ),
                }
                for item in case_file.evidence
                if item.visibility == Visibility.PUBLIC
            ],
            "timeline": [
                {
                    "id": event.id,
                    "sequence": event.sequence,
                    "timestamp": event.timestamp,
                    "description": event.description,
                }
                for event in sorted(case_file.timeline, key=lambda entry: entry.sequence)
                if event.visibility == Visibility.PUBLIC
            ],
        }

    def get_public_witness(self, case_id: UUID, witness_id: str) -> dict[str, Any]:
        case_file = self.get_case(case_id)
        witness = next(
            (
                item
                for item in case_file.witnesses
                if item.id == witness_id and item.visibility == Visibility.PUBLIC
            ),
            None,
        )
        if witness is None:
            raise CaseNotFoundError(f"Witness not found: {witness_id}")

        public_evidence_ids = _public_ids(case_file.evidence)
        public_timeline_ids = _public_ids(case_file.timeline)
        return {
            "id": witness.id,
            "name": witness.name,
            "role": witness.role,
            "bio": witness.bio,
            "statements": [
                {
                    "id": statement.id,
                    "summary": statement.summary,
                    "evidence_links": [
                        link
                        for link in statement.evidence_links
                        if link in public_evidence_ids
                    ],
                    "timeline_event_links": [
                        link
                        for link in statement.timeline_event_links
                        if link in public_timeline_ids
                    ],
                }
                for statement in witness.statements
                if statement.visibility == Visibility.PUBLIC
            ],
        }

    def get_public_evidence(self, case_id: UUID, evidence_id: str) -> dict[str, Any]:
        case_file = self.get_case(case_id)
        evidence = next(
            (
                item
                for item in case_file.evidence
                if item.id == evidence_id and item.visibility == Visibility.PUBLIC
            ),
            None,
        )
        if evidence is None:
            raise CaseNotFoundError(f"Evidence not found: {evidence_id}")

        public_witness_ids = _public_ids(case_file.witnesses)
        public_timeline_ids = _public_ids(case_file.timeline)
        public_statement_ids = {
            statement.id
            for witness in case_file.witnesses
            if witness.visibility == Visibility.PUBLIC
            for statement in witness.statements
            if statement.visibility == Visibility.PUBLIC
        }

        return {
            "id": evidence.id,
            "title": evidence.title,
            "type": evidence.type,
            "description": evidence.description,
            "admissibility_status": (
                evidence.admissibility_status
                if evidence.admissibility_visibility == Visibility.PUBLIC
                else None
            ),
            "witness_links": [
                link for link in evidence.witness_links if link in public_witness_ids
            ],
            "timeline_event_links": [
                link
                for link in evidence.timeline_event_links
                if link in public_timeline_ids
            ],
            "witness_statement_links": [
                link
                for link in evidence.witness_statement_links
                if link in public_statement_ids
            ],
        }

    def get_case(self, case_id: UUID) -> CaseFile:
        for case_file in self._load_cases():
            if case_file.id == case_id:
                return case_file
        raise CaseNotFoundError(f"Case not found: {case_id}")

    def load_case_file(self, path: Path) -> CaseFile:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return CaseFile.model_validate(payload)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in case file {path.name}: {exc}") from exc
        except ValidationError:
            raise

    def _load_cases(self) -> list[CaseFile]:
        if not self.case_dir.exists():
            raise FileNotFoundError(f"Case directory does not exist: {self.case_dir}")

        cases = [
            self.load_case_file(path)
            for path in sorted(self.case_dir.glob("*.json"))
            if path.is_file()
        ]
        case_ids: set[UUID] = set()
        for case_file in cases:
            if case_file.id in case_ids:
                raise ValueError(f"Duplicate case id: {case_file.id}")
            case_ids.add(case_file.id)
        return cases

    def _case_summary(self, case_file: CaseFile) -> dict[str, Any]:
        return {
            "id": str(case_file.id),
            "title": case_file.title,
            "summary": case_file.summary,
            "status": case_file.status,
            "charge_count": len(case_file.charges),
            "witness_count": len(
                [
                    witness
                    for witness in case_file.witnesses
                    if witness.visibility == Visibility.PUBLIC
                ]
            ),
            "evidence_count": len(_public_items(case_file.evidence)),
        }


def _public_items(items: list[Any]) -> list[Any]:
    return [item for item in items if item.visibility == Visibility.PUBLIC]


def _public_ids(items: list[Any]) -> set[str]:
    return {item.id for item in items if item.visibility == Visibility.PUBLIC}


@lru_cache
def get_case_repository() -> CaseRepository:
    return CaseRepository()
