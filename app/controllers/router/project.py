from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from app.applications.services.audio import AudioService
from app.applications.services.project import ProjectService
from app.applications.services.text import TextService
from app.controllers.schemas.audio import AudioSchema, AudioDetailSchema
from app.controllers.schemas.text import TextSchema
from app.controllers.schemas.project import ProjectSchema
from app.infrastructures.containers import AudioContainer

router = APIRouter(
    prefix="/projects",
    tags=["project"],
)


@router.get("/")
@inject
def get_projects(project_service: ProjectService = Depends(Provide[AudioContainer.project_service])):
    return project_service.get_objects()


@router.get("/{project_id}")
@inject
def get_project_detail(project_id: int, project_service: ProjectService = Depends(Provide[AudioContainer.project_service])):
    return project_service.get_object_by_id(project_id)


@router.post("/")
@inject
def create_projects(
    project: ProjectSchema,
    project_service: ProjectService = Depends(
        Provide[AudioContainer.project_service])
):
    project_dict = project.dict()
    return project_service.create(**project_dict)


@router.patch("/{project_id}")
@inject
def update_project(
    project: ProjectSchema,
    project_id: int,
    project_service: ProjectService = Depends(
        Provide[AudioContainer.project_service])
):
    project_service.update(project_id)
    return


@router.delete("/{project_id}")
@inject
def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(
        Provide[AudioContainer.project_service])
):
    project_service.delete(project_id)
    return
