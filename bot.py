from pickle import TRUE, FALSE
import requests
import discord


bot = discord.Client()
gameStarted = FALSE
msg = ""
answer = ""
currentScore = 0
currentQuestion = 1

TOKEN = "OTk2NDQ5OTI5MDg0MDE0NjEy.GenFH3.anIjseHT05yOL4xw0vBfSNeMWYwM27Lvhs3LgQ"


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
    if gameStarted == TRUE:
        if message.content == "True" or message.content == "False" or message.content == "true" or message.content == "false":
            if answer == message.content:
                await message.channel.send("correct answer!")
                currentScore += 1
                await message.channel.send(f"current score: {currentScore}")
            else:
                await message.channel.send("wrong answer!")
                await message.channel.send(f"current score: {currentScore}")
            await loadQuestion("https://opentdb.com/api.php?amount=1&category=26&difficulty=easy&type=boolean", message.channel)
        # hit api
    if message.content == "-play":
        await message.channel.send("RULES: A question will be popped and you have to answer True/False. use -stop to stop quiz. Final" +
                                   "score will be displayed! Enjoy the quiz!!")
        gameStarted = TRUE
        msg = message.channel
        await loadQuestion("https://opentdb.com/api.php?amount=1&category=26&difficulty=easy&type=boolean", message.channel)
    elif message.content == "-stop":
        gameStarted = FALSE
        await message.channel.send(f"final score is: {currentScore}")


async def loadQuestion(api, msgSender):

    global answer
    global currentScore
    global currentQuestion
    response = requests.get(f"{api}")
    if response.status_code == 200:
        print("successfully fetched the data")
        responseInJson = response.json()
        question = responseInJson['results'][0]['question']
        answer = responseInJson['results'][0]['correct_answer']
        await msgSender.send(f"{currentQuestion}) {question}")
        print(f"{currentQuestion}) {question}")
        currentQuestion += 1
    else:
        print(f"ma ka bhosada {response.status_code}")


bot.run(TOKEN)
