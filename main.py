import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from db import create_tables
from public.routers import users_router
from public.level_routers import level_router

app = FastAPI()
create_tables()

app.include_router(users_router)
app.include_router(level_router)

# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "https://vkr-frg0.onrender.com",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.on_event("startup")
def on_startup():
    open("log.txt", mode ="a").write(f'{datetime.utcnow()}: Begin\n')

@app.on_event("shutdown")
def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get("/")
def main():
    return ("<b>Hello world!</b>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
