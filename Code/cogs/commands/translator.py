import discord
from discord.ext import commands

import logging
import aiohttp
from deep_translator import GoogleTranslator

from Code.embeds import scemb, eremb

class translator(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command('translate', aliases=['trans'], help='Translator')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def translate(self, ctx, to_lang = "en", *, text):
        try:
            translated = GoogleTranslator(source='auto', target=to_lang).translate(text)
            msg = scemb.copy()
            msg.description = f'```{translated}```'
            await ctx.reply(embed=msg)
        
        except Exception as e:
            msg = eremb.copy()
            msg.description = f"Error: {str(e)}"
            await ctx.send(embed=msg)
            
async def setup(bot):
    await bot.add_cog(translator(bot))
