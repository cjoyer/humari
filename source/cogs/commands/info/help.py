# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.slash_command()
  async def help(self, inter: disnake.ApplicationCommandInteraction):
    header = disnake.ui.TextDisplay(content=f"## 📋 Available commands:")

    sep1 = disnake.ui.Separator()

    info_section = disnake.ui.Section(
      disnake.ui.TextDisplay(content=f"## 📋 Information\n`/help`"),
      accessory=disnake.ui.Button(
        style=disnake.ButtonStyle.secondary,
        emoji="▶",
        custom_id="help_info"
      )
    )

    sep2 = disnake.ui.Separator()

    moderation_section = disnake.ui.Section(
      disnake.ui.TextDisplay(content=f"## 🛡️ Moderation\n`clear`"),
      accessory=disnake.ui.Button(
        style=disnake.ButtonStyle.secondary,
        emoji="▶",
        custom_id="moderation_info"
      )
    )

    container = disnake.ui.Container(
      header, sep1, info_section, sep2, moderation_section,
      accent_colour=disnake.Color.blue()
    )
    await inter.response.send_message(
      components=[container],
      flags=disnake.MessageFlags(is_components_v2=True), ephemeral=True
    )

def setup(client):
  client.add_cog(Help(client))