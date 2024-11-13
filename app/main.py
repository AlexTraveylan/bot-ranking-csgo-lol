import logging

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
from app.core.commands.after_cs_go_form import AfterCsGoForm, extract_steam_id
from app.core.commands.after_lol_form import AfterLolForm
from app.core.commands.cs_go_ranking import CsGoRanking
from app.core.commands.lol_ranking import RiotRanking
from app.core.constants import BOT_TOKEN, PRODUCTION
from app.core.database.models import DiscordMember, unit

logger = logging.getLogger(__name__)
bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    logger.info("Bot is ready")
    logger.info(f"This bot is owned by {bot.owner}")
    lol_begin_day.start()
    cs_go_begin_day.start()


@Task.create(TimeTrigger(hour=17, minute=30))
async def cs_go_begin_day():
    channel = bot.get_channel(1264655139411857499)

    try:
        with unit() as session:
            module = CsGoRanking(session=session)
            csgo_accounts = module.get_csgo_accounts()
            last_scores = module.get_last_cs_go_score_by_account(csgo_accounts.values())

            new_scores = module.register_actual_score_for_all_accounts(
                csgo_accounts.values()
            )

            embed = Embed(
                title="Counter Strike ranking",
                description="Voici le classement actuel des membres",
                color=BrandColors.BLURPLE,
            )

            for index, (account_id, score) in enumerate(
                sorted(new_scores.items(), key=lambda x: x[1], reverse=True)
            ):
                last_score = last_scores[account_id]
                account = csgo_accounts[account_id]
                member = session.get_one(DiscordMember, account.discord_member_id)
                embed.add_field(
                    name=f"#{index + 1} {member.discord_name}: {account}",
                    value=f"Rank: {score}, (+{score.wins - last_score.wins} wins) (+{score.losses - last_score.losses} losses) (+{score.kills - last_score.kills} kills) (+{score.deaths - last_score.deaths} deaths) (+{score.assists - last_score.assists} assists)",
                    inline=False,
                )

            return await channel.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        logger.exception(e)
        return await channel.send(embeds=embed)

    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            logger.exception(e)
            return await channel.send(embeds=embed)
        else:
            logger.exception(e)
            await channel.send(e.args[0])
            raise e


@Task.create(TimeTrigger(hour=17, minute=00))
async def lol_begin_day():
    channel = bot.get_channel(1264655923071291414)

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
                account = riot_accounts[account_id]
                member = session.get_one(DiscordMember, account.discord_member_id)
                embed.add_field(
                    name=f"#{index + 1} {member.discord_name}: {account}",
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
        logger.exception(e)
        return await channel.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            logger.exception(e)
            return await channel.send(embeds=embed)
        else:
            logger.exception(e)
            await channel.send(e.args[0])
            raise e


@slash_command(
    name="see_riot_accounts",
    description="Affiche la liste des comptes Riot enregistrés",
)
async def see_riot_accounts(ctx: SlashContext):
    """Function to see the list of riot accounts"""
    try:
        with unit() as session:
            module = RiotRanking(session=session)
            riot_accounts = module.get_riot_accounts()

            embed = Embed(
                title="Liste des comptes Riot",
                description="Voici la liste des comptes Riot enregistrés",
                color=BrandColors.BLURPLE,
            )

            for account in riot_accounts.values():
                member = session.get_one(DiscordMember, account.discord_member_id)
                embed.add_field(
                    name=f"{account}",
                    value=f"Ajouté par {member.discord_name}",
                    inline=False,
                )

            return await ctx.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        logger.exception(e)
        return await ctx.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            logger.exception(e)
            return await ctx.send(embeds=embed)
        else:
            logger.exception(e)
            await ctx.send(e.args[0])
            raise e


@slash_command(
    name="create_form_buttons",
    description="Create a button to lol and cs go form",
)
async def create_lol_form_button(ctx: SlashContext):
    if ctx.author_id != bot.owner:
        return await ctx.send("You are not the owner of this bot", ephemeral=True)

    embed = Embed(
        title="Ajouter votre compte de jeu à associer à votre compte Discord",
        # description="Choisissez le formulaire à lancer",
        color=BrandColors.FUCHSIA,
    )

    lol_button = Button(
        custom_id="lol_btn_form",
        style=ButtonStyle.GREEN,
        label="League of Legends",
    )

    cs_go_button = Button(
        custom_id="cs_go_btn_form",
        style=ButtonStyle.BLURPLE,
        label="Counter Strike",
    )

    return await ctx.send(embeds=embed, components=[lol_button, cs_go_button])


@component_callback("lol_btn_form")
async def get_lol_modal(ctx: SlashContext):
    """Function to create the modal league of legends form"""

    my_modal = Modal(
        ShortText(label="Nom d'invocateur", custom_id="summoner_name"),
        ShortText(label="Après le #", custom_id="tagline", value="euw"),
        title="League of Legends",
        custom_id="lol_modal",
    )

    return await ctx.send_modal(modal=my_modal)


@modal_callback("lol_modal")
async def on_lol_modal_answer(ctx: ModalContext, summoner_name: str, tagline: str):
    """Function to handle the model league of legends form"""
    channel = bot.get_channel(1265030202711347322)

    # Clean the summoner name
    summoner_name = summoner_name.strip()
    if "#" in summoner_name:
        summoner_name = summoner_name.split("#")[0]

    # Clean the tagline
    tagline = tagline.strip()

    try:
        with unit() as session:
            module = AfterLolForm(
                summoner_name=summoner_name,
                tagline=tagline,
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
                message = f"Le compte Riot LoL de {member} a été créé avec succès"
            else:
                message = f"Le membre {member} a bien ajouté son smurf"

            embed = Embed(
                title="Compte Riot LoL ajouté",
                description=message,
                color=BrandColors.GREEN,
            )
            embed.add_field(
                name="Compte Riot LoL:",
                value=f"{riot_account}",
                inline=False,
            )
            embed.add_field(
                name="Rank actuel",
                value=f"{riot_score}",
                inline=False,
            )
        try:
            await ctx.send(
                f"Le compte Riot LoL: {riot_account} a bien été ajouté",
                ephemeral=True,
            )
        except Exception:
            pass

        return await channel.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        logger.exception(e)
        return await channel.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur Inconnue",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            logger.exception(e)
            return await channel.send(embeds=embed)
        else:
            logger.exception(e)
            await channel.send(e.args[0])
            raise e


@component_callback("cs_go_btn_form")
async def get_cs_go_modal(ctx: SlashContext):
    """Function to create the modal cs go form"""

    my_modal = Modal(
        ShortText(label="Steam URL ou Steam ID", custom_id="steam_id_or_url"),
        title="Counter Strike",
        custom_id="cs_go_modal",
    )

    return await ctx.send_modal(modal=my_modal)


@modal_callback("cs_go_modal")
async def on_cs_go_modal_answer(ctx: ModalContext, steam_id_or_url: str):
    """Function to handle the model cs go form"""

    channel = bot.get_channel(1264655139411857499)

    try:
        steam_id = extract_steam_id(steam_id_or_url)

        with unit() as session:
            module = AfterCsGoForm(
                steam_id=steam_id,
                discord_author_id=str(ctx.author_id),
                discord_author_name=ctx.author.display_name,
                session=session,
            )

            member = module.get_or_create_discord_member()
            module.check_if_csgo_account_exist(member)
            cs_go_account, csgostats = module.create(member)

            if module.is_member_exist == "create":
                message = f"Le compte counter Strike de {member} a été créé avec succès"
            else:
                message = f"Le membre {member} a bien ajouté son compte Counter Strike"

            embed = Embed(
                title="Compte Counter Strike ajouté",
                description=message,
                color=BrandColors.GREEN,
            )
            embed.add_field(
                name="Compte Counter Strike:",
                value=f"{cs_go_account}",
                inline=False,
            )
            embed.add_field(
                name="Rank actuel",
                value=f"{csgostats}",
                inline=False,
            )

        try:
            await ctx.send(
                f"Le compte Counter Strike: {cs_go_account} a bien été ajouté",
                ephemeral=True,
            )
        except Exception:
            pass

        return await channel.send(embeds=embed)

    except BotException as e:
        embed = Embed(
            title="Erreur",
            description=f"Une erreur est survenue: {e.message}",
            color=BrandColors.RED,
        )
        logger.exception(e)
        return await channel.send(embeds=embed)
    except Exception as e:
        if PRODUCTION:
            embed = Embed(
                title="Erreur Inconnue",
                description="Une erreur inattendue est survenue",
                color=BrandColors.RED,
            )
            logger.exception(e)
            return await channel.send(embeds=embed)
        else:
            logger.exception(e)
            await channel.send(e.args[0])
            raise e


bot.start(BOT_TOKEN)
