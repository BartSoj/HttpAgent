import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field

from api_servers.context_service.context_manager import ContextManager
from api_servers.memory_service.memory_manager import MemoryManager
from api_servers.schedule_service.schedule_manager import ScheduleManager
from api_servers.console_chat_service.console_chat import ConsoleChat

app = FastAPI(title="essentials",
              summary="Essential Agent API",
              description="This API is used for essential agent operation such as getting time, date, city, saving memory, adding schedule, interacting with the user",
              version="0.1.0",
              servers=[{"url": "http://127.0.0.1:8001"}]
              )
agent_url = "http://localhost:8000/"

context_manager = ContextManager()
memory_manager = MemoryManager()
schedule_manager = ScheduleManager(agent_url=agent_url)
console_chat = ConsoleChat(user_name="User", agent_name="Agent", agent_url=agent_url)


@app.get('/time')
async def get_time():
    """
    Get the current time.

    Returns the current time.
    """
    return JSONResponse(content={"time": context_manager.get_time()})


@app.get('/date')
async def get_date():
    """
    Get the current date.

    Returns the current date.
    """
    return JSONResponse(content={"date": context_manager.get_date()})


@app.get('/city')
async def get_city():
    """
    Get the current city.

    Returns the current city.
    """
    return JSONResponse(content={"city": context_manager.get_city()})


class MemoryModel(BaseModel):
    memory: str = Field(...,
                        description="String with the content that represents a memory and will be saved for later use in the conversation.")


@app.post('/memory')
async def save_memory(reqeust: MemoryModel):
    """
    Save a new memory.

    Stores the provided memory for later use in the conversation.
    """
    memory_manager.save_memory(reqeust.memory)
    return JSONResponse(content={"status": "ok"})


@app.get('/memory')
async def get_memory():
    """
    Get all the saved memory.

    Returns the list of saved memories.
    """
    memory = memory_manager.get_memory()
    return JSONResponse(content=memory)


class ScheduleModel(BaseModel):
    time: str = Field(...,
                      description="The date and time when the assistant should be invoked. The date and time should be in ISO 8601 format.",
                      examples=["2024-08-20T16:33:14Z", "2024-09-01T12:43:00Z"])
    content: str = Field(...,
                         description="The content that should be sent to the assistant when it is invoked. It can inform the assistant about the action to be performed, the reminder message, the notification message, etc.",
                         examples=["Reminder to take medicine", "Reminder me to call mom", "Wake up alarm"])


@app.post('/schedule')
async def add_schedule(request: ScheduleModel):
    """
    Add a new schedule for later execution.

    Add a schedule to invoke the assistant at a specific time with specific content. Can be used to schedule a reminder, notification, set a timer, alarm or any other time-based action.
    """
    schedule_manager.add_schedule(request.time, request.content)
    return JSONResponse(content={"status": "ok"})


class UserMessage(BaseModel):
    message: str = Field(..., description="String with the content of the message that is sent to the user")


@app.post('/send_message_to_user')
async def send_message_to_user(request: UserMessage):
    """
    Send a message to the user.

    Sends the provided message to the user.
    Use this endpoint as a way to respond to the user's messages.
    Send a message to the user whenever user asks for anything.
    """
    console_chat.print_answer(request.message)
    return JSONResponse(content={"status": "ok"})


class UserNameModel(BaseModel):
    user_name: str


@app.put('/set_user_name')
async def set_user_name(request: UserNameModel):
    """
    Set the user name.

    Sets the user name to be used in the conversation.
    """
    console_chat.set_user_name(request.user_name)
    return JSONResponse(content={"status": "ok"})


class AgentNameModel(BaseModel):
    agent_name: str


@app.put('/set_agent_name')
async def set_agent_name(request: AgentNameModel):
    """
    Set the agent name.

    Sets the agent name to be used in the conversation.
    """
    console_chat.set_agent_name(request.agent_name)
    return JSONResponse(content={"status": "ok"})


def main():
    try:
        try:
            uvicorn.run(app, host="0.0.0.0", port=8001)
        finally:
            context_manager.close()
            memory_manager.close()
            schedule_manager.close()
            console_chat.close()
    finally:
        os._exit(0)


if __name__ == '__main__':
    main()
