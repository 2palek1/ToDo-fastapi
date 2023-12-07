from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from src.database import get_async_session
from src.tasks.models import task


router = APIRouter(
    prefix="/task",
    tags=["task"]
)


templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def home(request: Request, session: AsyncSession = Depends(get_async_session)):
    stmt = select(task).order_by(task.c.id)
    result = await session.execute(stmt)
    todos_data = result.all()
    return templates.TemplateResponse("/index.html", {
        "request": request,
        "app_name": "ToDo List",
        "todo_list": todos_data
    })


@router.post("/create")
async def create_task(new_task: str = Form(...), session: AsyncSession = Depends(get_async_session)):
    stmt = insert(task).values({"task_name": new_task})
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount > 0:
        return RedirectResponse(url="http://127.0.0.1:8000/task/", status_code=HTTP_303_SEE_OTHER)
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


@router.get("/delete/{task_id}")
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
        return RedirectResponse(url="http://127.0.0.1:8000/task/", status_code=HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=500, detail="Task was not deleted")


@router.get("/update/{task_id}")
async def update_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(task)
        .where(task.c.id == task_id)
        .values(status=~task.c.status)
    )
    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount > 0:
        return RedirectResponse(url="http://127.0.0.1:8000/task/", status_code=HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=500, detail="Task update failed")
