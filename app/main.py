from datetime import datetime

from interactions import (
    BrandColors,
    Button,
    ButtonStyle,
    Client,
    Embed,
    Intents,
    Modal,
    ModalContext,
    ShortText,
    SlashContext,
    component_callback,
    listen,
    modal_callback,
    slash_command,
)

from app.adapter.exception.bot_exception import (
    BotException,
)
from app.adapter.league_of_legend.api_league import (
    get_league_informations,
)
from app.adapter.league_of_legend.schema import LeagueOutputItem
from app.core.commands.after_lol_form import AfterLolForm
from app.core.constants import BOT_TOKEN, PRODUCTION
from app.core.database.models import DiscordMember, RiotAccount, RiotScore, unit
from app.core.database.services.discord_member import DiscordMemberService
from app.core.database.services.riot_account import RiotAccountService
from app.core.database.services.riot_score import RiotScoreService

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
        member: DiscordMember = DiscordMemberService.get_by_discord_id(
            session=session,
            discord_real_name=str(ctx.author_id),
        )

        if member is None:
            raise ValueError("Member not found")

        account: RiotAccount = RiotAccountService.get_by_discord_member_id(
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

        riot_score_created = RiotScoreService.create(session, riot_score)

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


@slash_command(
    name="create_lol_form_button",
    description="Create a button to ask for a League of Legends form",
)
async def create_lol_form_button(ctx: SlashContext):
    """Function to create the button to ask for the league of legends form"""

    # if ctx.author_id != bot.owner:
    #     return await ctx.send("You are not the owner of this bot", ephemeral=True)

    button = Button(
        custom_id="lol_btn_form",
        style=ButtonStyle.GREEN,
        label="League of Legends",
    )

    await ctx.send("Lancer le formulaire", components=button)


@component_callback("lol_btn_form")
async def get_lol_modal(ctx: SlashContext):
    """Function to create the modal league of legends form"""

    my_modal = Modal(
        ShortText(label="Nom d'invocateur", custom_id="summoner_name"),
        title="League of Legends",
        custom_id="lol_modal",
    )
    await ctx.send_modal(modal=my_modal)


@modal_callback("lol_modal")
async def on_lol_modal_answer(ctx: ModalContext, summoner_name: str):
    """Function to handle the model league of legends form"""
    channel = bot.get_channel(842769999638429707)

    try:
        with unit() as session:
            module = AfterLolForm(
                summoner_name=summoner_name,
                discord_author_id=str(ctx.author_id),
                discord_author_name=ctx.author.display_name,
                session=session,
            )

            member = module.get_or_create_discord_member()
            module.check_if_riot_account_exist(member)
            riot_account = module.create_riot_account(member)
            riot_score = module.create_riot_score(
                summoner_id=riot_account.summoner_id, riot_account_id=riot_account.id
            )

            if module.is_member_exist == "create":
                message = f"Le membre {member} a été créé avec succès"
            else:
                message = f"Le membre {member} existait déjà"

            embed = Embed(
                title="Membre ajouté avec succès",
                description=message,
                color=BrandColors.GREEN,
            )
            embed.add_field(
                name="Compte riot (League of Legends) ajouté avec succès",
                value=f"{riot_account}",
                inline=False,
            )
            embed.add_field(
                name="Score actuel",
                value=f"{riot_score}",
                inline=False,
            )

            await channel.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        return await channel.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            return await channel.send(embeds=embed)
        else:
            raise e


bot.start(BOT_TOKEN)
