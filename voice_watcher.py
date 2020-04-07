from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os

import discord
import json

def mark_connected(members):
    with open("statistics.json", "r+") as f:
        data = json.load(f)
        for member in members:
            if str(member) not in data["members"]:
                data["members"][str(member)] = {}
                data["members"][str(member)]["connected"] = 0
                data["members"][str(member)]["total"] = 0
            data["members"][str(member)]["connected"] += 1
        f.seek(0)
        json.dump(data, f)
        f.truncate()

def step_time():
    with open("statistics.json", "r+") as f:
        data = json.load(f)
        for member in data["members"]:
            data["members"][member]["total"] += 1
        f.seek(0)
        json.dump(data, f)
        f.truncate()

class MyClient(discord.Client):
    async def on_ready(self):
        print("logged on as {}".format(self.user))
        def update_members():
            voice_members = []
            for member in self.get_all_members():
                if member.voice and member.voice.channel:
                    voice_members.append(member)
            mark_connected(voice_members)
            step_time()

        scheduler = AsyncIOScheduler()
        scheduler.add_job(update_members, "cron", minute="*")
        scheduler.start()

if __name__ == "__main__":
    if not os.path.exists("statistics.json"):
        print("creating empty statistics.json")
        with open("statistics.json", "w") as f:
            json.dump({"members": {}}, f)

    client = MyClient()
    client.run(os.environ["DISCORD_TOKEN"])

    try:
        asyncio.get_event_loop().run_forever()
    except(KeyboardInterrupt, SystemExit):
        pass