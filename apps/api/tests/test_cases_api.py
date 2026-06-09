from collections.abc import Iterator
from typing import Any

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

HIDDEN_STRINGS = [
    "HIDDEN_FRAMEUP_ELEMENT_441",
    "HIDDEN_FRAMEUP_ELEMENT_DESCRIPTION_441",
    "HIDDEN_MARA_ADMITTED_BACKUP_KEY_771",
    "HIDDEN_DANIEL_RECOGNIZED_MARA_882",
    "HIDDEN_ELI_SAW_LEDGER_ON_DESK_393",
    "HIDDEN_BACKUP_KEY_FOUND_119",
    "HIDDEN_BACKUP_KEY_DESCRIPTION_119",
    "HIDDEN_BACKUP_KEY_STATUS_119",
    "HIDDEN_BACKUP_KEY_USED_EVENT_220",
    "HIDDEN_CONTRADICTION_KEY_LOG_515",
    "HIDDEN_CONTRADICTION_CAMERA_GAP_616",
    "INTERNAL_LEDGER_FRAMEUP_NOTE_909",
]


def test_health_still_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"service": "objection-api", "status": "ok"}


def test_cases_returns_demo_case_safely() -> None:
    payload = _json(client.get("/cases"))

    assert payload[0]["id"] == "the-missing-ledger"
    assert payload[0]["title"] == "The Missing Ledger"
    assert payload[0]["charge_count"] == 1
    assert payload[0]["witness_count"] == 3
    assert payload[0]["evidence_count"] == 4
    _assert_hidden_strings_absent(payload)


def test_overview_returns_public_case_data_only() -> None:
    payload = _json(client.get("/cases/the-missing-ledger/overview"))

    assert payload["title"] == "The Missing Ledger"
    assert len(payload["charges"][0]["legal_elements"]) == 3
    assert len(payload["witnesses"]) == 3
    assert len(payload["evidence"]) == 4
    assert len(payload["timeline"]) == 6
    assert "contradictions" not in payload
    assert "internal_notes" not in payload
    _assert_hidden_strings_absent(payload)


def test_witness_detail_returns_public_statements_only() -> None:
    payload = _json(client.get("/cases/the-missing-ledger/witnesses/witness-mara-vale"))

    assert payload["id"] == "witness-mara-vale"
    assert [statement["id"] for statement in payload["statements"]] == [
        "statement-mara-key-cabinet",
        "statement-mara-locked-up",
    ]
    _assert_hidden_strings_absent(payload)


def test_evidence_detail_returns_public_links_only() -> None:
    payload = _json(
        client.get("/cases/the-missing-ledger/evidence/evidence-security-still")
    )

    assert payload["id"] == "evidence-security-still"
    assert payload["admissibility_status"] == "Pending foundation"
    assert payload["witness_statement_links"] == [
        "statement-daniel-hallway",
        "statement-daniel-camera-gap",
    ]
    _assert_hidden_strings_absent(payload)


def test_unknown_resources_return_404() -> None:
    assert client.get("/cases/not-real/overview").status_code == 404
    assert (
        client.get("/cases/the-missing-ledger/witnesses/not-real").status_code == 404
    )
    assert client.get("/cases/the-missing-ledger/evidence/not-real").status_code == 404


def _json(response) -> Any:
    assert response.status_code == 200
    return response.json()


def _assert_hidden_strings_absent(payload: Any) -> None:
    visible_text = "\n".join(_flatten_strings(payload))
    for hidden in HIDDEN_STRINGS:
        assert hidden not in visible_text


def _flatten_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _flatten_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _flatten_strings(child)
