# Samir Kothari

# Import discord.py
import discord
from discord.ext import commands
from discord import Message
import logging # setup to record errors that are encountered // https://docs.python.org/3/library/logging.html#module-logging
import re
import random

# import Google modules
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Thank you Lucas (https://www.youtube.com/channel/UCR-zOCvDCayyYy1flR5qaAg) for the great tutorials online!
 
TOKEN = open("token.txt","r").readline() # REPLACE TOKEN NAME
client = commands.Bot(command_prefix = '.')
#answers with the ms latency

# SET UP GSHEETS DESTINATION
scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
client1 = gspread.authorize(creds)

sheet =client1.open("SPREADSHEET TITLE").sheet1

def next_available_row(sheet=sheet, cols_to_sample=2):
  # looks for empty row based on values appearing in 1st N columns
  cols = sheet.range(1, 1, sheet.row_count, cols_to_sample)
  return max([cell.row for cell in cols if cell.value]) + 1

@client.event
async def on_ready():
      print("Ready!")

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 500)}ms ')

#If there is an error, it will answer with an error
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try .help ({error})')

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel
    if content.startswith('ns'): # STAND IN FOR 'NEW SOURCE' 
        
        # separate into items to be placed into google sheets
        content = re.sub('^ns ', '', content) # REMOVES NS AND THE SPACE THAT COMES AFTER IT
        content = content.split(', ') # SPLIT INTO LIST BY COMMA AND A SPACE
        
        sheet.insert_row(content, next_available_row()) # INSERT THE CONTENT INTO THE NEXT AVAILABLE ROW

        await channel.send(f"{author} added '{content[0]}' to 'SPREADSHEET NAME'") # CONFIRM THAT THE PROCESS HAS BEEN COMPLETED
    


logging.basicConfig(level=logging.INFO)
client.run(TOKEN)
