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
    description="Kicks user from server",
    default_member_permissions=disnake.Permissions(kick_members=True)
  )
  async def kick(
    self, inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member = commands.Param(
      description="The user to kick",
    ),
    reason: str = commands.Param(
      description="The reason for kicking | Default: None",
      default=None
    )
  ):
    if inter.guild is None:
      await inter.response.send_message("It's a server-only command!", ephemeral=True)
      return

    if user.id == self.client.user.id:
      await inter.response.send_message("You can't kick me by using my command!", ephemeral=True)
      return

    if user.id == inter.author.id:
      await inter.response.send_message("You can't kick yourself!", ephemeral=True)
      return

    if user.top_role >= inter.guild.me.top_role:
      await inter.response.send_message("I can't kick this user due to role hierarchy.", ephemeral=True)
      return

    user_id = user.id
    kick_reason = f"Reason: `{reason}`" if reason else "Reason: `None`"

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])

    if log_channel:
      log_embed = disnake.Embed(
        title="Member kicked",
        description=f"Member <@{user.id}> (`{user.id}`) has been kicked by <@{inter.author.id}>.\n{kick_reason}"
      )

      log_embed.set_footer(
        text=f"Interactor — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )

      await log_channel.send(embed=log_embed)

    await user.kick(reason=reason)

    await inter.response.send_message(
      f"User <@{user_id}> (`{user_id}`) was kicked by <@{inter.author.id}>\n{kick_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Kick(client))