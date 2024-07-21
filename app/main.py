from interactions import Client, Intents, listen

from app.core.constants import BOT_TOKEN

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    print(f"message received: {event.message.jump_url}")


bot.start(BOT_TOKEN)
