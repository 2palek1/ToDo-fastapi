from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.tasks.models import task
from src.tasks.schemas import Task
from src.tasks.utils import get_task_dict

router = APIRouter(
    prefix="/task",
    tags=["task"]
)


@router.post("/create")
async def create_task(task_data: Task, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(task).values(**task_data.dict())
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount > 0:
        return ({
            "status": "success",
            "data": task_data,
            "details": None
        })
    raise HTTPException(status_code=500, detail="Error creation task")


@router.get("/{task_id}")
async def get_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(task).where(task.c.id == task_id)
    result = await session.execute(stmt)
    task_data = result.fetchone()
    if task_data:
        return ({
            "status": "success",
            "data": {
                "id": task_data[0],
                "task_name": task_data[1],
                "status": task_data[2],
                "created_at": task_data[3]
            },
            "details": None
        })
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    # Use the select query to check if the task exists before attempting to delete it
    select_stmt = select(task).where(task.c.id == task_id)
    existing_task = await session.execute(select_stmt)

    # Check if the task exists
    existing_task = existing_task.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_stmt = delete(task).where(task.c.id == task_id)
    result = await session.execute(delete_stmt)
    await session.commit()
    if result.rowcount > 0:
        return ({
            "status": "success",
            "data": "{} task deleted successfully".format(task_id),
            "details": None
        })
    raise HTTPException(status_code=500, detail="Task was not deleted")
