# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Server(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(description="Показывает информацию о сервере")
  async def server(self, inter: disnake.ApplicationCommandInteraction):
    if inter.guild is None:
      await inter.response.send_message("Это серверная команда!", ephemeral=True)
      return

    server_name = inter.guild.name
    server_owner = inter.guild.owner
    server_members_count = sum(1 for member in inter.guild.members if not member.bot)
    server_bots_count = sum(1 for member in inter.guild.members if member.bot)
    server_roles_count = len(inter.guild.roles)
    server_categories_count = len(inter.guild.categories)
    server_text_channels_count = len(inter.guild.text_channels)
    server_voice_channels_count = len(inter.guild.voice_channels)

    server_info_embed = disnake.Embed(
      title=f":grey_exclamation: | Информация о сервере",
      description=(
        f"Имя сервера: `{server_name}`\n"
        f"Владелец: <@{server_owner.id}>\n\n"
        f"Участники: `{server_members_count}`\n"
        f"Боты: `{server_bots_count}`\n\n"
        f"Роли: `{server_roles_count}` (+@everyone)\n"
        f"Категории: `{server_categories_count}`\n"
        f"Текстовые каналы: `{server_text_channels_count}`\n"
        f"Голосовые каналы: `{server_voice_channels_count}`\n"
      )
    )

    if inter.guild.icon:
        server_info_embed.set_thumbnail(url=inter.guild.icon.url)

    await inter.response.send_message(embed=server_info_embed, ephemeral=True)

def setup(client):
  client.add_cog(Server(client))