import discord
from discord.ext import commands
import logging

from Code.embeds import scemb, eremb




class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__ )
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if ctx.command is not None:
            command = self.bot.get_command(ctx.command.name)
        else:
            command = None
        if isinstance(error, commands.errors.CommandOnCooldown):
            msg = eremb.copy()
            msg.description = str(error)
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.MissingRequiredArgument):
            msg = eremb.copy()
            msg.description = f'Missing required argument.\nUsage: `{self.bot.command_prefix}{command.name} {command.signature}`.'
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.MissingPermissions):
            msg = eremb.copy()
            msg.description = 'You dont have permissions to execute this command.'
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.BotMissingPermissions):
            msg = eremb.copy()
            msg.description = 'Bot doesnt have permissions.'
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.CommandNotFound):
            msg = eremb.copy()
            msg.description = 'Command not found.'
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.MemberNotFound):
            msg = eremb.copy()
            msg.description = 'Member not found.'
            await ctx.reply(embed=msg)
        elif isinstance(error, SyntaxError):
            msg = eremb.copy()
            msg.description = 'Syntax error'
            await ctx.reply(embed=msg)
        elif isinstance(error, commands.CommandError):
            if 'yourself' in str(error):
                msg = eremb.copy()
                msg.description = 'Cannot do it for yourself.'
                await ctx.reply(embed=msg)
            elif 'BotRoleTooLow' in str(error):
                msg = eremb.copy()
                msg.description = 'Bot role too low.'
                await ctx.reply(embed=msg)
            elif 'AuthorRoleTooLow' in str(error):
                msg = eremb.copy()
                msg.description = 'You cannot do it for member with a role higher or equal to yours.'
                await ctx.reply(embed=msg)
            elif 'bot_doing' in str(error):
                msg = eremb.copy()
                msg.description = 'Cannot do it for myself'
                await ctx.reply(embed=msg)
            elif 'HTTP' in str(error):
                msg = eremb.copy()
                msg.description = f"Discord API error. Try again later. (`{error}`)"
                await ctx.reply(embed=msg)
        
        elif isinstance(error, discord.HTTPException):
            msg = eremb.copy()
            msg.description = "Discord API error. Try again later."
            await ctx.reply(embed=msg)
        else:
            self.logger.error(f"Unhandled error: `{error}`.")
            msg = eremb.copy()
            msg.description = f'An error has occurred: `{error}`.'
            await ctx.reply(embed=msg)
        
            
            
async def setup(bot):
    await bot.add_cog(errors(bot))
