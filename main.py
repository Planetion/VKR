import uvicorn
from fastapi import FastAPI
from datetime import datetime
from db import create_tables
from public.routers import users_router, level_router

app = FastAPI()
create_tables()

app.include_router(users_router)
app.include_router(level_router)

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
