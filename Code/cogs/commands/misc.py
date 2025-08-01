import discord
from discord.ext import commands


import logging

from Code.embeds import scemb, eremb

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command('avatar', help='Returns player avatar')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.User = None):
        user = user or ctx.author
        
        msg = discord.Embed()
        msg.set_author(
            name=user.display_name,
            icon_url=user.avatar.url
        )
        msg.set_image(url=user.avatar.url)
        await ctx.reply(embed=msg)
    
    @commands.hybrid_command('userinfo', help='Send user information.', aliases=['playerinfo', 'plrinfo'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        
        msg = discord.Embed(
            description=f'{member.name.capitalize()}\'s Information',
            colour=discord.Colour.brand_green()
        )
        
        roles = [role for role in member.roles if role != ctx.guild.default_role]
        
        if roles:
            roles_str = "\n".join([role.mention for role in roles[:10]])
            if len(roles) > 10:
                roles_str += f"\n(+{len(roles)-10} more)"

            msg.add_field(name=f"Roles [{len(roles)}]", value=roles_str, inline=True)
        else:
            msg.add_field(name="Roles", value="No roles", inline=True)
        
        created_timestamp = int(member.created_at.timestamp())
        msg.add_field(
            name="Create date", 
            value=f"<t:{created_timestamp}:F> (<t:{created_timestamp}:R>)", 
            inline=True
        )
        
        joined_timestamp = int(member.joined_at.timestamp())
        msg.add_field(
            name='Join date',
            value=f'<t:{joined_timestamp}:F> (<t:{joined_timestamp}:R>)',
            inline=True
        )
        
        msg.set_author(
            name=member.name,
            icon_url=member.avatar.url
        )
        
        msg.set_footer(
            text=f'ID: {member.id}'
        )
        
        await ctx.reply(embed=msg)
    
    @commands.hybrid_command('serverinfo', help='Returns a server information', aliases=['srvinfo', 'guildinfo'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverinfo(self, ctx: commands.Context):
        server = ctx.guild
        
        msg = discord.Embed(
            title=f'{server.name.capitalize()} server information',
            colour=discord.Colour.brand_green()
        )
        
        msg.add_field(
            name=f'Total members [{server.member_count}]',
            value=' '
        )
        
        msg.add_field(
            name='Owner',
            value=f'{server.owner.mention}'
        )
        
        created_at = int(server.created_at.timestamp())
        msg.add_field(
            name='Server created',
            value=f'<t:{created_at}:F> (<t:{created_at}:R>)'
        )
        
        msg.set_author(name=f'{server.name.capitalize()}', icon_url=server.icon.url)
        msg.set_thumbnail(url=server.icon.url)
        msg.set_footer(text=f'ID: {server.id}')
        await ctx.reply(embed=msg)
    
async def setup(bot):
    await bot.add_cog(misc(bot))
