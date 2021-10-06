from fastapi import APIRouter
from api.api_v1_0.endpoints.auth import router as auth_router
from api.api_v1_0.endpoints.shortener import router as shortener_router
from api.api_v1_0.endpoints.report import router as report_router
from starlette.status import HTTP_404_NOT_FOUND

router = APIRouter()
router.include_router(auth_router, prefix="/auth",
                      responses={HTTP_404_NOT_FOUND: {"description": "Not found"}}, tags=["auth"],
                      include_in_schema=False)

router.include_router(shortener_router, prefix="/shortener",
                      responses={HTTP_404_NOT_FOUND: {"description": "Not found"}}, tags=["shortener"])

router.include_router(report_router, prefix="/report",
                      responses={HTTP_404_NOT_FOUND: {"description": "Not found"}}, tags=["general"])
