# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Kick(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(
    description="Kicks user from server",
    default_member_permissions=disnake.Permissions(ban_members=True))
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
      await inter.response.send_message("It's server-only command!", ephemeral=True)
      retur

    user_id = user.id
    kick_reason = f"Reason: `{reason}`" if reason else "`None`"

    await user.kick(reason=reason)

    await inter.response.send_message(
      f"User <@{user_id}> (`{user_id}`) was kicked by <@{inter.author.id}>\n{kick_reason}",
      ephemeral=True
    )

def setup(client):
  client.add_cog(Kick(client))