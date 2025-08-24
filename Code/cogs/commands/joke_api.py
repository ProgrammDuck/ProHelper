import discord
from discord.ext import commands

import logging
import aiohttp

from Code.embeds import scemb, eremb

class joke_api(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command('joke', help='Return a joke.')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def joke(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://v2.jokeapi.dev/joke/Any?type=twopart') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title='😂 joke!',
                            description=f'**{data["setup"]}\n{data["delivery"]}**',
                            colour=discord.Colour.orange()
                        )

                        # embed.set_footer(text=f"The \"{self.bot.command_prefix}joke\" command provides random cat images using a public API. This is done through integration with The Joke API, one of the most trusted sources of cat images on the web. (Powered by The Joke API - https://sv443.net/jokeapi/v2/)")
                        await ctx.send(embed=embed)
                    else:
                        msg = eremb.copy()
                        msg.description = 'API error'
                        await ctx.send(embed=msg)
        
        except Exception as e:
            msg = eremb.copy()
            msg.description = f"Error: {str(e)}"
            await ctx.send(embed=msg)
            
async def setup(bot):
    await bot.add_cog(joke_api(bot))
