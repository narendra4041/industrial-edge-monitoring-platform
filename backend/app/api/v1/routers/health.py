from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/live")
def liveness_check() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready")
def readiness_check() -> dict[str, str]:
    return {"status": "ready"}
