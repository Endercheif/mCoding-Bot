from typing import TYPE_CHECKING
from math import log

from config import MEMBER_COUNT_CHANNEL, MCODING_SERVER
from discord.ext import commands, tasks

if TYPE_CHECKING:
    from app.bot import Bot


class MemberCount(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        if MEMBER_COUNT_CHANNEL is not None:
            self.update_member_count.start()

    def get_member_count(self, guild):
        mc = guild.member_count
        mc_log = round(log(mc, 2), 3)
        if mc_log % 1 == 0:
            mc_log = int(mc_log)
        return f"2**{str(mc_log)}"

    @tasks.loop(minutes=10)
    async def update_member_count(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(MEMBER_COUNT_CHANNEL)
        guild = self.bot.get_guild(MCODING_SERVER)
        await channel.edit(name=(
            f"Members: {self.get_member_count(guild)} ({guild.member_count})"
        ))


def setup(bot: "Bot"):
    bot.add_cog(MemberCount(bot))