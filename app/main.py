from interactions import (
    Client,
    Intents,
    Modal,
    ModalContext,
    OptionType,
    ShortText,
    SlashContext,
    listen,
    modal_callback,
    slash_command,
    slash_option,
)

from app.adapter.league_of_legend.api_league import (
    get_account_informations,
    get_league_informations,
    get_summoner_informations,
)
from app.adapter.league_of_legend.schema import LeagueOutputItem, RiotAccountInput
from app.core.constants import BOT_TOKEN

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(
    name="get_lol_rank_2", description="Get the rank of a League of Legends player"
)
@slash_option(
    name="game_name",
    description="The game name of the player",
    required=True,
    opt_type=OptionType.STRING,
)
async def get_lol_rank(ctx: SlashContext, game_name: str, tag_line: str = "euw"):
    await ctx.defer()

    input = RiotAccountInput(game_name=game_name, tag_line=tag_line)

    account = get_account_informations(input)
    summoner = get_summoner_informations(account.puuid)
    league = get_league_informations(summoner.id)

    league_5x5: LeagueOutputItem = [
        item for item in league.league if item.queueType == "RANKED_SOLO_5x5"
    ][0]

    await ctx.send(
        f"{account.gameName}#{account.tagLine} is currently {league_5x5.tier} {league_5x5.rank} with {league_5x5.leaguePoints} LP"
    )


@slash_command(name="get_lol_modal", description="Ask for a League of Legends form")
async def get_lol_modal(ctx: SlashContext):
    my_modal = Modal(
        ShortText(label="Nom d'invocateur", custom_id="summoner_name"),
        title="League of Legends",
        custom_id="lol_modal",
    )
    await ctx.send_modal(modal=my_modal)


@modal_callback("lol_modal")
async def on_lol_modal_answer(ctx: ModalContext, summoner_name: str):
    await ctx.send(summoner_name)


bot.start(BOT_TOKEN)
