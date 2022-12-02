from fastapi import APIRouter, Depends, Response, status


router = APIRouter(
    prefix="/projects",
    tags=["project"],
)