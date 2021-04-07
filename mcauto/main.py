import discord
import os
import mcauto.mc as mc
import sys

def app():
    _DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not _DISCORD_TOKEN:
        print("DISCORD_TOKEN is not set")
        sys.exit(1)

    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        msg = message.content.strip()
        if msg == "!mcup":
            try:
                mc.start_server()
                await message.channel.send("Server is starting...")
            except mc.IllegalStateError:
                await message.channel.send("Server is already started.")
        elif msg == "!mcdown":
            try:
                mc.stop_server()
                await message.channel.send("Command: stop")
            except mc.IllegalStateError:
                await message.channel.send("Server is not started.")
        elif msg == "!mcsave":
            try:
                mc.send_command("save-all")
                await message.channel.send("Command: save-all")
            except mc.IllegalStateError:
                await message.channel.send("Server is not started.")
        elif msg == "!mcstatus":
            is_running = mc.is_server_running()
            if is_running:
                reply = "RUNNING"
            else:
                reply = "STOPPED"
            await message.channel.send(reply)

    client.run(_DISCORD_TOKEN)

if __name__ == "__main__":
    app()
