import discord
from discord.ext import commands

def read_config(file_path):
    config = {}
    with open("config.txt", 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config


# Lire le fichier de configuration
config = read_config("config.txt")

# Récupérer le token et le channel ID depuis le fichier de configuration
TOKEN = config['TOKEN']
CHANNEL_ID = int(config['CHANNEL_ID'])
# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionnaire pour suivre les messages consécutifs
user_message_count = {}


compteur = 160



@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
 
    messages = [msg async for msg in channel.history(limit=2)]
    if messages:
        dernier_message = messages[0]
        global compteur
        try:
            compteur = int(dernier_message.content) + 1
        except ValueError:
            print("Le dernier message n'est pas un nombre")
    




@bot.event
async def on_message(message):
    global compteur
    
    channel = bot.get_channel(CHANNEL_ID)
 
    messages = [msg async for msg in channel.history(limit=2)]
    dernier_message = messages[0]  
    avant_dernier_message = messages[1]  

    if not message.content.isdigit():#delete if the message is an str
        await message.delete()
        print(f"Message supprimé: '{message.content}' (ne contient pas uniquement des nombres)")
        return
    
    if int(message.content) == compteur:
        compteur += 1
        print(f"Le compteur est a {compteur}")
    
    else:
        await message.delete()
        
        print("dernier_message supprimer car int(message.content) !== compteur")

    if dernier_message.author == avant_dernier_message.author:
        if message.content.isdigit():
            await dernier_message.delete()
            print("le derniers message a été supprimer car dernier_message.author == avant_dernier_message.author")
            compteur -= 1
              

# Remplace 'YOUR_BOT_TOKEN' par le token de ton bot
bot.run(TOKEN)
