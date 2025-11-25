import discord

from dictionaryManager import DictionaryManager

class DictionaryChangeAccessTypeView(discord.ui.View):
    def __init__(self, view_owner_id, dictionary_manager: DictionaryManager):
        super().__init__()
        self.view_owner_id: int = view_owner_id
        self.dictionary_manager = dictionary_manager

    async def __embedBuilder__(self, interaction) -> discord.Embed:
        response_embed = discord.Embed(title='Dictionary Access Type Changer', description='', colour=0x00FF00)
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        response_embed.add_field(name='Dictionary Name:', value=self.dictionary_manager.data['Name'], inline=False)
        response_embed.add_field(name='Dictionary Owner:', value=f'{interaction.user.name}({interaction.user.id})', inline=False)
        response_embed.add_field(name='Current Access Type:', value=self.dictionary_manager.data['Access_Type'], inline=False)
        return response_embed

    @discord.ui.button(label='Set Dictionary To Personal', style=discord.ButtonStyle.green, row=0)
    async def setToPersonal(self, interaction, button):
        if not interaction.user.id == self.view_owner_id:
            return
        await self.dictionary_manager.set_access_type('personal')
        await interaction.response.edit_message(embed=await self.__embedBuilder__(interaction), view=self)

    @discord.ui.button(label='Set Dictionary To Group', style=discord.ButtonStyle.red, row=1)
    async def setToGroup(self, interaction, button):
        if not interaction.user.id == self.view_owner_id:
            return
        await self.dictionary_manager.set_access_type('group')
        await interaction.response.edit_message(embed=await self.__embedBuilder__(interaction), view=self)
