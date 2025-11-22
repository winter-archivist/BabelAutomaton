import json
import os

import dictionary_manager
import views

import discord
from discord import app_commands

# TODO:
    # fix the 'share' perm check so that others can share the dictionary
    # add_word_to_dictionary should also have an optional entry for definitions
    # remove_word_from_dictionary, make it

from logger import Logger
logger = Logger()
source: str = 'Main'

CONFIG_LOCATION: str = ''
if os.path.isfile('Automaton/config.json'):
    with open('Automaton/config.json', 'r') as opened_file:
        config: dict = json.load(opened_file)
else:
    logger.log('critical', 'main', '"Automaton/config.json" not found in Automaton/, please reread README.')

if os.path.isfile('Automaton/.client.secret'):
    with open('Automaton/.client.secret', 'r') as opened_file:
        token: str = opened_file.read()
else:
    logger.log('critical', 'main', '".client.secret" not found in Automaton/, please reread README.')

auto_sync: bool = config['auto_sync']
reconnect: bool = config['reconnect']
prefix: str = config['prefix']

testing_guild_id: int = 601192368489758731

intents = discord.Intents.all()
automaton = discord.Client(intents=intents)
tree = app_commands.CommandTree(automaton)

async def __user_access_change_embed_builder__(interaction, Dictionary_Manager) -> discord.Embed:
    embed = discord.Embed(title='Dictionary Access', description='', colour=0x00FF00)
    embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']} ({Dictionary_Manager.data['Owner']['id']})', inline=False)
    embed.add_field(name='Users With Access:', value=', '.join(await Dictionary_Manager.all_access_users()), inline=False)
    return embed

@automaton.event
async def on_ready():
    logger.log('info', f'{source}.on_read()', 'Automaton Loading Began')

    if auto_sync:
        logger.log('info', f'{source}.on_read()', 'Auto-Sync is enabled, syncing...')
        await tree.sync(guild=discord.Object(id=testing_guild_id))
    else:
        logger.log('info', f'{source}.on_read()', 'Auto-Sync is disabled, skipping sync...')

    await automaton.change_presence(status=discord.Status.online)
    logger.log('success', f'{source}.on_read()', 'Automaton Ready for Use')

@tree.command(name="set", description="Sets your target dictionary, this must be done before using the rest of the automaton.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_uuid='Dictionary Unique ID')
async def set_dictionary_command(interaction: discord.Interaction, dictionary_uuid: str):
    dictionary_manager.set_users_target_dictionary_uuid(interaction.user.id, dictionary_uuid)
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)

    response_embed = discord.Embed(title='Dictionary Target', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Access Type:', value=Dictionary_Manager.data['Access_Type'], inline=False)

    await interaction.response.send_message(embed=response_embed)

@tree.command(name="create", description="Creates a new babel dictionary", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
@app_commands.choices(access_type=[
    app_commands.Choice(name="Personal", value="personal"),
    app_commands.Choice(name="Group", value="group")
])
async def create_dictionary_command(interaction: discord.Interaction, dictionary_name: str, access_type: app_commands.Choice[str]):
    dictionary_uuid: str = dictionary_manager.make_dictionary(dictionary_name, interaction.user.id, interaction.user.name, access_type.value)
    dictionary_manager.set_users_target_dictionary_uuid(interaction.user.id, dictionary_uuid)
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)

    response_embed = discord.Embed(title='Dictionary Creation', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Dictionary ID:', value=Dictionary_Manager.data['uuid'], inline=False)
    response_embed.add_field(name='Access Type:', value=Dictionary_Manager.data['Access_Type'], inline=False)

    await interaction.response.send_message(embed=response_embed)

@tree.command(name="change_access_type", description="Changes the access type of a target dictionary.", guild=discord.Object(id=testing_guild_id))
async def change_dictionary_access_type_command(interaction: discord.Interaction):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)

    response_embed = discord.Embed(title='Dictionary Access Type Changer', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Current Access Type:', value=Dictionary_Manager.data['Access_Type'], inline=False)

    await interaction.response.send_message(embed=response_embed, view=views.Dictionary_Change_Access_Type_View(interaction.user.id, Dictionary_Manager))

@tree.command(name="add_user", description="Gives a user access to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(user_id='User ID')
@discord.app_commands.describe(user_name='User Name')
async def add_user_to_dictionary_command(interaction: discord.Interaction, user_id: str, user_name: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)
    await Dictionary_Manager.give_user_access_to_dictionary(interaction.user.id, int(user_id), user_name)
    await interaction.response.send_message(embed=await __user_access_change_embed_builder__(interaction, Dictionary_Manager))

@tree.command(name="remove_user", description="Remove a user's access to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(user_id='User ID')
async def remove_user_from_dictionary_command(interaction: discord.Interaction, user_id: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)
    await Dictionary_Manager.remove_user_access_to_dictionary(interaction.user.id, int(user_id))
    await interaction.response.send_message(embed=await __user_access_change_embed_builder__(interaction, Dictionary_Manager))

# TODO: Change User Permissions Command

@tree.command(name="add_word", description="Adds a word to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(word='Word')
async def add_word_to_dictionary_command(interaction: discord.Interaction, word: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)
    await Dictionary_Manager.add_word_to_dictionary(interaction.user.id, word)

    response_embed = discord.Embed(title='Dictionary Access', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Current Words In Dictionary:', value=Dictionary_Manager.data['Words'], inline=False)

    await interaction.response.send_message(embed=response_embed)

@tree.command(name="remove_word", description="Adds a word to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(word='Word')
async def remove_word_from_dictionary_command(interaction: discord.Interaction, word: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)
    await Dictionary_Manager.remove_word_from_dictionary(interaction.user.id, word)

    response_embed = discord.Embed(title='Dictionary Access', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Name'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Current Words In Dictionary:', value=Dictionary_Manager.data['Words'], inline=False)

    await interaction.response.send_message(embed=response_embed)


@tree.command(name="random", description="Gets a random word from a target dictionary.", guild=discord.Object(id=testing_guild_id))
async def random_command(interaction: discord.Interaction):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(interaction.user.id, logger)
    random_word: str = await Dictionary_Manager.get_random_word_from_dictionary(interaction.user.id)

    response_embed = discord.Embed(title='Dictionary', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.data['Owner']['user'], inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Owner']['user']}({Dictionary_Manager.data['Owner']['id']})', inline=False)
    response_embed.add_field(name='Random Word:', value=random_word, inline=False)

    await interaction.response.send_message(embed=response_embed)


if __name__ == '__main__':
    automaton.run(token=token, reconnect=reconnect)
