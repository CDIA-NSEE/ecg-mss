from fastapi import FastAPI
from modules.routers.auth_router import auth_router
from modules.routers.exam_router import exam_router

app = FastAPI(title="ECG Mss", version="1.0.0", description="ECG Mss API", root_path="/api")

app.include_router(auth_router)
app.include_router(exam_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9876, log_level="info")
