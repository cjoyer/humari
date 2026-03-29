import disnake
from disnake.ext import commands

class Ready(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"✅ | Bot logged as {self.client.user}")

def setup(client):
  client.add_cog(Ready(client))