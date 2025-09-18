import dictionary_manager

import discord


class Dictionary_Change_Access_Type_View(discord.ui.View):
    def __init__(self, view_owner_id, Dictionary_Manager: dictionary_manager.Dictionary_Manager):
        super().__init__()
        self.view_owner_id: int = view_owner_id
        self.Dictionary_Manager = Dictionary_Manager

    def __interactor_is_owner_check__(self, interactor_id: int) -> bool:
        if interactor_id == self.view_owner_id:
            return True
        return False

    async def __embed_builder__(self, interaction) -> discord.Embed:
        response_embed = discord.Embed(title='Dictionary Access Type Changer', description='', colour=0x00FF00)
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        response_embed.add_field(name='Dictionary Name:', value=self.Dictionary_Manager.data['Name'], inline=False)
        response_embed.add_field(name='Dictionary Owner:', value=f'{interaction.user.name}({interaction.user.id})', inline=False)
        response_embed.add_field(name='Current Access Type:', value=self.Dictionary_Manager.data['Access_Type'], inline=False)
        return response_embed

    @discord.ui.button(label='Set Dictionary To Personal', style=discord.ButtonStyle.green, row=0)
    async def set_to_personal(self, interaction, button):
        if not self.__interactor_is_owner_check__(interaction.user.id):
            return
        await self.Dictionary_Manager.change_dictionary_access_type('personal')
        await interaction.response.edit_message(embed=await self.__embed_builder__(interaction), view=self)

    @discord.ui.button(label='Set Dictionary To Group', style=discord.ButtonStyle.red, row=1)
    async def set_to_group(self, interaction, button):
        if not self.__interactor_is_owner_check__(interaction.user.id):
            return
        await self.Dictionary_Manager.change_dictionary_access_type('group')
        await interaction.response.edit_message(embed=await self.__embed_builder__(interaction), view=self)