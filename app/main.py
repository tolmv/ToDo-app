from fastapi import FastAPI
from app.api import auth, todos
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="ToDo API",
    description="A simple ToDo API built with FastAPI",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operations with user authentication"
        },
        {
            "name": "todos",
            "description": "CRUD operations with todos"
        }
    ]
)
# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(todos.router, tags=["todos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)