from typing import Union
from Handlers.AbstractHandler import AbstractHandler
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Music.VulkanBot import VulkanBot
from Parallelism.AbstractProcessManager import AbstractPlayersManager
from Parallelism.Commands import VCommands, VCommandsType


from discord import Interaction
from discord.ext.commands import Context

from UI.Buttons.LyricsDropdown import LyricsDropdown
from UI.Views.BasicView import BasicView


class LyricsHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self) -> HandlerResponse:
        dropdown = LyricsDropdown(self.bot, LyricsSelectionHandler, ["hello", "hello2", "hello3"], self.ctx.channel, self.ctx.guild, MessagesCategory.OTHERS)
        view = BasicView(self.bot, [dropdown], self.config.LYRICS_VIEW_TIMEOUT)
        return HandlerResponse(self.ctx, self.embeds.LYRICS(), view=view)   

class LyricsSelectionHandler(AbstractHandler):
    def __init__(self, ctx: Union[Context, Interaction], bot: VulkanBot) -> None:
        super().__init__(ctx, bot)

    async def run(self, selectedLyric:str) -> HandlerResponse:
        return HandlerResponse(self.ctx, self.embeds.LYRICS_SELECTED(selectedLyric))