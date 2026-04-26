# Info:
#   Created at: 04.07.2026
#   Author: cjoyer

import disnake
from disnake.ext import commands
import commentjson

class OnSlashCommandError(commands.Cog):
  def __init__(self, client):
    self.client = client
      
    with open("config/modules.jsonc", "r") as f:
      self.data = commentjson.load(f)

  @commands.Cog.listener()
  async def on_slash_command_error(
    self, inter: disnake.ApplicationCommandInteraction,
    error: Exception
  ):
    report_channel = self.client.get_channel(self.data["client_modules"]["events"]["on_slash_command_error"]["send_error_report"])
    options = ", ".join(f"{opt.name}: {opt.value}" for opt in inter.data.options)

    error_embed = disnake.Embed(
      title="❌ Обишка слэш-команды!",
      description=f"Ошибка при использовании команды:\n```sh\n{error}\n```"
    )
    
    report_embed = disnake.Embed(
      title="⚠️ Репорт о ошибке слэш-команды",
      description=f"/**{inter.data.name}** {options or '`none`'}\n```sh\n{error}\n```"
    )
    
    if (report_channel):
      error_embed.set_footer(
        text="Разработчик уведомлён"
      )
      
      report_embed.set_footer(
        text=f"Пользователь — {inter.author.name} ({inter.author.id})",
        icon_url=inter.author.avatar.url
      )
      
      await report_channel.send(embed=report_embed)

    if isinstance(error, commands.MissingPermissions):
      await inter.response.send_message("❌ Ошибка: `У вас нет прав для использования этой команды`", ephemeral=True)
    else:
      await inter.response.send_message(embed=error_embed, ephemeral=True)


def setup(client):
  client.add_cog(OnSlashCommandError(client))