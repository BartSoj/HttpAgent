from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from context_service.context_manager import ContextManager
from memory_service.memory_manager import MemoryManager
from schedule_service.schedule_manager import ScheduleManager

app = FastAPI()

context_manager = ContextManager()
memory_manager = MemoryManager()
schedule_manager = ScheduleManager(callback_url="http://localhost:8000/")


@app.get('/context')
async def get_context():
    context = context_manager.get_context()
    return JSONResponse(content=context)


@app.post('/memory')
async def save_memory(memory: str):
    memory_manager.save_memory(memory)
    return JSONResponse(content={"status": "ok"})


@app.get('/memory')
async def get_memory():
    memory = memory_manager.get_memory()
    return JSONResponse(content=memory)


@app.post('/schedule')
async def add_schedule(datetime: str, content: str):
    schedule_manager.add_schedule(datetime, content)
    return JSONResponse(content={"status": "ok"})


def main():
    try:
        uvicorn.run(app, host="0.0.0.0", port=8001)
    finally:
        context_manager.close()
        memory_manager.close()
        schedule_manager.close()


if __name__ == '__main__':
    main()
