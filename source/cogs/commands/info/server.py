# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands

class Server(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.slash_command(description="Shows information about server")
  async def server(self, inter: disnake.ApplicationCommandInteraction):
    if inter.guild is None:
      await inter.response.send_message("It's server-only command!", ephemeral=True)
      return

    server_name = inter.guild.name
    server_owner = inter.guild.owner
    server_members_count = sum(1 for member in inter.guild.members if not member.bot)
    server_bots_count = sum(1 for member in inter.guild.members if member.bot)
    server_roles_count = len(inter.guild.roles)
    server_categories_count = len(inter.guild.categories)
    server_text_channels_count = len(inter.guild.text_channels)
    server_voice_channels_count = len(inter.guild.voice_channels)

    server_info_embed = disnake.Embed(
      title=f":grey_exclamation: | Server info",
      description=(
        f"Server name: `{server_name}`\n"
        f"Server owner: <@{server_owner.id}>\n\n"
        f"Members count: `{server_members_count}`\n"
        f"Bots count: `{server_bots_count}`\n\n"
        f"Roles count: `{server_roles_count}` (+@everyone)\n"
        f"Categories count: `{server_categories_count}`\n"
        f"Text channels count: `{server_text_channels_count}`\n"
        f"Voice channels count: `{server_voice_channels_count}`\n"
      )
    )

    if inter.guild.icon:
        server_info_embed.set_thumbnail(url=inter.guild.icon.url)

    await inter.response.send_message(embed=server_info_embed, ephemeral=True)

def setup(client):
  client.add_cog(Server(client))