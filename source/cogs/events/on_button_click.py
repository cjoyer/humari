# Info:
#   Created at: 04.06.2026
#   Author: cjoyer

import disnake
import commentjson
from disnake.ext import commands

class OnButtonClick(commands.Cog):
  def __init__(self, client):
    self.client = client
    
    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.Cog.listener()
  async def on_button_click(self, inter: disnake.MessageInteraction):
    green_boat_emoji  = 1490673747504533694
    yellow_boat_emoji = 1490673746347032658
    red_boat_emoji    = 1490673742786072648
    blue_boat_emoji   = 1490673739224977469

    if inter.component.custom_id == "help_info":
      help_load_module = self.data["client_modules"]["commands"]["info"]["help"]["load_module"]
      help_cmd_status  = self.data["client_modules"]["commands"]["info"]["help"]["status"]

      if help_load_module and help_cmd_status == "done":
        help_cmd_status_emj = f"<:greenboat:{green_boat_emoji}>"
      elif help_cmd_status == "in_dev":
        help_cmd_status_emj = f"<:yellowboat:{yellow_boat_emoji}>"
      elif help_cmd_status == "comming_soon":
        help_cmd_status_emj = f"<:blueboat:{blue_boat_emoji}>"
      else:
        help_cmd_status_emj = f"<:redboat:{red_boat_emoji}>"

      help_info_embed = disnake.Embed(
        title="Information",
        description=(
          f"<:greenboat:{green_boat_emoji}> - command is enabled\n"
          f"<:yellowboat:{yellow_boat_emoji}> - command in development\n"
          f"<:redboat:{red_boat_emoji}> - command is disabled\n\n"
          f"{help_cmd_status_emj} `help` - shows information about bot commands"
        )
      )
      
      await inter.response.send_message(embed=help_info_embed, ephemeral=True)
      
    elif inter.component.custom_id == "moderation_info":
      clear_load_module = self.data["client_modules"]["commands"]["moderation"]["clear"]["load_module"]
      clear_cmd_status  = self.data["client_modules"]["commands"]["moderation"]["clear"]["status"]

      if clear_load_module and clear_cmd_status == "done":
        clear_cmd_status_emj = f"<:greenboat:{green_boat_emoji}>"
      elif clear_cmd_status == "in_dev":
        clear_cmd_status_emj = f"<:yellowboat:{yellow_boat_emoji}>"
      elif clear_cmd_status == "comming_soon":
        clear_cmd_status_emj = f"<:blueboat:{blue_boat_emoji}>"
      else:
        clear_cmd_status_emj = f"<:redboat:{red_boat_emoji}>"
        
      moderation_info_embed = disnake.Embed(
        title="Moderation",
        description=(
          f"<:greenboat:{green_boat_emoji}> - command is enabled\n"
          f"<:yellowboat:{yellow_boat_emoji}> - command in development\n"
          f"<:redboat:{red_boat_emoji}> - command is disabled\n\n"
          f"{clear_cmd_status_emj} `clear` - clears many messages at once"
        )
      )
      
      await inter.response.send_message(embed=moderation_info_embed, ephemeral=True)

def setup(client):
  client.add_cog(OnButtonClick(client))