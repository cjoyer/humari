# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Clear(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(
    default_member_permissions=disnake.Permissions(manage_messages=True),
    description="Delete many messages at once"
  )
  async def clear(
    self,
    inter,
    amount: int = commands.Param(
      description="Number of messages to delete"
    ),
    by: disnake.Member = commands.Param(
      description="Delete messages writen by member | Default: None",
      default=None
    )
  ):
    limit = 1024

    if amount > limit:
      await inter.response.send_message(
        f"Limit of messages to delete: `{limit}`", ephemeral=True
      )
      return

    await inter.response.defer(ephemeral=True)

    if by is None:
      deleted = await inter.channel.purge(limit=amount)
    else:
      deleted = await inter.channel.purge(limit=amount, check=lambda m: m.author == by)

    await inter.edit_original_response(
      content=f"`{len(deleted)}` messages have been deleted"
    )

def setup(client):
  client.add_cog(Clear(client))