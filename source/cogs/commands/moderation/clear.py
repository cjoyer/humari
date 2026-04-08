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
    description="Delete many messages at once"
  )
  async def clear(
    self,
    inter: disnake.ApplicationCommandInteraction,
    amount: int = commands.Param(
      description="Number of messages to delete"
    ),
    by: disnake.Member = commands.Param(
      description="Delete messages written by member | Default: None",
      default=None
    )
  ):
    if inter.guild is None:
      await inter.response.send_message("It's a server-only command!", ephemeral=True)
      return

    if amount <= 0:
      await inter.response.send_message(
        "Amount of messages to delete must be greater than `0`.", ephemeral=True
      )
      return

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

    log_channel = self.client.get_channel(self.data["client_modules"]["commands"]["moderation"]["send_logs"])

    if log_channel:
      log_embed = disnake.Embed(
        title="Messages cleared",
        description=(
          f"`{len(deleted)}` messages have been deleted in <#{inter.channel.id}> "
          f"by <@{inter.author.id}>."
          + (f"\nFiltered by: <@{by.id}> (`{by.id}`)" if by else "")
        )
      )

      log_embed.set_footer(
        text=f"Interactor — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.display_avatar.url
      )

      await log_channel.send(embed=log_embed)

    await inter.edit_original_response(
      content=f"`{len(deleted)}` messages have been deleted"
    )

def setup(client):
  client.add_cog(Clear(client))