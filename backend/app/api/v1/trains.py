"""Train and coach endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.schemas import CoachCreate, CoachResponse, TrainCreate, TrainResponse
from app.db.session import get_db
from app.repositories.train import get_train, list_coaches
from app.services.train import TrainNumberAlreadyExistsError, add_coach, create_train

router = APIRouter(prefix="/trains", tags=["trains"])


@router.post("", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
def create_train_endpoint(
    payload: TrainCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> TrainResponse:
    try:
        return create_train(db, payload)
    except TrainNumberAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc


@router.get("/{train_id}/coaches", response_model=list[CoachResponse])
def get_coaches(train_id: str, db: Session = Depends(get_db)) -> list[CoachResponse]:  # noqa: B008
    if get_train(db, train_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Train not found"
        )
    return list_coaches(db, train_id)


@router.post(
    "/{train_id}/coaches",
    response_model=CoachResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_coach_endpoint(
    train_id: str,
    payload: CoachCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> CoachResponse:
    train = get_train(db, train_id)
    if train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Train not found"
        )
    return add_coach(db, train, payload)
