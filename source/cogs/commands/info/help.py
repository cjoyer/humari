# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        container = disnake.ui.Container(
            disnake.ui.TextDisplay(content="## Команды"),
            disnake.ui.TextDisplay(content="### 📋 Информация\n`/help` , `/host` , `/server` , `/user`"),
            disnake.ui.TextDisplay(content="### 🛡️ Модерация\n`/clear` , `/ban` , `/kick`"),
        )

        await inter.response.send_message(
            components=[container],
            flags=disnake.MessageFlags(is_components_v2=True),
            ephemeral=True
        )

def setup(client):
    client.add_cog(Help(client))