import discord
from discord.ext import commands
import qrcode
from qrcode.main import QRCode
import re
from colour import Color
import io

import logging

from Code.embeds import scemb, eremb

class qr_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.hybrid_command('qrcode', help='Creates qrcode')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def qrcode(self, ctx, data, backgroundcolor:str = "white", color:str = "black"):
        try:
            qr = QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            async def is_hex_color(hexcolor):
                hex_color_pattern = r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$'
                return bool(re.match(hex_color_pattern, hexcolor))

            async def is_name_color(color):
                try:
                    color = color.replace(" ", "")
                    Color(color)
                    return True
                except ValueError:
                    return False

            async def is_correct_colors(bg, fg):
                if not (await is_hex_color(bg) or await is_name_color(bg)):
                    msg = eremb.copy()
                    msg.description = 'Background color incorrect!'
                    await ctx.reply(embed=msg)
                    return False
                elif not (await is_hex_color(fg) or await is_name_color(fg)):
                    msg = eremb.copy()
                    msg.description = 'Qr color incorrect!'
                    await ctx.reply(embed=msg)
                    return False
                return True

            valid_colors = await is_correct_colors(backgroundcolor, color)
            if not valid_colors:
                return


            img = qr.make_image(
                fill_color=color,
                back_color=backgroundcolor
            )

            type(img)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(buffer, filename="qrcode.png")

            msg = scemb.copy()
            msg.set_image(url='attachment://qrcode.png')

            await ctx.reply(embed=msg, file=file)

        except Exception as e:
            await ctx.reply(e)





async def setup(bot):
    await bot.add_cog(qr_command(bot))
