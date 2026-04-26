# Info:
#   Created at: 04.06.2026
#   Author: cjoye

import disnake
from disnake.ext import commands

class User(commands.Cog):
  def __init__(self, client):
      self.client = client

  @commands.slash_command(description="Показывает информацию о юзере")
  async def user(
    self, inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member = commands.Param(
        description="Информация о выбраном юзере | Опционально: Interactor",
        default=lambda inter: inter.author
    )
  ):
    user_id = user.id
    user_name = user.name

    user_info_embed = disnake.Embed(
      title=f":grey_exclamation: | Информация о юзере",
      description=(
        f"Имя юзера: <@{user_id}>/`{user_name}`\n"
        f"ID юзера: `{user_id}`\n"
      )
    )

    if user.display_avatar:
      user_info_embed.set_thumbnail(url=user.display_avatar.url)

    await inter.response.send_message(embed=user_info_embed, ephemeral=True)

def setup(client):
  client.add_cog(User(client))