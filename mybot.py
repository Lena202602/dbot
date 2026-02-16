from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def call_openai(question):
    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                 "role": "user",
                 "content": f"Respond like a Toni Robbins to the following question: {question}. Keep your response below 1500 characters and make it as impactful as possible. It's very important to have not more than 1500 characters in the response. If you have more to say, just say 'I have more to say, but I can't fit it all in one message.' and then stop. Do not write anything else after that. Do not write more than 1500 characters in your response!!",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("Let's change your life today, one question at a time")

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_openai(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
