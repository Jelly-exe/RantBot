import json

import discord
from discord.ext import commands


class Command(commands.Command):
    def __init__(self, *args, **kwargs):
        self.access = kwargs.pop('access')
        super().__init__(*args, **kwargs)


class Group(commands.Group):
    def __init__(self, *args, **kwargs):
        self.access = kwargs.pop('access')
        super().__init__(*args, **kwargs)


class NoPermission(commands.CheckFailure):
    pass


# class PersistentView(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#
#     @discord.ui.button(label="Sea Of Thieves", style=discord.ButtonStyle.grey, custom_id='button:sot')
#     async def SoT(self, button: discord.ui.Button, interaction: discord.Interaction):
#         role = discord.utils.get(interaction.guild.roles, id=894034614086139934)
#         user = discord.utils.get(interaction.guild.members, id=interaction.user.id)
#         thing = None
#         if role in user.roles:
#             await user.remove_roles(role)
#             thing = 'removed.'
#         else:
#             await user.add_roles(role)
#             thing = 'added.'
#
#         await interaction.response.send_message(f'The Sea of Thieves role has been {thing}', ephemeral=True)
#
#     @discord.ui.button(label="Elder", style=discord.ButtonStyle.grey, custom_id='button:elder')
#     async def Elder(self, button: discord.ui.Button, interaction: discord.Interaction):
#         role = discord.utils.get(interaction.guild.roles, id=894034650345898014)
#         user = discord.utils.get(interaction.guild.members, id=interaction.user.id)
#         thing = None
#         if role in user.roles:
#             await user.remove_roles(role)
#             thing = 'removed.'
#         else:
#             await user.add_roles(role)
#             thing = 'added.'
#
#         await interaction.response.send_message(f'The Elder role has been {thing}', ephemeral=True)
#
#
# class Dropdown(discord.ui.Select):
#     def __init__(self):
#         with open("roles2.json", encoding='utf8') as file:
#             self.roles = json.load(file)
#
#         options = [
#             discord.SelectOption(label='Sea of Thieves', description='Add or remove the sea of thieves role', emoji='🦜'),
#             discord.SelectOption(label='Elder', description='Add or remove the elder role', emoji='❤')
#         ]
#         super().__init__(placeholder='Select role...', min_values=1, max_values=1, options=options, custom_id='menu:roles')
#
#     async def callback(self, interaction: discord.Interaction):
#         role = discord.utils.get(interaction.guild.roles, id=self.roles[self.values[0]])
#         user = discord.utils.get(interaction.guild.members, id=interaction.user.id)
#
#         if role in user.roles:
#             await user.remove_roles(role)
#             thing = 'removed.'
#         else:
#             await user.add_roles(role)
#             thing = 'added.'
#
#         await interaction.response.send_message(f'The {self.values[0]} role has been {thing}', ephemeral=True)
#
#
# class PersistentView2(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#
#         self.add_item(Dropdown())
#
#
# class PersistentView3(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#
#     @discord.ui.button(label="Accept Rules", style=discord.ButtonStyle.green, custom_id='button:rules')
#     async def SoT(self, button: discord.ui.Button, interaction: discord.Interaction):
#         role = discord.utils.get(interaction.guild.roles, id=900724805702152254)
#         user = discord.utils.get(interaction.guild.members, id=interaction.user.id)
#
#         if role in user.roles:
#             message = 'You have already accepted the rules.'
#         else:
#             await user.add_roles(role)
#             message = 'You have accepted the rules, and the Swifter role has been added'
#
#         await interaction.response.send_message(message, ephemeral=True)
