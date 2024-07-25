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
    Task,
    TimeTrigger,
    component_callback,
    listen,
    modal_callback,
    slash_command,
)

from app.adapter.exception.bot_exception import (
    BotException,
)
from app.core.commands.after_lol_form import AfterLolForm
from app.core.commands.lol_ranking import RiotRanking
from app.core.constants import BOT_TOKEN, PRODUCTION
from app.core.database.models import DiscordMember, unit

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
    begin_day.start()


@Task.create(TimeTrigger(hour=5, minute=0))
async def begin_day():
    channel = bot.get_channel(842769999638429707)

    try:
        with unit() as session:
            module = RiotRanking(session=session)
            riot_accounts = module.get_riot_accounts()
            last_scores = module.get_last_riot_score_by_account(riot_accounts.values())
            new_scores = module.register_actual_score_for_all_accounts(
                riot_accounts.values()
            )

            embed = Embed(
                title="Riot ranking",
                description="Voici le classement actuel des membres",
                color=BrandColors.BLURPLE,
            )

            for index, (account_id, score) in enumerate(
                sorted(new_scores.items(), key=lambda x: x[1], reverse=True)
            ):
                last_score = last_scores[account_id]
                embed.add_field(
                    name=f"#{index + 1} {riot_accounts[account_id]}",
                    value=f"{score} (+{score.wins - last_score.wins} wins) (+{score.losses - last_score.losses} losses)",
                    inline=False,
                )

            return await channel.send(embeds=embed)

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
            await channel.send(e.args[0])
            raise e


@slash_command(
    name="see_riot_accounts",
    description="Affiche la liste des comptes riot enregistrés",
)
async def see_riot_accounts(ctx: SlashContext):
    """Function to see the list of riot accounts"""
    try:
        with unit() as session:
            module = RiotRanking(session=session)
            riot_accounts = module.get_riot_accounts()

            embed = Embed(
                title="Liste des comptes riot",
                description="Voici la liste des comptes riot enregistrés",
                color=BrandColors.BLURPLE,
            )

            for account in riot_accounts.values():
                member = session.get_one(DiscordMember, account.discord_member_id)
                embed.add_field(
                    name=f"{account}",
                    value=f"Ajouté par {member.discord_name} ({member.discord_id})",
                    inline=False,
                )

            return await ctx.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        return await ctx.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            return await ctx.send(embeds=embed)
        else:
            await ctx.send(e.args[0])
            raise e


@slash_command(
    name="create_lol_form_button",
    description="Create a button to ask for a League of Legends form",
)
async def create_lol_form_button(ctx: SlashContext):
    """Function to create the button to ask for the league of legends form"""

    if ctx.author_id != bot.owner:
        return await ctx.send("You are not the owner of this bot", ephemeral=True)

    button = Button(
        custom_id="lol_btn_form",
        style=ButtonStyle.GREEN,
        label="League of Legends",
    )

    return await ctx.send("Lancer le formulaire", components=button)


@component_callback("lol_btn_form")
async def get_lol_modal(ctx: SlashContext):
    """Function to create the modal league of legends form"""

    my_modal = Modal(
        ShortText(label="Nom d'invocateur", custom_id="summoner_name"),
        title="League of Legends",
        custom_id="lol_modal",
    )

    return await ctx.send_modal(modal=my_modal)


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

            return await channel.send(embeds=embed)

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
            await channel.send(e.args[0])
            raise e


bot.start(BOT_TOKEN)
