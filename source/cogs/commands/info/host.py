# Info:
#   Created at: 04.06.2026
#   Author: cjoye

import disnake
import subprocess
import os
from disnake.ext import commands

class Host(commands.Cog):
  def __init__(self, client):
      self.client = client

  @commands.slash_command(description="Shows information about host")
  async def host(self, inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer(ephemeral=True)
    date = subprocess.check_output(["date", "+%Y-%m-%d %H:%M"]).decode().strip()
    uptime = f"{os.environ.get("UPTIME_DAYS")}d {os.environ.get("UPTIME_HOURS")}h {os.environ.get("UPTIME_MINUTES")}m"

    host_info_embed = disnake.Embed(
      title=f":grey_exclamation: | Host info",
      description=(
        f"Host system date: `{date}`\n"
        f"Bot uptime: `{uptime}`"
      )
    )

    await inter.edit_original_message(embed=host_info_embed)

def setup(client):
  client.add_cog(Host(client))