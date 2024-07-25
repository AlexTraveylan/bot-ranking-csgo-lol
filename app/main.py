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
from app.core.constants import BOT_TOKEN, PRODUCTION
from app.core.database.models import unit

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
    begin_day.start()


@Task.create(TimeTrigger(hour=5, minute=0, second=0, utc=True))
async def begin_day():
    print("It's a new day")


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
