# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Ban(commands.Cog):
  def __init__(self, client):
      self.client = client

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
      description=f"The reason for banning | Default: None",
      default=None
    ),
  ):
    if inter.guild is None:
      await inter.response.send_message("It's server-only command!", ephemeral=True)
      retur

    user_id = user.id
    ban_reason = f"Reason: `{reason}`" if reason else "`None`"

    await user.ban(reason=reason, clean_history_duration=clean_history_duration)

    await inter.response.send_message(
      f"User <@{user_id}> (`{user_id}`) was banned by <@{inter.author.id}>\n{ban_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Ban(client))