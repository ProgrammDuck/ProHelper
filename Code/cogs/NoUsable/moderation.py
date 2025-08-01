import discord
import asyncio
from discord.ext import commands
import logging
import datetime

from Code.embeds import scemb, eremb

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot  = bot
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command('kick', help='Kick a user from the server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if member == ctx.author:
            raise commands.CommandError("yourself")
        elif member == ctx.guild.me:
            raise commands.CommandError("bot_doing")
        elif ctx.guild.me.top_role <= member.top_role:
            raise commands.CommandError("BotRoleTooLow")
        
        msg = scemb.copy()
        msg.description = f'{member.mention} has been kicked for `{reason}` by {ctx.author.mention}'
        await ctx.send(embed=msg)
        self.logger.info(f'[KICK] Kicked the NAME: {member.name} | ID: {member.id} for {reason} by NAME: {ctx.author.name} | ID: {ctx.author.id}')
        
        msg.title = 'Kicked'
        msg.description = f'You have been kicked for `{reason}` by {ctx.author.mention} from **{ctx.guild.name.capitalize()}**'
        msg.colour = discord.Colour.brand_red()
        try:
            await member.send(embed=msg)
        except discord.Forbidden:
            pass
        
        await member.kick(reason=reason)

    @commands.hybrid_command('mute', help='Mute a user in the server')
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, duration: str, *, reason=None):
        if member == ctx.author:
            raise commands.CommandError("yourself")
        elif member == ctx.guild.me:
            raise commands.CommandError("bot_doing")
        elif ctx.guild.me.top_role <= member.top_role:
            raise commands.CommandError("BotRoleTooLow")
        
        if member.is_timed_out() == True:
            msg = eremb.copy()
            msg.description = 'User already muted.'
            await ctx.reply(embed=msg)
            return
        
        duration = duration.lower()
        if duration.endswith('d'):
            time = int(duration[:-1]) * 86400
        elif duration.endswith('h'):
            time = int(duration[:-1]) * 3600
        elif duration.endswith('m'):
            time = int(duration[:-1]) * 60
        elif duration.endswith('s'):
            time = int(duration[:-1])
        else:
            msg = eremb.copy()
            msg.description = 'Invalid duration format. Use **d for days**, **h for hours**, **m for minutes**, **s for seconds.**'
            await ctx.reply(embed=msg)
            return
        
        if time > 2419200:
            time = 2419199
            msg = eremb.copy()
            msg.description = 'Im can mute only for 28 days! (discord restriction).\nYour mute became 28 days.'
            duration = '28d'
            await ctx.reply(embed=msg)
        elif time == 2419200:
            time = 2419199
            duration = '28d'
            
        until = discord.utils.utcnow() + datetime.timedelta(seconds=time)
                
        await member.timeout(until, reason=reason)
        msg = scemb.copy()
        msg.description = f'{member.mention} has been muted for **{duration}** for `{reason}` by {ctx.author.mention}'
        self.logger.info(f'[MUTE] NAME: {member.name} | ID: {member.id} has been muted for {reason} by NAME: {ctx.author.name} | ID: {ctx.author.id}')
        await ctx.reply(embed=msg)
        msg.title = 'Muted'
        msg.description = f'You have been muted for **{duration}** for `{reason}` by {ctx.author.mention} in **{ctx.guild.name.capitalize()}**'
        msg.colour = discord.Colour.brand_red()
        try:
            await member.send(embed=msg)
        except discord.Forbidden:
            pass



    @commands.hybrid_command('unmute', help='Unmute a user in the server')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        if member.is_timed_out() == True:
            await member.timeout(None)
            self.logger.info(f'[UNMUTE] NAME: {member.name} | ID: {member.id} has been unmuted by NAME: {ctx.author.name} | ID: {ctx.author.id}')
            msg = scemb.copy()
            msg.description = f'{member.mention} has been unmuted.'
            await ctx.reply(embed=msg)
            msg.title = 'Unmuted'
            msg.description = f'You have been unmuted in **{ctx.guild.name.capitalize()}** by {ctx.author.mention}'
            msg.colour = discord.Colour.brand_green()
            try:
                await member.send(embed=msg)
            except discord.Forbidden:
                pass
        else:
            msg = eremb.copy()
            msg.description = 'Member is not muted.'
            await ctx.reply(embed=msg)












    @commands.hybrid_command('ban', help='Ban a user.\n**__MAY BE BROKEN IF THE BOT IS RELAUNCHED__**')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.User, duration: str, *, reason=None):
        gm = ctx.guild.get_member(member.id)
        obj = discord.Object(id=member.id)
        
        try:
                ban_entry = await ctx.guild.fetch_ban(member)
                msg = eremb.copy()
                msg.description = f"{member.mention} already banned. Reason: `{ban_entry.reason or 'None'}`"
                await ctx.send(embed=msg)
                return
        except discord.NotFound:
            pass
        
        duration = duration.lower()
        if duration.endswith('d'):
            time = int(duration[:-1]) * 86400
        elif duration.endswith('h'):
            time = int(duration[:-1]) * 3600
        elif duration.endswith('m'):
            time = int(duration[:-1]) * 60
        elif duration.endswith('s'):
            time = int(duration[:-1])
        else:
            msg = eremb.copy()
            msg.description = 'Invalid duration format. Use **d for days**, **h for hours**, **m for minute**, **s for seconds.**'
            await ctx.send(embed=msg)
            return

        
        if gm:
            member = gm
            if member == ctx.author:
                raise commands.CommandError("yourself")
            elif member == ctx.guild.me:
                raise commands.CommandError("bot_doing")
            elif ctx.guild.me.top_role <= member.top_role:
                raise commands.CommandError("BotRoleTooLow")
            
            msg = scemb.copy()
            msg.description = f'{member.mention} has been banned for **{duration}** for `{reason}` by {ctx.author.mention}'
            self.logger.info(f'[BAN] NAME: {member.name} | ID: {member.id} has been banned for {reason} by NAME: {ctx.author.name} | ID: {ctx.author.id}')
            await ctx.send(embed=msg)
            msg.title = 'Banned'
            msg.description = f'You have been banned for **{duration}** for `{reason}` by {ctx.author.mention} in **{ctx.guild.name.capitalize()}**'
            msg.colour = discord.Colour.brand_red()
            await member.send(embed=msg)
            
            await ctx.guild.ban(member)
            await asyncio.sleep(time)
            await ctx.guild.unban(member)
            
            msg.title = 'Unbanned'
            msg.description = f'You have been unbanned from **{ctx.guild.name.capitalize()}**. Please, dont break rules'
            msg.colour = discord.Colour.brand_green()
            try:
                await member.send(embed=msg)
            except discord.Forbidden:
                pass
        else:
            msg = scemb.copy()
            msg.description = f'{member.mention} has been banned for **{duration}** for `{reason}` by {ctx.author.mention}'
            self.logger.info(f'[BAN] NAME: {member.name} | ID: {member.id} has been banned for {reason} by NAME: {ctx.author.name} | ID: {ctx.author.id}')
            await ctx.send(embed=msg)
            msg.title = 'Banned'
            msg.description = f'You have been banned for **{duration}** for `{reason}` by {ctx.author.mention} in **{ctx.guild.name.capitalize()}**'
            msg.colour = discord.Colour.brand_red()
            await member.send(embed=msg)
            
            await ctx.guild.ban(obj, reason=reason)
            await asyncio.sleep(time)
            await ctx.guild.unban(member)
            
            msg.title = 'Unbanned'
            msg.description = f'You have been unbanned from **{ctx.guild.name.capitalize()}**. Please, dont break rules'
            msg.colour = discord.Colour.brand_green()
            try:
                await member.send(embed=msg)
            except discord.Forbidden:
                pass
        
        
        
        
    @commands.hybrid_command('unban', help='Unban a user from the server')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User):
        try:
            await ctx.guild.unban(user)
            
            self.logger.info(f'[UNBAN] NAME: {user.name} | ID: {user.id} has been unbanned by NAME: {ctx.author.name} | ID: {ctx.author.id}')
            
            msg = scemb.copy()
            msg.description = f'{user.mention} has been unbanned.'
            await ctx.reply(embed=msg)
            msg.title = 'Unbanned'
            msg.description = f'You have been unbanned from **{ctx.guild.name.capitalize()}** by {ctx.author.mention}. Please, dont break rules'
            msg.colour = discord.Colour.brand_green()
            try:
                await user.send(embed=msg)
            except discord.Forbidden:
                pass
        except discord.NotFound:
            msg = eremb.copy()
            msg.description = f'**{user.mention}** is not banned.'
            await ctx.reply(embed=msg)
        
        
        
        
        
        
        
        # try:
        #     if user is None:
        #         raise commands.UserNotFound("user")
        # except commands.UserNotFound:
        #     msg = eremb.copy()
        #     msg.description = 'User not found.'
        #     await ctx.reply(embed=msg)
        #     return

        # try:
        #     await ctx.guild.fetch_ban(user)
        # except discord.NotFound:
        #     msg = eremb.copy()
        #     msg.description = f'**{user.name.capitalize()}** is not banned.'
        #     await ctx.reply(embed=msg)
        #     return

        # await ctx.guild.unban(user)
        # self.logger.info(f'[UNBAN] **{user.name.capitalize()}** has been unbanned by **{ctx.author.name}')
        
        # msg = scemb.copy()
        # msg.description = f'**{user.capitalize()}** has been unbanned.'
        # await ctx.reply(embed=msg)
    
async def setup(bot):
    await bot.add_cog(moderation(bot))
