# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class OnButtonClick(commands.Cog):
  def __init__(self, client):
    self.client = client

    self.green_boat_emoji  = 1490673747504533694
    self.yellow_boat_emoji = 1490673746347032658
    self.red_boat_emoji    = 1490673742786072648
    self.blue_boat_emoji   = 1490673739224977469

    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.Cog.listener()
  async def on_button_click(self, inter: disnake.MessageInteraction):

    def check_cmd_load(cmd_category, cmd_name):
      return self.data["client_modules"]["commands"][cmd_category][cmd_name]["load_module"]

    def check_cmd_status(cmd_category, cmd_name):
      return self.data["client_modules"]["commands"][cmd_category][cmd_name]["status"]

    def get_cmd_status_emoji(cmd_category, cmd_name):
      cmd_module_load = check_cmd_load(cmd_category, cmd_name)
      cmd_module_status = check_cmd_status(cmd_category, cmd_name)

      if cmd_module_load and cmd_module_status == "done":
        return f"<:greenboat:{self.green_boat_emoji}>"
      elif cmd_module_status == "in_dev":
        return f"<:yellowboat:{self.yellow_boat_emoji}>"
      elif cmd_module_status == "coming_soon":
        return f"<:blueboat:{self.blue_boat_emoji}>"
      else:
        return f"<:redboat:{self.red_boat_emoji}>"

    help_boats_description_embed = disnake.Embed(
      description=(
        f"<:greenboat:{self.green_boat_emoji}> - command is enabled\n"
        f"<:yellowboat:{self.yellow_boat_emoji}> - command in development\n"
        f"<:redboat:{self.red_boat_emoji}> - command is disabled\n\n"       
      )
    )

    if inter.component.custom_id == "help_info":
      help_emj = get_cmd_status_emoji("info", "help")
      server_emj = get_cmd_status_emoji("info", "server")
      user_emj = get_cmd_status_emoji("info", "user")
      host_emj = get_cmd_status_emoji("info", "host")

      help_info_embed = disnake.Embed(
        title="Information",
        description=(
          f"{help_emj} `/help` - shows information about bot commands\n"
          f"{server_emj} `/server` - shows information about current server\n"
          f"{user_emj} `/user` - shows information about user\n"
          f"{host_emj} `/host` - shows information about host\n"
        )
      )

      await inter.response.send_message(embeds=[help_boats_description_embed,
                                                help_info_embed], ephemeral=True)

    elif inter.component.custom_id == "moderation_info":
      clear_emj = get_cmd_status_emoji("moderation", "clear")
      ban_emj = get_cmd_status_emoji("moderation", "ban")
      kick_emj = get_cmd_status_emoji("moderation", "kick")

      help_moderation_embed = disnake.Embed(
        title="Moderation",
        description=(
          f"{clear_emj} `/clear` - clears many messages at once\n"
          f"{ban_emj} `/ban` - ran user in server\n"
          f"{kick_emj} `/kick` - kick user from server"
        )
      )

      await inter.response.send_message(embeds=[help_boats_description_embed,
                                                help_moderation_embed], ephemeral=True)


def setup(client):
  client.add_cog(OnButtonClick(client))