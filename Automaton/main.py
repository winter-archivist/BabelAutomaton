import json
import time

import discord
from discord import app_commands

with open('Automaton/config.json', 'r') as opened_file:
    config: dict = json.load(opened_file)
auto_sync: bool = config['auto_sync']
reconnect: bool = config['reconnect']
prefix: str = config['prefix']
token: str = config['token']

testing_guild_id: int = 601192368489758731

intents = discord.Intents.all()
automaton = discord.Client(intents=intents)
tree = app_commands.CommandTree(automaton)


@automaton.event
async def on_ready():
    print('--------Automaton Loading Began')
    await tree.sync(guild=discord.Object(id=testing_guild_id))
    await automaton.change_presence(status=discord.Status.online)
    print('--------Bot Online')


@tree.command(
    name="test_command",
    description="test command",
    # To be Removed
    guild=discord.Object(id=testing_guild_id)
    # To be Removed
)
async def test_command(interaction):
    await interaction.response.send_message("ping-PONG")


if __name__ == '__main__':
    automaton.run(token=token, reconnect=reconnect)
