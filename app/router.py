from fastapi import APIRouter
from api.router import audio, project, user

router = APIRouter(prefix='/api/v1')

router.include_router(audio.router)
router.include_router(project.router)
router.include_router(user.router)