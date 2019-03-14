import discord
import asyncio
import requests
import json
import tweepy
import re
import os
import urllib.request
from discord.ext import commands
from discord.ext.commands import Bot
client = discord.Client()

bot = commands.Bot(command_prefix='.')
CONSUMER_KEY ="x"
CONSUMER_SECRET = "x"   
ACCESS_KEY = "x"    
ACCESS_SECRET = "x"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

global api
api = tweepy.API(auth)

@bot.event
async def on_ready():
    print ("online")


@bot.event
async def on_message(message):
    global api
    if str(message.channel.name) == "success": #Set channel name it is viewing
        try:
            author = str(message.author)
            author = re.split(r'\b#\b', author, maxsplit=1)[0].strip() #Gets user's name without their tag
            image_url = message.attachments[0]['url']
            tweet_text = ('Success by '+author) #Adjust how tweet looks
            tweet_image = image_url
            
            filename = 'temp.jpg' #Note: a file with this name will be saved in the file location alongside bot.
            request = requests.get(tweet_image, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                        
                upload_tweet = api.update_with_media(filename, status=tweet_text) #Posts Tweet
                tweet_id = str(upload_tweet.id)
                

                embed=discord.Embed(title="Tweet Posted! React below to undo tweet.")
                embed.set_footer(text="Created by @thecopbuddy") #on the 99.9% chance you will change this remember to credit via twitter <3
                sent_msg =  await bot.send_message(message.channel, embed=embed)
                await bot.add_reaction(sent_msg, emoji="\U0001F5D1")
                await asyncio.sleep(0.1) #Stops wait_for_reaction being triggered by the bot giving itself a reaction

                tweet_owner = (message.author)
                
                owner_delete = False
                while not owner_delete:
                    react_delete = await bot.wait_for_reaction(message=sent_msg)

                    gather_reactions = discord.utils.get(bot.messages, id=sent_msg.id)
                    for member in gather_reactions.reactions:
                        reactors = await bot.get_reaction_users(member)

                    if react_delete.reaction.emoji=="\U0001F5D1" and tweet_owner in reactors: #Only starts delete if correct emoji used and owner of image reacts
                        owner_delete = True
                        try:
                            api.destroy_status(tweet_id) #Deletes Tweet
                            await bot.delete_message(message) #Deletes image sent by user
                            await bot.clear_reactions(sent_msg)
                            edit_embed=discord.Embed(title="Tweet was deleted! Make sure to check images before posting.",color=0x80ff00)
                            edit_embed.set_footer(text="Created by @thecopbuddy")
                            await bot.edit_message(sent_msg, embed=edit_embed)
                        except:
                            print('Error deleting tweet/telling user')
                        
                print('Owner of image deleted tweet')
                
            else:
                print("Unable to download/upload image")


            
        except IndexError:
           pass

bot.run("INSERT DISCORD BOT TOKEN HERE")
