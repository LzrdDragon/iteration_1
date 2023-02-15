from fastapi import FastAPI
from iteration_1.fastapi_endpoints import router as iteration_1_router
import uvicorn


def init_routers(app: FastAPI) -> FastAPI:
    app.include_router(iteration_1_router, tags=["iteration_1"])
    return app


def get_app() -> FastAPI:
    app: FastAPI = FastAPI()
    init_routers(app)
    return app


app = get_app()


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("asgi:app", host="0.0.0.0", port=8000, reload=True, workers=1, log_level='debug', access_log=True)
