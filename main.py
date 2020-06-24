import configparser, discord, glob, random

config = configparser.ConfigParser()
config.read('config.ini')

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_message(self, message):
        if message.content == config['discord']['cmd']:
            meme = Meme()
            meme.select()
            loaded_meme = discord.File(meme.meme)
            await message.channel.send(file=loaded_meme)

class Meme():
    def __init__(self):
        self.meme_folder = config['memes']['folder']
        self.meme_list = glob.glob(self.meme_folder)
        self.meme = None
    
    def select(self):
        if len(self.meme_list) > 0:
            self.meme = self.meme_list[random.randint(1, len(self.meme_list))-1]
        else:
            print('aaaaa')
        

client = DiscordClient()

client.run(config['discord']['token'])