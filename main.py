import time
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response

app = FastAPI()

headers = {
    "Cache-Control": "no-cache",
    "X-Content-Type-Options": "nosniff",
    "Transfer-Encoding": "chunked",
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
    return StreamingResponse(
        generator(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Content-Type-Options": "nosniff",
            "X-Accel-Buffering": "no",
        },
    )
