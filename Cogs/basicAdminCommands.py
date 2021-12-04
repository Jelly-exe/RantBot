import inspect
import time

import discord
from discord.ext import commands

from Utils.classes import Command, Group


class BasicAdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.group(name='say',
                    invoke_without_command=True,
                    usage='say [text/embed]',
                    description='Make the bot say something.',
                    cls=Group,
                    access='botAdmin')
    async def say(self, context):
        raise commands.MissingRequiredArgument(inspect.Parameter('UsageError', inspect.Parameter.POSITIONAL_ONLY))

    @commands.is_owner()
    @say.command(name='text',
                 description='Make the bot say something in message format.',
                 usage='say text [text]',
                 access='botAdmin',
                 cls=Command)
    async def text_say(self, context, *, content):
        time.sleep(0.05)
        await context.message.delete()
        await context.send(content)

    @commands.is_owner()
    @say.command(name='embed',
                 description='Make the bot say something in message format.',
                 usage='say embed [embed title;embed content]',
                 access='botAdmin',
                 cls=Command)
    async def embed_say(self, context, *, content):
        client = self.client
        content = content.split(';')

        if len(content) != 2:
            raise commands.MissingRequiredArgument(inspect.Parameter('UsageError', inspect.Parameter.POSITIONAL_ONLY))

        embed = discord.Embed(
            title=content[0],
            description=content[1],
            colour=client.config['embed']['colour']
        )
        embed.set_footer(text=client.config['embed']['footer']['text'], icon_url=client.config['embed']['footer']['url'])

        time.sleep(0.05)
        await context.message.delete()
        await context.send(embed=embed)

    @commands.is_owner()
    @commands.command(name='react',
                      description='React to a message with a reaction (Must run in channel)',
                      usage='react [message id] [reaction]',
                      access='botAdmin',
                      cls=Command)
    async def react(self, context, messageId, reaction):
        time.sleep(0.05)
        await context.message.delete()

        message = await context.message.channel.fetch_message(messageId)
        await message.add_reaction(reaction)

    @commands.is_owner()
    @commands.command(name='link',
                      description='Manually link a user with a valorant account',
                      usage='link [user] [name]#[tag]',
                      access='botAdmin',
                      cls=Command)
    async def link(self, context, user: discord.Member, name):
        client = self.client

        thing = name.split("#")


def setup(client):
    client.add_cog(BasicAdminCommands(client))
