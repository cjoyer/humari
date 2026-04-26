# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class OnDropdown(commands.Cog):
  def __init__(self, client):
    self.client = client

    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

    emojis = self.data["client_modules"]["commands"]["info"]["help"]["emojis"]

    green_id  = emojis.get("green",  "0")
    yellow_id = emojis.get("yellow", "0")
    red_id    = emojis.get("red",    "0")
    blue_id   = emojis.get("blue",   "0")

    self.green_boat_emoji  = f"<:greenboat:{green_id}>"  if green_id  != "0" else "🟢"
    self.yellow_boat_emoji = f"<:yellowboat:{yellow_id}>" if yellow_id != "0" else "🟡"
    self.red_boat_emoji    = f"<:redboat:{red_id}>"      if red_id    != "0" else "🔴"
    self.blue_boat_emoji   = f"<:blueboat:{blue_id}>"    if blue_id   != "0" else "🔵"

  @commands.Cog.listener()
  async def on_dropdown(self, inter: disnake.MessageInteraction):
    def check_cmd_load(cmd_category, cmd_name):
      return self.data["client_modules"]["commands"][cmd_category][cmd_name]["load_module"]

    def check_cmd_status(cmd_category, cmd_name):
      return self.data["client_modules"]["commands"][cmd_category][cmd_name]["status"]

    def get_cmd_status_emoji(cmd_category, cmd_name):
      cmd_module_load = check_cmd_load(cmd_category, cmd_name)
      cmd_module_status = check_cmd_status(cmd_category, cmd_name)

      if cmd_module_load and cmd_module_status == "done":
        return f"{self.green_boat_emoji}"
      elif cmd_module_status == "in_dev":
        return f"{self.yellow_boat_emoji}"
      elif cmd_module_status == "coming_soon":
        return f"{self.blue_boat_emoji}"
      else:
        return f"{self.red_boat_emoji}"

    help_boats_description_embed = disnake.Embed(
      description=(
        f"{self.green_boat_emoji} - command is enabled\n"
        f"{self.yellow_boat_emoji} - command in development\n"
        f"{self.red_boat_emoji} - command is disabled\n\n"       
      )
    )
    
    if inter.component.custom_id == "help_category_select":
      if inter.values[0] == "help_info_select":
        help_emj = get_cmd_status_emoji("info", "help")
        server_emj = get_cmd_status_emoji("info", "server")
        user_emj = get_cmd_status_emoji("info", "user")
        botinfo_emj = get_cmd_status_emoji("info", "botinfo")

        help_info_embed = disnake.Embed(
          title="Information",
          description=(
            f"{help_emj} `/help` - shows information about bot commands\n"
            f"{server_emj} `/server` - shows information about current server\n"
            f"{user_emj} `/user` - shows information about user\n"
            f"{botinfo_emj} `/botinfo` - shows information about bot\n"
          )
        )

        await inter.response.send_message(embeds=[help_boats_description_embed,
                                                  help_info_embed], ephemeral=True)

      elif inter.values[0] == "help_moder_select":
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
  client.add_cog(OnDropdown(client))