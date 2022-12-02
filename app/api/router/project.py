from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from applications.audio_service import AudioService, AudioTextService, ProjectService
from schemas.audio import AudioSchema, AudioDetailSchema, AudioTextSchema
from schemas.project import ProjectSchema
from containers import AudioContainer

router = APIRouter(
    prefix="/projects",
    tags=["project"],
)

@router.get("/")
@inject
def get_projects(project_service: ProjectService = Depends(Provide[AudioContainer.project_service])):
    return project_service.get_objects()

@router.post("/")
@inject
def create_projects(project: ProjectSchema, 
                    project_service: ProjectService = Depends(Provide[AudioContainer.project_service])
                    ):
    project_dict = project.dict()
    return project_service.create(**project_dict)
