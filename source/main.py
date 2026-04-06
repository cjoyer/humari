# Info:
#   Created at: 03.29.2026
#   Author: cjoyer

def main():
  import disnake
  from disnake.ext import commands
  import os
  import commentjson
  import threading
  import time
    
  intents = disnake.Intents.default()
  intents.message_content = True
  intents.members = True
  
  with open("config/modules.jsonc", "r") as f:
    data = commentjson.load(f)
    
  client = commands.Bot(
    intents=intents,
    command_prefix='$'
  )
  
  def uptime_task():
    days = hours = minutes = 0
    os.environ["UPTIME_DAYS"] = str(days)
    os.environ["UPTIME_HOURS"] = str(hours)
    os.environ["UPTIME_MINUTES"] = str(minutes)

    while True:
      time.sleep(60)
      minutes += 1

      if minutes == 60:
        hours += 1
        minutes = 0

      if hours == 24:
        days += 1
        hours = 0

      os.environ["UPTIME_DAYS"] = str(days)
      os.environ["UPTIME_HOURS"] = str(hours)
      os.environ["UPTIME_MINUTES"] = str(minutes)

  t1 = threading.Thread(target=uptime_task, daemon=True)
  t1.start()
  
  server_modules_events = [
    "on_voice_state_update",
    "on_member_join"
  ]
  
  client_modules_events = [
    "on_ready"
  ]

  client_modules_commands_info = [
    "help",
    "server",
    "user",
    "host"
  ]

  client_modules_commands_moderation = [
    "clear",
    "ban",
    "kick"
  ]
  
  for module in server_modules_events:
    if data["server_modules"]["events"][module]["load_module"]:
      client.load_extension(f"source.cogs.events.{module}")
      print(f"✅ | Cog 'source.cogs.events.{module}' was loaded")
  
  for module in client_modules_events:
    if data["client_modules"]["events"][module]["load_module"]:
      client.load_extension(f"source.cogs.events.{module}")
      print(f"✅ | Cog 'source.cogs.events.{module}' was loaded")

  for module in client_modules_commands_info:
    if data["client_modules"]["commands"]["info"][module]["load_module"]:
      client.load_extension(f"source.cogs.commands.info.{module}")
      print(f"✅ | Cog 'source.cogs.commands.info.{module}' was loaded")

  for module in client_modules_commands_moderation:
    if data["client_modules"]["commands"]["moderation"][module]["load_module"]:
      client.load_extension(f"source.cogs.commands.moderation.{module}")
      print(f"✅ | Cog 'source.cogs.commands.moderation.{module}' was loaded")
      
  client.load_extension("source.cogs.events.on_button_click")
  print(f"✅ | Cog 'source.cogs.events.on_button_click' was loaded")

  client.run(os.environ.get("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
  main()