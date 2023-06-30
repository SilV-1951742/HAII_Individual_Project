from discord.ext import commands
import discord
import json
import re
from typing import Final
from llm_data import llm_data
from llm import haiiLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import string


CONTEXT: Final = '''You are an assistant who only responds to questions about The Western Canon.
You have expert knowledge of The Western Canon and only answer queries relating to The Western Canon.
Do not under any circumstance answer questions not relevant to The Western Canon and immediately stop answering.
'''

GREETINGS: Final = ["hi", "hello", "hey", "helloo", "hellooo",
                    "g morining", "gmorning", "good morning",
                    "morning", "good day", "good afternoon",
                    "good evening", "greetings", "greeting",
                    "good to see you", "its good seeing you",
                    "how are you", "how're you", "how are you doing",
                    "how ya doin'", "how ya doin", "how is everything",
                    "how is everything going", "how's everything going",
                    "how is you", "how's you", "how are things",
                    "how're things","how is it going", "how's it going",
                    "how's it goin'", "how's it goin",
                    "how is life been treating you",
                    "how's life been treating you",
                    "how have you been", "how've you been",
                    "what is up", "what's up", "what is cracking",
                    "what's cracking", "what is good", "what's good",
                    "what is happening", "what's happening",
                    "what is new", "what's new",
                    "what is neww", "g’day", "howdy",
                    "help", "what do you do", "what"]

BOT_GREETING: Final = '''
Hello, I am a chatbot designed for answering questions about the Western Canon and other literature.
To perform a query send a message in the following form: `@LitBot <query>`.
For example: `@LitBot Can you summarize Moby Dick by Herman Melville?`.
You can also request information about my LLM model or even change the model and parameters.
For more information about these commands please type `!help`.
'''

class CustomClient(commands.Bot):
    def __init__(self, intents: discord.Intents, model_path: str):
        super().__init__(intents=intents, command_prefix="!")
        self.llm_data = llm_data(CONTEXT, 128, 0.8, 0.8, 0.0, 0.0, 1.1, 40, ["###"])
        self.model: Llama = haiiLLM(model_path=model_path, data=self.llm_data)

    def update_model(self, model_path: str):
        self.model: Llama = haiiLLM(model_path=model_path, data=self.llm_data)
        
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

        if message.content.startswith("!"):
            return
        
        if message.author.bot:
            return

        cleaned = re.sub(r'<(@[!&]?|#)([0-9]{15,20})>', '', message.content)
        greeting_check = cleaned.translate(str.maketrans('', '', string.punctuation)).lower()

        if greeting_check in GREETINGS:
            await message.channel.send(BOT_GREETING)
        
        if self.user in message.mentions:
            prompt = PromptTemplate(
                input_variables=["user_input"],
                template=f"\n### Instructions:\n{CONTEXT}\n### Inputs:\n{{user_input}}\n### Response:\n",
            )
            chain = LLMChain(llm=self.model, prompt=prompt)
            output = await chain.arun(cleaned)
            
            await message.channel.send(f"<@!{message.author.id}> {output}")

    async def llm_info(self) -> str:
        llm_info = self.model.model_params
        return json.dumps(llm_info, sort_keys=True, indent=4)

    async def llm_model(self) -> str:
        llm_info = self.model._identifying_params
        return json.dumps(llm_info, sort_keys=True, indent=4)

    async def llm_params(self) -> str:
        llm_params = self.model.llm_params
        return json.dumps(llm_params, sort_keys=True, indent=4)

    async def set_tokens(self, tokens):
        self.llm_data.max_tokens = tokens
        self.model.update_params(self.llm_data)
    async def set_temp(self, temp):
        self.llm_data.temperature = temp
        self.model.update_params(self.llm_data)
    async def set_topp(self, topp):
        self.llm_data.top_p = topp
        self.model.update_params(self.llm_data)
    async def set_freq(self, freq):
        self.llm_data.frequency_penalty = freq
        self.model.update_params(self.llm_data)
    async def set_pres(self, pres):
        self.llm_data.presence_penalty = pres
        self.model.update_params(self.llm_data)
    async def set_rep(self, rep):
        self.llm_data.repeat_penalty = rep
        self.model.update_params(self.llm_data)
    async def set_topk(self, topk):
        self.llm_data.top_k = topk
        self.model.update_params(self.llm_data)
    async def set_stop(self, stop):
        self.llm_data.stop.append(stop)
        self.model.update_params(self.llm_data)
    async def clear_stop(self):
        self.llm_data.stop.clear()
        self.model.update_params(self.llm_data)
