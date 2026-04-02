# Info:
#   Created at: 03.29.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands
import commentjson

class VoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.temp_channels: dict[int, int] = {}
        
        with open("config/modules.jsonc", "r") as f:
          self.data = commentjson.load(f)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState,
    ):
      CREATE_CHANNEL_ID = self.data["server_modules"]["events"]["on_voice_state_update"]["create_channel_id"]

      if after.channel and after.channel.id == CREATE_CHANNEL_ID:
          guild = member.guild
          category = after.channel.category

          overwrites = {
              member: disnake.PermissionOverwrite(
                  manage_channels=True,
                  move_members=True,
                  mute_members=True,
                  deafen_members=True,
              )
          }

          new_channel = await guild.create_voice_channel(
              name=f"୨🔊୧・{member.display_name}'s channel",
              category=category,
              overwrites=overwrites,
              reason=f"Temporary voice channel for {member.display_name}",
          )

          self.temp_channels[new_channel.id] = member.id
          await member.move_to(new_channel)

          if self.data["server_modules"]["events"]["on_voice_state_update"]["send_msg"]:
            await new_channel.send(f"Привет, <@{member.id}>!\nДобро пожаловать в твой приватный голосовой канал.\n**У тебя есть права, что бы управлять им**. Веселись! <:pepe_drinks_tea:1473281666582843402>")

      if before.channel and before.channel.id in self.temp_channels:
          channel = before.channel

          if len(channel.members) == 0:
              self.temp_channels.pop(channel.id)
              await channel.delete(reason="Temporary channel is empty")

def setup(client):
  client.add_cog(VoiceStateUpdate(client))