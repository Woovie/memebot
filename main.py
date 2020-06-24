import configparser, discord, glob, random, pymongo, uuid

config = configparser.ConfigParser()
config.read('config.ini')

mong_client = pymongo.MongoClient()

db = mong_client['memebot']

collection = db['memecount']

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_message(self, message):
        if message.content == config['discord']['cmd']:
            meme = Meme()
            meme.select()
            if meme.meme:
                loaded_meme = discord.File(meme.meme)
                meme_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, meme.meme))
                query = {"uuid": meme_uuid}
                result_count = collection.count_documents(query)
                if result_count == 0:
                    insertable = {"uuid": meme_uuid, "count": 1}
                    collection.insert(insertable)
                elif result_count == 1:
                    results = collection.find(query)
                    for result in results:
                        insertable = result
                    new_value = { "$set": { "count": insertable["count"] + 1}}
                    collection.update_one(query, new_value)
                else:
                    print("oh shit oh shit oh shit")
                await message.channel.send(file=loaded_meme)
            else:
                await message.channel.send("Failed to load any memes! Check logs.")

class Meme():
    def __init__(self):
        self.meme_folder = config['memes']['folder']
        self.meme_list = glob.glob(f"{self.meme_folder}/*")
        self.meme = None
    
    def select(self):
        if len(self.meme_list) > 0:
            self.meme = self.meme_list[random.randint(1, len(self.meme_list))-1]
        

client = DiscordClient()

client.run(config['discord']['token'])