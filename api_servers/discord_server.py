import discord
import requests
from discord.ext import commands

# Replace with your bot token
TOKEN = 'MTI5MTg1NzUwMjU1NTYwNzEyMw.GmjASx.qDffJ4yqOOSmAdqKcOqUJhS08GWJe5tnqxwLxY'

# Replace with the URL of your server to forward messages
FORWARD_URL = 'http://localhost:8000/discord-webhook/'

# Create a bot instance with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Prepare the data to be sent
    data = {
        'content': message.content,
        'author': str(message.author),
        'channel_id': str(message.channel.id),
        'channel': str(message.channel),
        'guild': str(message.guild),
        'timestamp': str(message.created_at)
    }

    # If there are attachments, add their URLs
    if message.attachments:
        data['attachments'] = [attachment.url for attachment in message.attachments]

    # Send the data to your server
    try:
        response = requests.post(FORWARD_URL, json=data)
        if response.status_code == 200:
            print(f"Message forwarded successfully: {message.content}")
        else:
            print(f"Failed to forward message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error forwarding message: {str(e)}")

    # Process commands if any
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    data = {
        'event': 'member_join',
        'member': str(member),
        'guild': str(member.guild)
    }
    requests.post(FORWARD_URL, json=data)


@bot.event
async def on_member_remove(member):
    data = {
        'event': 'member_remove',
        'member': str(member),
        'guild': str(member.guild)
    }
    requests.post(FORWARD_URL, json=data)


# Add more event handlers as needed

bot.run(TOKEN)
