from aiohttp.web import Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, MemoryStorage, UserState
from botbuilder.schema import Activity
from dialogs import UserProfileDialog
from bots import DialogBot
from flask import Flask,request,Response
from config import DefaultConfig
import asyncio


app = Flask(__name__)
loop = asyncio.get_event_loop()


SETTINGS = BotFrameworkAdapterSettings("dd17a8e2-70d5-4f9f-ab1e-fb74ba6972bf", "hDB8Q~YpMMBU7lpExYhxAY3cpTlsuS7-..hvCaCy")
adapter = BotFrameworkAdapter(SETTINGS)


# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# create main dialog and bot
DIALOG = UserProfileDialog(USER_STATE)
bot = DialogBot(DefaultConfig.EXPIRE_AFTER_SECONDS,CONVERSATION_STATE, USER_STATE, DIALOG)


@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await bot.on_turn(turncontext)

    task = loop.create_task(
        adapter.process_activity(activity,auth_header,call_fun))
    loop.run_until_complete(task)


if __name__ == '__main__':
    app.run('localhost',3978)