import discord
from client import CustomClient
import commands
import argparse
import asyncio
import nest_asyncio
nest_asyncio.apply()
import json


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="../models/orca-mini-7b.ggmlv3.q4_K_S.bin")
args = parser.parse_args()


async def main():
    BOT_KEY: str = ""
    SERVER_KEY: str = ""
    
    with open("../.key", 'r') as f:
        BOT_KEY = f.readline()
        SERVER_KEY = f.readline()

    intents = discord.Intents.all()
    intents.guilds =  True
    intents.messages = True
    intents.message_content = True
    # intents = discord.Intents(guilds=True,messages=True,message_content=True)

    client = CustomClient(intents=intents, model_path=args.model)
    client.help_command = commands.CHelpCommand()
    await client.add_cog(commands.Ping(client))
    await client.add_cog(commands.Info(client))
    await client.add_cog(commands.Model(client))
    await client.add_cog(commands.Parameterize(client))
    await client.run(BOT_KEY)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except TypeError:
        pass
