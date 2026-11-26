from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from uuid import UUID

from app.models.Workspace import Workspace
from app.models.WorkspaceMember import WorkspaceMember
from .schemas import WorkspaceCreate


def get_user_workspace_role(db: Session, user_id: UUID, workspace_id: UUID):
    role = (
        db.query(WorkspaceMember.role)
        .where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        .scalar()
    )
    if role is None:
        raise HTTPException(status_code=404, detail="Workspace Not Found")
    return role


def get_user_workspaces(db: Session, user_id: UUID):
    return (
        db.query(
            Workspace.id,
            Workspace.name,
            Workspace.currency,
            WorkspaceMember.role,
        )
        .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
        .where(WorkspaceMember.user_id == user_id)
        .order_by(Workspace.name)
        .all()
    )


def create_user_workspace(db: Session, user_id: UUID, data: WorkspaceCreate):
    new_workspace = Workspace(
        name=data.name, currency=data.currency, created_by=user_id
    )
    db.add(new_workspace)
    try:
        db.flush()
        new_workspace_member = WorkspaceMember(
            workspace_id=new_workspace.id, user_id=user_id, role="owner"
        )
        db.add(new_workspace_member)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create Workspace.")

    return get_user_workspaces(db, user_id)


def delete_user_workspace(db: Session, user_id: UUID, workspace_id: UUID):
    role = get_user_workspace_role(db, user_id, workspace_id)
    if role != "owner":
        raise HTTPException(
            status_code=403, detail="You Must Be Owner Of Workspace To Delete Workspace"
        )

    workspace_count = (
        db.query(WorkspaceMember)
        .where(WorkspaceMember.user_id == user_id, WorkspaceMember.role == "owner")
        .count()
    )
    if workspace_count <= 1:
        raise HTTPException(
            status_code=409, detail="You Can't Delete Your Last Workspace"
        )
    stmt = delete(Workspace).where(Workspace.id == workspace_id)

    try:
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could Not Delete Workspace",
        )
    return get_user_workspaces(db, user_id)
