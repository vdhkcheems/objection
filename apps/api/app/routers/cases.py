from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.services.case_repository import (
    CaseNotFoundError,
    CaseRepository,
    get_case_repository,
)

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("")
def list_cases(
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> list[dict]:
    return repository.list_cases()


@router.get("/{case_id}/overview")
def get_case_overview(
    case_id: UUID,
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> dict:
    try:
        return repository.get_public_overview(case_id)
    except CaseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{case_id}/witnesses/{witness_id}")
def get_witness_detail(
    case_id: UUID,
    witness_id: str,
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> dict:
    try:
        return repository.get_public_witness(case_id, witness_id)
    except CaseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{case_id}/witnesses")
def get_public_witness_ids(
    case_id: UUID,
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> list[str]:
    try:
        return repository.get_public_witness_ids(case_id)
    except CaseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{case_id}/evidence")
def get_public_evidence_ids(
    case_id: UUID,
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> list[str]:
    try:
        return repository.get_public_evidence_ids(case_id)
    except CaseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{case_id}/evidence/{evidence_id}")
def get_evidence_detail(
    case_id: UUID,
    evidence_id: str,
    repository: Annotated[CaseRepository, Depends(get_case_repository)],
) -> dict:
    try:
        return repository.get_public_evidence(case_id, evidence_id)
    except CaseNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
