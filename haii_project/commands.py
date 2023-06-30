from discord.ext import commands
import discord
import json
import os


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(
        help="Shows the ping/latency of the bot in miliseconds.",
        brief="Shows ping."
    )
    async def ping(self, ctx):
        if round(self.client.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(self.client.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(self.client.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pingpingpingpingping! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0x990000)
        await ctx.send(embed=embed)

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Shows the input parameters of the LLM.",
        brief="Shows input params."
    )
    async def parameters(self, ctx):
        ret_str = await self.client.llm_params()
        await ctx.send(f"```\n{ret_str}\n```")


class Model(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Shows the model parameters of the LLM.",
        brief="Shows model info."
    )
    async def model_info(self, ctx):
        ret_str = await self.client.llm_info()
        await ctx.send(f"```\n{ret_str}\n```")

    @commands.command(
        help="Shows the model of the LLM.",
        brief="Shows model."
    )
    async def current_model(self, ctx):
        ret_str = await self.client.llm_model()
        await ctx.send(f"```\n{ret_str}\n```")

    @commands.command(
        help="Show a list of available models.",
        brief="Show models.")
    async def list_models(self, ctx): # "arg" will have the first argument the user sent when he used the command "candidate"
        entries = os.listdir('../models')
        entries = "\n".join(entries)
        response = f"Available models:\n```\n{entries}```"
        await ctx.send(response)

    @commands.command(
        help="Pick a model to use.",
        brief="Update mode.")
    async def update_model(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        base_path = os.path.basename(arg)
        model_path = f"../models/{base_path}"
        if not os.path.isfile(model_path):
            ctx.send(f"`{base_path}` is not a valid model!")
            return

        self.client.update_model(model_path)
        
        await ctx.send(f"Updated to model `{base_path}`")


class Parameterize(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Set the max tokens of the LLM.",
        brief="Set max tokens.")
    async def max_tokens(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        tokens = 0
        try:
            tokens = int(arg)
        except:
            await ctx.send("Invalid **max_token** value")
            return

        await self.client.set_tokens(tokens)
        response = f"Set **max_tokens** to **{tokens}**"
        await ctx.send(response)

    @commands.command(
        help="Set the temperature of the LLM.",
        brief="Set temperature.")
    async def temperature(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = float(arg)
        except:
            await ctx.send("Invalid **temperature** value")
            return

        await self.client.set_temp(temp)
        response = f"Set **temperature** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Set the top_k of the LLM.",
        brief="Set top_k.")
    async def top_k(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = int(arg)
        except:
            await ctx.send("Invalid **top_k** value")
            return

        await self.client.set_topk(temp)
        response = f"Set **top_k** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Set the top_p of the LLM.",
        brief="Set top_p.")
    async def top_p(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = float(arg)
        except:
            await ctx.send("Invalid **top_p** value")
            return

        await self.client.set_topp(temp)
        response = f"Set **top_p** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Set the frequency penalty of the LLM.",
        brief="Set frequency penalty.")
    async def frequency_penalty(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = float(arg)
        except:
            await ctx.send("Invalid **frequency penalty** value")
            return

        await self.client.set_freq(temp)
        response = f"Set **frequency penalty** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Set the presence penalty of the LLM.",
        brief="Set presence penalty.")
    async def presence_penalty(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = float(arg)
        except:
            await ctx.send("Invalid **presence penalty** value")
            return

        await self.client.set_pres(temp)
        response = f"Set **presence penalty** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Set the repeat penalty of the LLM.",
        brief="Set repeat penalty.")
    async def repeat_penalty(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = float(arg)
        except:
            await ctx.send("Invalid **repeat penalty** value")
            return

        await self.client.set_rep(temp)
        response = f"Set **repeat penalty** to **{temp}**"
        await ctx.send(response)

    @commands.command(
        help="Append to the stop list of the LLM.",
        brief="Append to stop list.")
    async def append_stop(self, ctx, arg): # "arg" will have the first argument the user sent when he used the command "candidate"
        temp = 0
        try:
            temp = str(arg)
        except:
            await ctx.send("Invalid **stop** value")
            return

        await self.client.set_stop(temp)
        response = f"Appended **{temp}** to **stop**"
        await ctx.send(response)

    @commands.command(
        help="Clear the stop list of the LLM.",
        brief="Clear stop list.")
    async def clear_stop(self, ctx): # "arg" will have the first argument the user sent when he used the command "candidate"
        await self.client.clear_stop()
        response = "Cleared the **stop** list"
        await ctx.send(response)

    @commands.command(
        help="Explain each adjustable parameter for the LLM.",
        brief="Explain parameters."
    )
    async def explain_parameters(self, ctx):
        response = '''
# List of adjustable parameters
- **Max_tokens**: The maximum number of tokens to generate in the completion. -1 returns as many tokens as possible given the prompt and the models maximal context size.
- **Temperature**: What sampling temperature to use. Temperature is a hyperparameter that controls the randomness of the sampling process. The higher the sampling temperature, the more random.
- **Top_p**: Total probability mass of tokens to consider at each step. It is a parameter used to control the range of tokens considered by the AI model based on their cumulative probability. 1.0 means "use all tokens in the vocabulary" while 0.5 means "use only the 50% most common tokens".
- **Top_k**: The number of highest probability vocabulary tokens to keep for top-k-filtering. The number of top elements to look at for computing precision and name is name of display.
- **Repeat_penalty**: The penalty to apply to repeated tokens.
- **Presence_penalty**: Penalizes repeated tokens.
- **Frequency_penalty**: Penalizes repeated tokens according to frequency.
- **Stop**: A list of strings to stop generation when encountered.
        '''
        await ctx.send(response)


class CHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description="Help command for HAII Literature Bot\n")
        e.description += "Normal usage: simple type a query mentioning the bot to get a response.\nExample: `@LitBot Summarize Moby Dick`\n\n"
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
