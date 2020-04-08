from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os

import discord
import json

def mark_connected(members):
    """Mark members as connected this minute."""

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

class VoiceWatcherClient(discord.Client):
    def read_config(self):
        """Open and read config.json."""

        with open("config.json", "r+") as f:
            config = json.load(f)

            if "token" not in config:
                config["token"] = input("Bot token: ")
            if "id" not in config:
                config["id"] = {}
            if "toggler" not in config["id"]:
                config["id"]["toggler"] = input("ID of toggler-bot: ")
            if "skolk_threshold" not in config:
                config["skolk_threshold"] = float(input("Threshold [0.0 - 1.0]: "))

            self.token = config["token"]
            self.toggler_id = config["id"]["toggler"]
            self.skolk_threshold = config["skolk_threshold"]

            f.seek(0)
            json.dump(config, f)
            f.truncate()

    def step_time(self):
        """Progress time and check thresholds."""

        with open("statistics.json", "r+") as f:
            data = json.load(f)
            for member_id in data["members"]:
                member = data["members"][member_id]
                member["total"] += 1
                if member["connected"] / member["total"] < self.threshold:
                    print("{} ({}/{}, {.2f})is below the skolk threshold!".format(
                        member_id,
                        member["connected"],
                        member["total"],
                        member["connected"] / member["total"]))
                    #TODO(gu) send message
            f.seek(0)
            json.dump(data, f)
            f.truncate()

    async def on_ready(self):
        print("logged on as {}".format(self.user))

        def update_members():
            """Update state"""

            voice_members = []
            for member in self.get_all_members():
                if member.voice and member.voice.channel:
                    voice_members.append(member)
            mark_connected(voice_members)
            self.step_time()

        scheduler = AsyncIOScheduler()
        scheduler.add_job(update_members, "cron", minute="*")
        scheduler.start()

if __name__ == "__main__":
    client = VoiceWatcherClient()

    if not os.path.exists("statistics.json"):
        print("creating empty statistics.json")
        with open("statistics.json", "w") as f:
            json.dump({"members": {}}, f)
    else:
        print("found already existing statistics.json")
    
    if not os.path.exists("config.json"):
        print("creating empty config.json")
        with open("config.json", "w") as f:
            json.dump({}, f)
    else:
        print("found already existing config.json")
    client.read_config()
    print("config read")

    client.run(client.token)

    try:
        asyncio.get_event_loop().run_forever()
    except(KeyboardInterrupt, SystemExit):
        pass
