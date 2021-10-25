import os
import discord
import requests
import json
from PyDictionary import PyDictionary

client = discord.Client()

dictionary = PyDictionary()

seperator = '\n ~'

language_codes = {
  'en_US':	'English (US)',
  'hi':	'Hindi',
  'es':	'Spanish',
  'fr':	'French',
  'ja':	'Japanese',
  'ru':	'Russian',
  'en_GB':	'English (UK)',
  'de':	'German',
  'it':	'Italian',
  'ko':	'Korean',
  'pt-BR':	'Brazilian Portuguese',
  'ar':	'Arabic',
  'tr':	'Turkish'
}

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('-dictionary'):
    try:
      words = message.content.split(" ")[1:-1] if len(message.content.split(" ")) > 2 else message.content.split(" ")[1:]
      words = "%20".join(words)
      language = message.content.split(" ")[-1] if len(message.content.split(" ")) > 2 else 'en_GB'
      search = requests.get(r'https://api.dictionaryapi.dev/api/v2/entries/' + language + r'/' + words).json()
      definitions = [str(f'({x["partOfSpeech"]}): {x["definitions"][0]["definition"]}') for x in search[0]['meanings']]
      try:
        await message.reply(f"Word: {search[0]['word']}\nLanguage: {language_codes[language]}\nDefinition(s):\n ~{seperator.join(definitions)}")
          
      except discord.errors.HTTPException:
        await message.reply('Meaning not found or word does not exist.')
        
    except KeyError:
      await message.reply('Meaning/language not found or word/language does not exist.')

    except json.decoder.JSONDecodeError:
      await message.reply('Please type in a word.')
  elif message.content.startswith('-synonym'):
    if len(message.content.split(" ")) > 2:
      await message.reply('Please only use one word.')
      
    elif len(message.content.split(" ")) == 2:
      word = message.content.split(" ")[1]
      try:
        try:
          await message.reply(f"Word: {word}\nSynonym(s):\n ~{seperator.join(dictionary.synonym(word))}")
        
        except discord.errors.HTTPException:
          await message.reply('Synonym(s) not found or word does  not exist.')
      
      except TypeError:
        await message.reply('Synonym(s) not found or word does not exist.')
        

    else:
      await message.reply('Please type in a word.')

  elif message.content.startswith('-antonym'):
      if len(message.content.split(" ")) > 2:
        await message.reply('Please only use one word.')
        
      elif len(message.content.split(" ")) == 2:
        word = message.content.split(" ")[1]
        try:
          try:
            await message.reply(f"Word: {word}\nAntonym(s):\n ~{seperator.join(dictionary.antonym(word))}")
          
          except discord.errors.HTTPException:
            await message.reply('Antonym(s) not found or word does  not exist.')
        
        except TypeError:
          await message.reply('Antonym(s) not found or word does not exist.')
          

      else:
        await message.reply('Please type in a word.')

  elif message.content.startswith('-translate'):
    if len(message.content.split(" ")) > 3:
      await message.reply('Please only use two words: -the word -the language.')
        
    elif len(message.content.split(" ")) == 3:
      word = message.content.split(" ")[1]
      language = message.content.split(" ")[2]
      try:
        try:
          await message.reply(f"Word: {word}\nLanguage: {language}\nTranslation: {dictionary.translate(word,language)}")
          
        except discord.errors.HTTPException:
          await message.reply('Translation not found or word does not exist.')
        
      except TypeError:
        await message.reply('Translation not found or word does not exist.')
          
    else:
      await message.reply('Please type in a word/language.')


client.run(os.environ['TOKEN'])