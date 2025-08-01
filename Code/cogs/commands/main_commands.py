import discord
from discord.ext import commands
from discord.ui import Button, View

import math
import logging

from Code.embeds import scemb, eremb

class main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        
    
    @commands.hybrid_command('clear', help='Clearing messages', aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, value = 10):
        deleted = await ctx.channel.purge(limit=value)
        
        msg = scemb.copy()
        msg.description = f'{len(deleted)} messages cleared'
        self.logger.info(f'[CLEAR] {ctx.author.name} cleared {len(deleted)} messages in {ctx.channel.id}')
        
        await ctx.send(embed=msg, delete_after=5)
        
    @commands.hybrid_command('echo', help='Repeat your message')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def echo(self, ctx, *, message):
        self.logger.info(f'[ECHO] {ctx.author.name} - {message}')
        await ctx.reply(message)
        
        
    @commands.hybrid_command('about', help='Information of the bot.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def about(self, ctx):
        msg = discord.Embed(
            title='Information',
            description='This is a open-source bot\n - [Github](https://github.com/ProgrammDuck/ProHelper)\n   - created by <@916019025945976842>. He is my Dad). I have only 1 developer. You can change this bot for your hope, This all.',
            colour=discord.Colour.blue()
        )

        await ctx.reply(embed=msg)

    @commands.hybrid_command('ping', help='Check if the bot is online')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply('Pong!')

    @commands.hybrid_command('help', help='List all available commands')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx, command_name: str = None):
        if command_name:
            command = self.bot.get_command(command_name)
            if command and not command.hidden:
                msg = discord.Embed(
                    description=f'Argument:\n`[]` - optional\n`<>` - required',
                    colour=discord.Colour.blue()
                )
                msg.add_field(name=command.name.capitalize(), value=f'{command.help}\nUsage: `{self.bot.command_prefix}{command.name} {command.signature}`', inline=False)
                await ctx.reply(embed=msg)
            else:
                msg = eremb.copy()
                msg.description = f'Command `{command_name}` not found.'
                await ctx.reply(embed=msg)
        else:
            commands_list = [command for command in self.bot.commands if not command.hidden]
            if not commands_list:
                msg = eremb.copy()
                msg.description = 'No commands available.'
                await ctx.reply(embed=msg)
                return

            commands_per_pages = 5
            
            pages = []
            for i in range(0, len(commands_list), commands_per_pages):
                page = discord.Embed(
                    title='Available Commands',
                    description=f'Use `{self.bot.command_prefix}` as the prefix for all commands.\nPage {len(pages) + 1}/{math.ceil(len(commands_list) / commands_per_pages)}\n\nArgument:\n`[]` - optional\n`<>` - required\n',
                    colour=discord.Colour.blue()
                )
                
                for command in commands_list[i:i+commands_per_pages]:
                    page.add_field(name=command.name.capitalize(), value=f'{command.help}\nUsage: `{self.bot.command_prefix}{command.name} {command.signature}`', inline=False)
                pages.append(page)

            current_page = 0

            class HelpView(View):
                def __init__(self, pages, current_page):
                    super().__init__()
                    self.pages = pages
                    self.current_page = current_page
                    self.update_buttons()
                
                def update_buttons(self):
                    self.previous.disabled = (self.current_page == 0)
                    self.next.disabled = (self.current_page == len(self.pages) - 1)
        
                @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary)
                async def previous(self, interaction: discord.Interaction, button: Button):
                    self.current_page -= 1
                    self.update_buttons()
                    await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

                @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
                async def next(self, interaction: discord.Interaction, button: Button):
                    self.current_page += 1
                    self.update_buttons()
                    await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

            view = HelpView(pages, current_page)
            await ctx.reply(embed=pages[current_page], view=view)
        
    
async def setup(bot):
    await bot.add_cog(main(bot))
