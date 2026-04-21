# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class Ban(commands.Cog):
  def __init__(self, client):
    self.client = client
    
    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.slash_command(
    description="Забанить юзера на сервере",
    default_member_permissions=disnake.Permissions(ban_members=True)
  )
  async def ban(
    self, inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member = commands.Param(
      description="Ваша жертва",
    ),
    clean_history_duration: int = commands.Param(
      description="Удалить сообщения за промежуток времени | Опционально: 0",
      default=0
    ),
    reason: str = commands.Param(
      description="Причина бана | Опционально: None",
      default=None
    ),
  ):
    if inter.guild is None:
      await inter.response.send_message("Это серверная команда!", ephemeral=True)
      return

    if user.id == self.client.user.id:
      await inter.response.send_message("Вы не можете забанить меня мной же!", ephemeral=True)
      return

    if user.id == inter.author.id:
      await inter.response.send_message("Вы не можете забанить себя!", ephemeral=True)
      return

    if user.top_role >= inter.guild.me.top_role:
      await inter.response.send_message(f"Я не могу забанить <@{user.id}> из-за положения в иерархии.", ephemeral=True)
      return

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])
    user_id = user.id
    ban_reason = f"Причина: `{reason}`" if reason else "Причина: `None`"
    
    if log_channel:
      log_embed = disnake.Embed(
        title="Юзер забанен",
        description=f"Пользователь <@{user.id}> (`{user.id}`) был забанен.\n{ban_reason}"
      )
      
      log_embed.set_footer(
        text=f"Пользователь — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )
      
      await log_channel.send(embed=log_embed)

    await user.ban(reason=reason, clean_history_duration=clean_history_duration)

    await inter.response.send_message(
      f"Пользователь <@{user_id}> (`{user_id}`) был забанен\n{ban_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Ban(client))