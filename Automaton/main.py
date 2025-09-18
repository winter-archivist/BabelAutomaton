import json

import dictionary_manager
import views

import discord
from discord import app_commands

# TODO:
    # fix the 'share' perm check so that others can share the dictionary


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

def __user_access_change_embed_builder__(interaction, Dictionary_Manager) -> discord.Embed:
    embed = discord.Embed(title='Dictionary Access', description='', colour=0x00FF00)
    embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.name, inline=False)
    embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Creator']['user']} ({Dictionary_Manager.data['Creator']['id']})', inline=False)
    return embed

@automaton.event
async def on_ready():
    print('Automaton Loading Began')

    if auto_sync:
        print('Auto-Sync is enabled, syncing...')
        await tree.sync(guild=discord.Object(id=testing_guild_id))
    else:
        print('Auto-Sync is disabled, skipping sync...')

    await automaton.change_presence(status=discord.Status.online)
    print('Automaton Ready for Use')

@tree.command(name="create_dictionary", description="Creates a new babel dictionary", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
@app_commands.choices(access_type=[
    app_commands.Choice(name="Personal", value="personal"),
    app_commands.Choice(name="Group", value="group")
])
async def create_dictionary_command(interaction: discord.Interaction, dictionary_name: str, access_type: app_commands.Choice[str]):
    dictionary_manager.make_dictionary(dictionary_name, interaction.user.id, interaction.user.name, access_type.value)

    response_embed = discord.Embed(title='Dictionary Creation', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)

    response_embed.add_field(name='Dictionary Name:', value=dictionary_name, inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{interaction.user.name}({interaction.user.id})', inline=False)
    response_embed.add_field(name='Access Type:', value=access_type.value, inline=False)

    await interaction.response.send_message(embed=response_embed)

@tree.command(name="change_dictionary_access_type", description="Changes the access type of a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
async def change_dictionary_access_type_command(interaction: discord.Interaction, dictionary_name: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(dictionary_name, interaction.user.id)

    response_embed = discord.Embed(title='Dictionary Access Type Changer', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=Dictionary_Manager.name, inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{interaction.user.name}({interaction.user.id})', inline=False)
    response_embed.add_field(name='Current Access Type:', value=Dictionary_Manager.data['Access_Type'], inline=False)

    await interaction.response.send_message(embed=response_embed, view=views.Dictionary_Change_Access_Type_View(interaction.user.id, Dictionary_Manager))

@tree.command(name="add_user_to_dictionary", description="Gives a user access to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
@discord.app_commands.describe(dictionary_owner_id='Dictionary Owner ID')
@discord.app_commands.describe(user_id='User ID')
@discord.app_commands.describe(user_name='User Name')
async def add_user_to_dictionary(interaction: discord.Interaction, dictionary_name: str, dictionary_owner_id: str, user_id: str, user_name: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(dictionary_name, int(dictionary_owner_id))
    await Dictionary_Manager.give_user_access_to_dictionary(interaction.user.id, int(user_id), user_name)
    await interaction.response.send_message(embed=__user_access_change_embed_builder__(interaction, Dictionary_Manager))

@tree.command(name="remove_user_from_dictionary", description="Remove a user's access to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
@discord.app_commands.describe(dictionary_owner_id='Dictionary Owner ID')
@discord.app_commands.describe(user_id='User ID')
async def remove_user_from_dictionary(interaction: discord.Interaction, dictionary_name: str, dictionary_owner_id: str, user_id: str):
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(dictionary_name, int(dictionary_owner_id))
    await Dictionary_Manager.remove_user_access_to_dictionary(interaction.user.id, int(user_id))
    await interaction.response.send_message(embed=__user_access_change_embed_builder__(interaction, Dictionary_Manager))

@tree.command(name="add_word_to_dictionary", description="Adds a word to a target dictionary.", guild=discord.Object(id=testing_guild_id))
@discord.app_commands.describe(dictionary_name='Dictionary Name')
@discord.app_commands.describe(dictionary_owner_id='Dictionary Owner ID')
@discord.app_commands.describe(word='Word')
async def add_word_to_dictionary(interaction: discord.Interaction, dictionary_name: str, dictionary_owner_id: str, word: str):
    dictionary_owner_id: int = int(dictionary_owner_id)
    Dictionary_Manager = dictionary_manager.Dictionary_Manager(dictionary_name, dictionary_owner_id)
    await Dictionary_Manager.add_word_to_dictionary(interaction.user.id, word)

    response_embed = discord.Embed(title='Dictionary Access', description='', colour=0x00FF00)
    response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
    response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
    response_embed.add_field(name='Dictionary Name:', value=dictionary_name, inline=False)
    response_embed.add_field(name='Dictionary Owner:', value=f'{Dictionary_Manager.data['Creator']['user']}{Dictionary_Manager.data['Creator']['id']}', inline=False)
    response_embed.add_field(name='Current Words In Dictionary:', value=Dictionary_Manager.data['Words'], inline=False)

    await interaction.response.send_message(embed=response_embed)

if __name__ == '__main__':
    automaton.run(token=token, reconnect=reconnect)
