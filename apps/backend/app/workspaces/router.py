from fastapi import APIRouter
from app.core.deps import dbSession, userDep
from .services import get_user_workspaces, create_user_workspace, delete_user_workspace
from .schemas import WorkspaceOut, WorkspaceCreate
from uuid import UUID

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/",response_model=list[WorkspaceOut])
def create_workspace(db : dbSession, user : userDep, data : WorkspaceCreate):
    return create_user_workspace(db,user, data)


@router.get("/", response_model=list[WorkspaceOut])
def get_workspaces(db : dbSession, user : userDep):
    return get_user_workspaces(db,user)


@router.delete("/{workspace_id}",response_model=list[WorkspaceOut])
def delete_workspace(db : dbSession, user : userDep, workspace_id : UUID):
    return delete_user_workspace(db,user,workspace_id)