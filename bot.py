import os
from doctest import FAIL_FAST
from email import message
from glob import glob
from pickle import FALSE, TRUE
import requests
import discord

bot = discord.Client()
gameStarted = FALSE
msg = ""
answer = ""
currentScore = 0
currentQuestion = 1
TOKEN = os.environ.get('BOT_TOKEN')


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"{guild.id} (name : {guild.name})")
        guild_count += 1
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
    global gameStarted
    global msg
    global currentScore
    global currentQuestion
    if gameStarted == TRUE:
        if message.content == "True" or message.content == "False" or message.content == "true" or message.content == "false":
            if answer == message.content:
                await message.channel.send("correct answer!")
                currentScore += 1
                await message.channel.send(f"current score: {currentScore}")
            else:
                await message.channel.send("wrong answer!")
                await message.channel.send(f"current score: {currentScore}")
            await loadQuestion("http://127.0.0.1:5000/load_questions", message.channel)
        # hit api
    if message.content == "-play":
        await message.channel.send("RULES: A question will be popped and you have to answer True/False. use -stop to stop quiz. Final" +
                                   "score will be displayed! Enjoy the quiz!!")
        gameStarted = TRUE
        msg = message.channel
        await loadQuestion("http://127.0.0.1:5000/load_questions", message.channel)
    elif message.content == "-stop":
        gameStarted = FALSE
        currentQuestion = 1
        await message.channel.send(f"final score is: {currentScore}")
        currentScore = 0


async def loadQuestion(api, msgSender):
    global answer
    global currentScore
    global currentQuestion
    response = requests.get(f"{api}")
    if response.status_code == 200:
        print("successfully fetched the data")
        responseInJson = response.json()
        question = responseInJson['question']
        answer = responseInJson['answer']
        await msgSender.send(f"{currentQuestion}) {question}")
        print(f"{currentQuestion}) {question}")
        currentQuestion += 1
    else:
        print(f"{response.status_code}")

bot.run(TOKEN)
