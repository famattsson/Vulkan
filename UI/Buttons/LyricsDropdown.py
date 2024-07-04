import asyncio
from typing import List
from discord import Interaction, Message, TextChannel, SelectOption
from discord.ui import Select, View
from Handlers.HandlerResponse import HandlerResponse
from Messages.MessagesCategory import MessagesCategory
from Messages.MessagesManager import MessagesManager
from Music.VulkanBot import VulkanBot
from Handlers.AbstractHandler import AbstractHandler
from UI.Buttons.AbstractItem import AbstractItem
from UI.Views.AbstractView import AbstractView
from Music.Playlist import Playlist


class LyricsDropdown(Select, AbstractItem):
    """Receives n elements to put in drop down and return the selected, pass the index value to a handler"""

    def __init__(self, bot: VulkanBot, handler: type[AbstractHandler], lyricsOptions: List[str], textChannel: TextChannel, guildID: int, category: MessagesCategory):

        selectOptions: List[SelectOption] = []

        for x in range(len(lyricsOptions)):
            selectOptions.append(SelectOption(label=lyricsOptions[x], value=str(x)))

        super().__init__(placeholder="Select a lyric source",
                         min_values=1, max_values=1, options=selectOptions)

        self.__lyricsOptions = lyricsOptions
        self.__channel = textChannel
        self.__guildID = guildID
        self.__category = category
        self.__handlerClass = handler
        self.__messagesManager = MessagesManager()
        self.__bot = bot
        self.__view: AbstractView = None

    async def callback(self, interaction: Interaction) -> None:
        """Callback to when the selection is selected"""
        await interaction.response.defer()

        # Execute the handler passing the value selected
        handler = self.__handlerClass(interaction, self.__bot)
        response: HandlerResponse = await handler.run(self.__lyricsOptions[int(self.values[0])])

        message = None
        if response and response.view is not None:
            message: Message = await self.__channel.send(embed=response.embed, view=response.view)
        elif response.embed:
            message: Message = await self.__channel.send(embed=response.embed)

        # Clear the last sended message in this category and add the new one
        if message:
            await self.__messagesManager.addMessageAndClearPrevious(self.__guildID, self.__category, message, response.view)

    def set_view(self, view: View):
        self.__view = view

    def get_view(self) -> View:
        return self.__view
