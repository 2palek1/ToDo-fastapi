from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


from src.tasks.router import router as router_tasks


app = FastAPI(
    title="To-Do list"
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(router_tasks)
