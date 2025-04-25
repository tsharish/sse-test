import time
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

headers = {
    "X-Accel-Buffering": "no",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Transfer-Encoding": "chunked",
    "Connection": "keep-alive",
}


def generator():
    i = 1
    while i <= 10:
        yield json.dumps({"session": i, "content": f"Session {i}"}) + "\n"
        i += 1
        time.sleep(1)


def sse_generator():
    i = 1
    while i <= 10:
        data = {"message": f"Session {i}"}
        yield f"data: {json.dumps(data)}\n\n"
        i += 1
        time.sleep(1)


def event_generator():
    i = 1
    while i <= 10:
        data = {"message": f"Session {i}"}
        yield f"{json.dumps(data)}"
        i += 1
        time.sleep(1)


@app.get("/")
async def main():
    return "Welcome to SSE Test"


@app.get("/notsse")
async def notsse():
    return StreamingResponse(generator(), media_type="application/json", headers=headers)


@app.get("/sse")
async def sse():
    return StreamingResponse(sse_generator(), media_type="text/event-stream", headers=headers)


@app.get("/plain")
async def plain():
    return StreamingResponse(generator(), media_type="text/plain", headers=headers)


@app.get("/web")
async def read_index():
    return FileResponse("index.html")


@app.get("/event")
async def event():
    return EventSourceResponse(event_generator())


@app.get("/webevent")
async def read_index():
    return FileResponse("index1.html")
