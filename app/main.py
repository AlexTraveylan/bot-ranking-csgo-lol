from datetime import datetime

from interactions import (
    BrandColors,
    Client,
    Embed,
    Intents,
    Modal,
    ModalContext,
    ShortText,
    SlashContext,
    listen,
    modal_callback,
    slash_command,
)

from app.adapter.league_of_legend.api_league import (
    get_account_informations,
    get_league_informations,
    get_summoner_informations,
)
from app.adapter.league_of_legend.schema import LeagueOutputItem, RiotAccountInput
from app.core.constants import BOT_TOKEN
from app.core.database.models import DiscordMember, RiotAccount, RiotScore, unit
from app.core.database.services.discord_member import DiscordMemberController
from app.core.database.services.riot_account import RiotAccountController
from app.core.database.services.riot_score import RiotScoreController

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(
    name="get_lol_rank", description="Get the rank of a League of Legends player"
)
async def get_lol_rank(ctx: SlashContext):
    await ctx.defer()

    with unit() as session:
        member: DiscordMember = DiscordMemberController.get_by_name(
            session=session,
            discord_real_name=str(ctx.author_id),
        )

        if member is None:
            raise ValueError("Member not found")

        account: RiotAccount = RiotAccountController.get_by_discord_member_id(
            session=session,
            discord_member_id=member.id,
        )

        if account is None:
            raise ValueError("Account not found")

        league = get_league_informations(account.summoner_id)

        league_5x5: LeagueOutputItem = [
            item for item in league.league if item.queueType == "RANKED_SOLO_5x5"
        ][0]

        riot_score = RiotScore(
            tier=league_5x5.tier,
            rank=league_5x5.rank,
            leaguePoints=league_5x5.leaguePoints,
            wins=league_5x5.wins,
            losses=league_5x5.losses,
            created_at=datetime.now(),
            riot_account_id=account.id,
        )

        riot_score_created = RiotScoreController.create(session, riot_score)

        embed = Embed(
            title="Score actuel",
            description=f"Voici le score actuel de {account}",
            color=BrandColors.GREEN,
        )
        embed.add_field(
            name="Score actuel",
            value=f"{riot_score_created}",
            inline=False,
        )

        await ctx.send(embeds=embed)


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
    await ctx.defer()

    member = DiscordMember(discord_real_name=str(ctx.author_id))

    with unit() as session:
        member_created = DiscordMemberController.create(session, member)
        riot_input = RiotAccountInput(game_name=summoner_name)

        lol_account_info = get_account_informations(riot_input)
        summoner_info = get_summoner_informations(lol_account_info.puuid)
        league_info = get_league_informations(summoner_info.id)

        league_5x5: LeagueOutputItem = [
            item for item in league_info.league if item.queueType == "RANKED_SOLO_5x5"
        ][0]

        riot_account = RiotAccount(
            game_name=lol_account_info.gameName,
            tag_line=lol_account_info.tagLine,
            puuid=lol_account_info.puuid,
            summoner_id=summoner_info.id,
            discord_member_id=member_created.id,
        )

        riot_account_created = RiotAccountController.create(session, riot_account)

        riot_score = RiotScore(
            tier=league_5x5.tier,
            rank=league_5x5.rank,
            leaguePoints=league_5x5.leaguePoints,
            wins=league_5x5.wins,
            losses=league_5x5.losses,
            created_at=datetime.now(),
            riot_account_id=riot_account_created.id,
        )

        riot_score_created = RiotScoreController.create(session, riot_score)

        embed = Embed(
            title="Membre ajouté avec succès",
            description=f"Le membre {riot_account_created} a été ajouté avec succès",
            color=BrandColors.GREEN,
        )
        embed.add_field(
            name="Compte riot (League of Legends)",
            value=f"{riot_account_created}",
            inline=False,
        )
        embed.add_field(
            name="Score actuel",
            value=f"{riot_score_created}",
            inline=False,
        )

        await ctx.send(embeds=embed)


bot.start(BOT_TOKEN)
