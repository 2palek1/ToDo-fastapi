from fastapi import FastAPI
from src.tasks.router import router as router_tasks


app = FastAPI(
    title="To-Do list"
)

app.include_router(router_tasks)
