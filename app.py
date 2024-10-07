import time

from dotenv import load_dotenv
import os
import discord
from discord import app_commands 
import pickle
import asyncio

class Member():
    def __init__(self, member_id):
        self.member_id = member_id
        self.rank = 0
        self.organization = Organization()
        
    async def set_rank(self, rank):
        self.rank = rank
        
    async def set_organization(self, organization):
        self.organization = organization
        
    async def get_rank(self):
        return self.rank
    
    async def get_organization(self):
        return self.organization
    
    async def get_member_id(self):
        return self.member_id

class Organization():
    def __init__(self):
        self.leadership = {}
        self.members = {}
        self.name = ""
        
    async def add_member(self, member_id):
        self.members.update({member_id: Member(member_id)})

    async def add_leader(self, member_id):
        self.leadership.update({member_id: Member(member_id)})

    async def remove_member(self, member_id):
        self.members.pop(member_id)
        
    async def remove_leader(self, member_id):
        self.leadership.pop(member_id)
        
    async def set_name(self, name):
        self.name = name


class Server():
    def __init__(self):
        self.organizations = {}

    async def add_organization(self, organization_name):
        self.organizations.update({organization_name: Organization()})

    async def remove_organization(self, organization_name):
        self.organizations.pop(organization_name)
        
    async def get_organization(self, organization_name):
        return self.organizations[organization_name]
    

class Servers():
    def __init__(self):
        self.servers = {}

    async def add_server(self, server_id):
        self.servers.update({server_id: Server()})
        
    async def remove_server(self, server_id):
        self.servers.pop(server_id)
    
    async def get_server(self, server_id):
        return self.servers[server_id]
    

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
    if interaction.user.resolved_permissions.administrator == True:
        await interaction.response.send_message(f'You are an admin')
    else:
        await interaction.response.send_message(f'You are not an admin')
    
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
client.run(token) 