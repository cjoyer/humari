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
    description="Ban user in server",
    default_member_permissions=disnake.Permissions(ban_members=True)
  )
  async def ban(
    self, inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member = commands.Param(
      description="The user to ban",
    ),
    clean_history_duration: int = commands.Param(
      description="Days of message history to delete | Default: 0",
      default=0
    ),
    reason: str = commands.Param(
      description="The reason for banning | Default: None",
      default=None
    ),
  ):
    if inter.guild is None:
      await inter.response.send_message("It's a server-only command!", ephemeral=True)
      return

    if user.id == self.client.user.id:
      await inter.response.send_message("You can't ban me by using my command!", ephemeral=True)
      return

    if user.id == inter.author.id:
      await inter.response.send_message("You can't ban yourself!", ephemeral=True)
      return

    if user.top_role >= inter.guild.me.top_role:
      await inter.response.send_message("I can't ban this user due to role hierarchy.", ephemeral=True)
      return

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])
    user_id = user.id
    ban_reason = f"Reason: `{reason}`" if reason else "Reason: `None`"
    
    if log_channel:
      log_embed = disnake.Embed(
        title="Member banned",
        description=f"Member <@{user.id}> (`{user.id}`) has been banned by <@{inter.author.id}>.\n{ban_reason}"
      )
      
      log_embed.set_footer(
        text=f"Interactor — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )
      
      await log_channel.send(embed=log_embed)

    await user.ban(reason=reason, clean_history_duration=clean_history_duration)

    await inter.response.send_message(
      f"User <@{user_id}> (`{user_id}`) was banned by <@{inter.author.id}>\n{ban_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Ban(client))