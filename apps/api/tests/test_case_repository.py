from copy import deepcopy
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models import CaseFile
from app.services.case_repository import CaseRepository


CASE_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "data"
    / "cases"
    / "the-missing-ledger.json"
)


@pytest.fixture
def valid_payload() -> dict:
    return CaseRepository().load_case_file(CASE_PATH).model_dump(mode="json")


def test_valid_demo_case_loads_successfully() -> None:
    case_file = CaseRepository().load_case_file(CASE_PATH)

    assert case_file.id == UUID("d6f8a523-4163-4c94-a83b-b9c7f11e9a02")
    assert len(case_file.charges) == 1
    assert len(case_file.witnesses) >= 3
    assert len(case_file.evidence) >= 4
    assert len(case_file.timeline) >= 6
    assert len(case_file.contradictions) >= 2


def test_missing_required_field_fails_validation(valid_payload: dict) -> None:
    payload = deepcopy(valid_payload)
    del payload["title"]

    with pytest.raises(ValidationError):
        CaseFile.model_validate(payload)


def test_invalid_visibility_fails_validation(valid_payload: dict) -> None:
    payload = deepcopy(valid_payload)
    payload["witnesses"][0]["statements"][0]["visibility"] = "sealed"

    with pytest.raises(ValidationError):
        CaseFile.model_validate(payload)


def test_invalid_case_id_fails_validation(valid_payload: dict) -> None:
    payload = deepcopy(valid_payload)
    payload["id"] = "the-missing-ledger"

    with pytest.raises(ValidationError):
        CaseFile.model_validate(payload)


def test_broken_reference_fails_validation(valid_payload: dict) -> None:
    payload = deepcopy(valid_payload)
    payload["contradictions"][0]["evidence_links"].append("evidence-missing")

    with pytest.raises(ValidationError):
        CaseFile.model_validate(payload)


def test_duplicate_ids_fail_validation(valid_payload: dict) -> None:
    payload = deepcopy(valid_payload)
    payload["evidence"][1]["id"] = payload["evidence"][0]["id"]

    with pytest.raises(ValidationError):
        CaseFile.model_validate(payload)
