import time

from dotenv import load_dotenv
import os
import discord
from discord import app_commands 
import pickle
import asyncio

class Server():
    pass

class Servers():
    def __init__(self):
        self.servers = {}

    async def add_server(self, server_id):
        self.servers.update({server_id: Server()})

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.data = Servers()
    async def setup_hook(self):
        await self.tree.sync()



intents = discord.Intents.default()
client = MyClient(intents=intents)

async def save():
    try: 
        os.mkdir("./data")
    except FileExistsError:
        pass
    with open ("./data/save.pkl", "wb") as output:
        pickle.dump(client.data, output, pickle.HIGHEST_PROTOCOL)

async def load():
    try:
        with open("./data/save.pkl", "rb") as output:
            client.data = pickle.load(output)
    except FileNotFoundError:
        pass



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------') # Used to signal to docker that the container is running

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    if interaction.app_permissions.administrator == True:
        await interaction.response.send_message(f'You are an admin')
    else:
        await interaction.response.send_message(f'You are not an admin')
    
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token) 