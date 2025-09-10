import dictionary_manager

import discord


class Dictionary_Change_Access_Type_View(discord.ui.View):
    def __init__(self, automaton, dictionary_name: str, view_owner_id: int):
        super().__init__()
        self.automaton = automaton
        self.dictionary_name: str = dictionary_name
        self.view_owner_id: int = view_owner_id

    def interactor_is_owner_check(self, interactor_id: int) -> bool:
        if interactor_id == self.view_owner_id:
            return True
        return False

    async def embed_builder(self, interaction, dictionary_data: dict) -> discord.Embed:
        response_embed = discord.Embed(title='Dictionary Access Type Changer', description='', colour=0x00FF00)
        response_embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        response_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        response_embed.add_field(name='Dictionary Name:', value=dictionary_data['Name'], inline=False)
        response_embed.add_field(name='Dictionary Owner:', value=f'{interaction.user.name}({interaction.user.id})',
                                 inline=False)
        response_embed.add_field(name='Current Access Type:', value=dictionary_data['Access_Type'], inline=False)
        return response_embed

    @discord.ui.button(label='Set Dictionary To Personal', style=discord.ButtonStyle.green, row=0)
    async def set_to_personal(self, interaction, button):
        if not self.interactor_is_owner_check(interaction.user.id):
            return

        dictionary_manager.change_dictionary_access_type(self.dictionary_name, self.view_owner_id, 'personal')
        dictionary_data: dict = dictionary_manager.get_dictionary_data(self.dictionary_name, self.view_owner_id)

        await interaction.response.edit_message(embed=await self.embed_builder(interaction, dictionary_data), view=self)

    @discord.ui.button(label='Set Dictionary To Group', style=discord.ButtonStyle.green, row=1)
    async def set_to_group(self, interaction, button):
        if not self.interactor_is_owner_check(interaction.user.id):
            return

        dictionary_manager.change_dictionary_access_type(self.dictionary_name, self.view_owner_id, 'group')
        dictionary_data: dict = dictionary_manager.get_dictionary_data(self.dictionary_name, self.view_owner_id)

        await interaction.response.edit_message(embed=await self.embed_builder(interaction, dictionary_data), view=self)
