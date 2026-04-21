# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class Kick(commands.Cog):
  def __init__(self, client):
    self.client = client

    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.slash_command(
    description="Кикнуть юзера с сервера",
    default_member_permissions=disnake.Permissions(kick_members=True)
  )
  async def kick(
    self, inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member = commands.Param(
      description="Юзер",
    ),
    reason: str = commands.Param(
      description="Причина кика | Опционально: None",
      default=None
    )
  ):
    if inter.guild is None:
      await inter.response.send_message("Это серверная команда!", ephemeral=True)
      return

    if user.id == self.client.user.id:
      await inter.response.send_message("Вы не можете кикнуть меня мной же!", ephemeral=True)
      return

    if user.id == inter.author.id:
      await inter.response.send_message("Вы не можете кикнуть меня", ephemeral=True)
      return

    if user.top_role >= inter.guild.me.top_role:
      await inter.response.send_message("Я не могу кикнуть <@{user.id}> из-за положения в иерархии.", ephemeral=True)
      return

    user_id = user.id
    kick_reason = f"Причина: `{reason}`" if reason else "Причина: `None`"

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])

    if log_channel:
      log_embed = disnake.Embed(
        title="Юзер кикнут",
        description=f"Юзер <@{user.id}> (`{user.id}`) был кикнут.\n{kick_reason}"
      )

      log_embed.set_footer(
        text=f"Пользователь — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )

      await log_channel.send(embed=log_embed)

    await user.kick(reason=reason)

    await inter.response.send_message(
      f"Юзер <@{user_id}> (`{user_id}`) был забанен\n{kick_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Kick(client))