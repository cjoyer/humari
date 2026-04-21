# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class Clear(commands.Cog):
  def __init__(self, client):
    self.client = client

    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.slash_command(
    default_member_permissions=disnake.Permissions(manage_messages=True),
    description="Удалить много сообщений за раз"
  )
  async def clear(
    self,
    inter: disnake.ApplicationCommandInteraction,
    amount: int = commands.Param(
      description="Кол-во сообщений для удаления"
    ),
    by: disnake.Member = commands.Param(
      description="Удалить сообщения юзера | Опционально: None",
      default=None
    )
  ):
    if inter.guild is None:
      await inter.response.send_message("Это серверная команда!", ephemeral=True)
      return

    if amount <= 0:
      await inter.response.send_message(
        "Минимальное кол-во сообщений для удаления: `0`.", ephemeral=True
      )
      return

    limit = 1024

    if amount > limit:
      await inter.response.send_message(
        f"Лимит сообщений для удаления: `{limit}`", ephemeral=True
      )
      return

    await inter.response.defer(ephemeral=True)

    if by is None:
      deleted = await inter.channel.purge(limit=amount)
    else:
      deleted = await inter.channel.purge(limit=amount, check=lambda m: m.author == by)

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])

    if log_channel:
      log_embed = disnake.Embed(
        title="Сообщения удалены",
        description=(
          f"`{len(deleted)}` сообщений было удалено в <#{inter.channel.id}>"
          + (f"\nФильтр: <@{by.id}> (`{by.id}`)" if by else "")
        )
      )

      log_embed.set_footer(
        text=f"Пользователь — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )

      await log_channel.send(embed=log_embed)

    await inter.edit_original_response(
      content=f"`{len(deleted)}` сообщений было удалено"
    )

def setup(client):
  client.add_cog(Clear(client))