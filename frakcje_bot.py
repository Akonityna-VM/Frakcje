import discord
from discord.ext import commands
import aiosqlite
import database
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

DOZWOLONE_KANAŁY = [
    "🎱┃eventy",
    "🧝｜hobbitˑrozmowy",
    "⚡｜potterˑrozmowy",
    "🗡️｜wiedzminˑrozmowy",
    "🧛｜zmierzchˑrozmowy",
    "🏹｜igrzyskaˑrozmowy",
    "🌌｜sandersonˑrozmowy"
]

ROLE_LORE = {
    # Hobbit
    "Hobbit": "Mały, pokojowy mieszkaniec Shire. Ceni spokój, jedzenie i ciepłe napoje.",
    "Atani": "Ludzie – śmiertelni mieszkańcy Śródziemia, podatni na pokusę, ale zdolni do wielkich czynów.",
    "Rohirrim": "Wojowniczy lud z Rohanu, mistrzowie jazdy konnej, wierni królowi i tradycji.",
    "Dúnedain": "Potomkowie Númenorejczyków, strażnicy północy. Długowieczni, szlachetni i skryci.",
    "Quendi": "Pierwsze dzieci Iluvatara – elfy. Mądrzy, piękni, długowieczni i związani z naturą.",
    "Istari": "Magowie wysłani przez Valarów, by wspierać Śródziemie. Najbardziej znani to Gandalf i Saruman.",
    "Majar": "Duchowe istoty, słudzy Valarów. Potężne byty, często działające z ukrycia.",
    "Valar": "Boskie moce Śródziemia, opiekunowie świata stworzonego przez Iluvatara.",
    "Ainur": "Pierwsze duchy stworzone przez Iluvatara. Uczestniczyły w tworzeniu świata przez muzykę.",
    "Władca Pierścieni": "Tytuł Saurona – potężnego Maia, który wykłuł Jedyny Pierścień.",
    "Eru Iluvatar": "Jedyny Stwórca wszystkiego. Ojciec Ainurów i twórca świata Ardy.",

    # Potter
    "Mugol": "Osoba niemagiczna. Nieświadoma istnienia świata czarodziejów.",
    "Charlak": "Urodzony w rodzinie czarodziejów, ale pozbawiony magii.",
    "Skrzat domowy": "Mała, magiczna istota służąca czarodziejom. Silna magia i lojalność.",
    "Szlama": "Czarodziej narodzony z mugoli – często niesłusznie dyskryminowany.",
    "Półkrwi": "Czarodziej z mieszanego pochodzenia – mugolskiego i magicznego.",
    "Czystej krwi": "Czarodziej pochodzący wyłącznie z magicznych rodzin.",
    "Uczeń Hogwartu": "Młody czarodziej uczący się w słynnej szkole magii.",
    "Pracownik ministerstwa magii": "Magiczny urzędnik pracujący dla rządu czarodziejów.",
    "Auror": "Elitarny łowca czarnoksiężników. Walczy z czarną magią.",
    "Animag": "Czarodziej potrafiący zamieniać się w zwierzę według własnej woli.",
    "Dementor": "Stworzenie karmiące się rozpaczą. Stróż Azkabanu.",

    # Wiedźmin
    "Mieszkaniec Temerii": "Zwykły obywatel świata wiedźmina – narażony na potwory i politykę.",
    "Biedna pierdolona piechota": "Najniższy szereg wojskowy. Rzucony na front i zapomniany przez świat.",
    "Aen seidhe": "Elfy zamieszkujące kontynent. Eleganccy, ale wypierani przez ludzi.",
    "Scoia'tael": "Radykalna partyzantka nieludzi walcząca z uciskiem.",
    "Wiedźma z krzywuchowych moczarów": "Starożytna i złowroga istota manipulująca losem ludzi.",
    "Vodyanoi": "Wodne potwory żyjące w głębinach. Często przedstawiane jako bóstwa przez lokalne ludy.",
    "Aen elle": "Elfy z innego wymiaru. Bardziej zaawansowane, ale bezlitosne.",
    "Czarodziej": "Uczony i mag władający potężną mocą. Często wpływają na losy świata zza kulis.",
    "Wiedźmin": "Mutant, najemnik, zabójca potworów. Szybki, precyzyjny, niebezpieczny.",
    "Wampir wyższy": "Nieśmiertelne, inteligentne istoty żywiące się krwią.",
    "Ukryty": "Postać lub potęga działająca w cieniu, nienazwana, niewidoczna.",
    "Dżin": "Magiczna istota potrafiąca spełniać życzenia lub niszczyć rzeczywistość.",

    # Zmierzch
    "Człowiek": "Zwykły śmiertelnik, nieświadomy istnienia nadnaturalnego świata.",
    "Ugryziony": "Osoba zainfekowana jadem wampira. Przemiana w toku...",
    "Nowonarodzony": "Wampir świeżo po przemianie – silny, ale niestabilny.",
    "Wilkołak": "Nadnaturalna istota zmieniająca się w wilka. Strażnik równowagi.",
    "Zmiennokształtny": "Osoba potrafiąca przybierać formy innych stworzeń.",
    "Cullen": "Rodzina wampirów łamiących tradycyjne zasady. Odmienni, szlachetni.",
    "Volturi": "Ród rządzący światem wampirów. Egzekutorzy prawa i władcy strachu.",
    "Strażnik Volturi": "Elitarna jednostka pilnująca porządku i wykonująca rozkazy przywódców.",
    "Królowa Wampirów": "Symboliczna lub faktyczna przywódczyni całego wampirzego świata.",
    "Nieśmiertelny": "Istota, która przekroczyła granice śmierci i czasu.",

    # Igrzyska
    "Mieszkaniec Dystryktu 12": "Zwykły obywatel jednego z najbiedniejszych dystryktów Panem.",
    "Trybut": "Osoba wybrana do udziału w Głodowych Igrzyskach.",
    "Trener": "Były zwycięzca szkolący nowych trybutów przed walką.",
    "Zwycięzca Igrzysk": "Przetrwał arenę i wygrał. Żyje z traumą, ale jest legendą.",
    "Mentor": "Zarządza i wspiera młodszych trybutów. Często z przymusu.",
    "Rebeliant": "Przeciwstawia się Kapitolowi. Symbol oporu.",
    "Symbol Buntu": "Postać inspirująca innych do powstania. Tak jak Kosogłos.",
    "Członek Kapitolu": "Bogaty, rozpieszczony obywatel żyjący kosztem reszty kraju.",
    "Przywódca Rebelii": "Dowódca ruchu oporu przeciwko tyranii Kapitolu.",
    "Prezydent Panem": "Władca całego Panem. Kontroluje wszystkie dystrykty.",

    # Sanderson
    "Mieszkaniec Scadrialu": "Zwykły obywatel świata alomantów. Żyje w cieniu Szlachetnych.",
    "Skaa": "Uciśniona niższa warstwa społeczeństwa Scadrialu.",
    "Mistborn": "Włada wszystkimi metalami alomantycznymi. Niezwykle potężny.",
    "Feruchemik": "Czerpie moc z magazynowania cech w metalach.",
    "Awakener": "Z Nalthis. Ożywia przedmioty za pomocą Oddechów.",
    "Elantrian": "Zmieniony przez Świetlistą Transformację. Mieszkaniec Elantris.",
    "Rycerz Radiant": "Wojownik związany ze sprenem. Walczy z niesprawiedliwością.",
    "Herald Rosharu": "Pradawni wojownicy, nieśmiertelni, strażnicy ładu.",
    "Shardbearer": "Włada Ostrzem Odłamka – orężem o ogromnej mocy.",
    "Naczynie Odłamka": "Istota połączona z jednym z Odłamków Adonalsium. Boska potęga."
}


REACTION_FRAKCJE = {
    "🧝": "hobbit",
    "⚡": "potter",
    "🗡️": "wiedzmin",
    "🧛": "zmierzch",
    "🏹": "igrzyska",
    "🌌": "sanderson"
}
FRAKCJA_OPISY = {
    "hobbit": {
        "emoji": "🧝",
        "opis": "Frakcja Władcy Pierścieni: elfy, ludzie, hobbici, magia, Valarowie.",
    },
    "potter": {
        "emoji": "⚡",
        "opis": "Frakcja Harry'ego Pottera: czarodzieje, Hogwart, Ministerstwo Magii, mugole.",
    },
    "wiedzmin": {
        "emoji": "🗡️",
        "opis": "Frakcja Wiedźmina: potwory, mutacje, wojna, elfy, czarodziejki.",
    },
    "zmierzch": {
        "emoji": "🧛",
        "opis": "Frakcja Zmierzchu: wampiry, wilkołaki, Volturi, Cullenowie, miłość i krew.",
    },
    "igrzyska": {
        "emoji": "🏹",
        "opis": "Frakcja Igrzysk Śmierci: dystrykty, rebelianci, trybuci, Kapitol.",
    },
    "sanderson": {
        "emoji": "🌌",
        "opis": "Cosmere: Roshar, Scadrial, Elantris, Nalthis – magia Sandersona.",
    }
}


LEVEL_ROLES = {
    "potter": {
        1: "Mugol",
        2: "Charlak",
        3: "Skrzat domowy",
        4: "Szlama",
        5: "Półkrwi",
        6: "Czystej krwi",
        7: "Uczeń Hogwartu",
        8: "Pracownik ministerstwa magii",
        9: "Auror",
        10: "Animag",
        11: "Dementor"
    },
    "wiedzmin": {
        1: "Mieszkaniec Temerii",
        2: "Biedna pierdolona piechota",
        3: "Aen seidhe",
        4: "Scoia'tael",
        5: "Wiedźma z krzywuchowych moczarów",
        6: "Vodyanoi",
        7: "Aen elle",
        8: "Czarodziej",
        9: "Wiedźmin",
        10: "Wampir wyższy",
        11: "Ukryty",
        12: "Dżin"
    },
    "hobbit": {
        1: "Hobbit",
        2: "Atani",
        3: "Rohirrim",
        4: "Dúnedain",
        5: "Quendi",
        6: "Istari",
        7: "Majar",
        8: "Valar",
        9: "Ainur",
        10: "Władca Pierścieni",
        11: "Eru Iluvatar"
    },
    "zmierzch": {
        1: "Człowiek",
        2: "Ugryziony",
        3: "Nowonarodzony",
        4: "Wilkołak",
        5: "Zmiennokształtny",
        6: "Cullen",
        7: "Volturi",
        8: "Strażnik Volturi",
        9: "Królowa Wampirów",
        10: "Nieśmiertelny"
    },
    "igrzyska": {
        1: "Mieszkaniec Dystryktu 12",
        2: "Trybut",
        3: "Trener",
        4: "Zwycięzca Igrzysk",
        5: "Mentor",
        6: "Rebeliant",
        7: "Symbol Buntu",
        8: "Członek Kapitolu",
        9: "Przywódca Rebelii",
        10: "Prezydent Panem"
    },
    "sanderson": {
        1: "Mieszkaniec Scadrialu",
        2: "Skaa",
        3: "Mistborn",
        4: "Feruchemik",
        5: "Awakener",
        6: "Elantrian",
        7: "Rycerz Radiant",
        8: "Herald Rosharu",
        9: "Shardbearer",
        10: "Naczynie Odłamka"
    }
}

# 🔧 Auto-tworzenie roli jeśli nie istnieje
async def get_or_create_role(guild, role_name):
    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        return role
    try:
        role = await guild.create_role(name=role_name)
        print(f"✅ Utworzono nową rolę: {role_name}")
        return role
    except discord.Forbidden:
        print(f"❌ Brak uprawnień do stworzenia roli: {role_name}")
    return None

@bot.event
async def on_ready():
    await database.setup_db()
    await database.setup_faction_table()
    print(f'Bot zalogowany jako {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, nie masz uprawnień.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Brakuje argumentu.")
    else:
        raise error

@bot.command()
@commands.has_permissions(administrator=True)
async def frakcje(ctx):
    embed = discord.Embed(
        title="📚 Wybierz swoją frakcję",
        description="\n".join([f"{emoji} – **{nazwa.title()}**" for emoji, nazwa in REACTION_FRAKCJE.items()]),
        color=discord.Color.purple()
    )
    msg = await ctx.send(embed=embed)
    for emoji in REACTION_FRAKCJE:
        await msg.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    guild = bot.get_guild(payload.guild_id)
    emoji = str(payload.emoji)
    frakcja = REACTION_FRAKCJE.get(emoji)

    if not frakcja:
        return  # reakcja spoza listy

    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT faction FROM users WHERE user_id = ?", (payload.member.id,))
        row = await cursor.fetchone()

        if row and row[0] != "brak" and row[0] is not None:
            try:
                await payload.member.send(f"❌ Masz już przypisaną frakcję: **{row[0].title()}**. Nie możesz jej zmienić.")
            except:
                pass
            return  # ZATRZYMAJ przed nadaniem jakichkolwiek ról

    # Jeśli dotąd nie wróciło, to znaczy że można przypisać frakcję i role

    frakcja_ro = await get_or_create_role(guild, frakcja.lower())
    if not frakcja_ro:
        return

    # Usuń stare role frakcyjne
    for r in payload.member.roles:
        if r.name.lower() in REACTION_FRAKCJE.values():
            await payload.member.remove_roles(r)

    await payload.member.add_roles(frakcja_ro)

    async with aiosqlite.connect("frakcje.db") as db:
        if row:
            await db.execute("UPDATE users SET faction = ? WHERE user_id = ?", (frakcja, payload.member.id))
        else:
            await db.execute("INSERT INTO users (user_id, faction, xp, level) VALUES (?, ?, ?, ?)",
                             (payload.member.id, frakcja, 0, 1))
        await db.commit()

    # Dodaj rolę poziomu 1
    level_roles = LEVEL_ROLES.get(frakcja, {})
    role1 = level_roles.get(1)
    if role1:
        rola = await get_or_create_role(guild, role1)
        if rola:
            await payload.member.add_roles(rola)

    try:
        await payload.member.send(f"✅ Wybrano frakcję: **{frakcja.title()}**, rola startowa: **{role1}**.")
    except:
        pass

@bot.command()
@commands.has_permissions(manage_messages=True)
async def dodajxp(ctx, member: discord.Member, liczba: int):
    await database.add_xp(member.id, "brak", liczba)
    frakcja, xp, level = await database.get_user_data(member.id)
    await ctx.send(f"{member.mention} ma teraz {xp} XP i poziom {level}")

    roleset = LEVEL_ROLES.get(frakcja.lower(), {})
    rola_do_dania = None
    for lvl, nazwa_roli in sorted(roleset.items()):
        if level >= lvl:
            rola_do_dania = nazwa_roli

    if rola_do_dania:
        rola = await get_or_create_role(ctx.guild, rola_do_dania)
        if rola and rola not in member.roles:
            await member.add_roles(rola)
            await ctx.send(f"🎉 {member.mention} otrzymał nową rolę: **{rola.name}**!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def odejmijxp(ctx, member: discord.Member, liczba: int):
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT xp, faction FROM users WHERE user_id = ?", (member.id,))
        row = await cursor.fetchone()
        if row:
            xp = max(0, row[0] - liczba)
            level = xp // 100 + 1
            frakcja = row[1]
            await db.execute("UPDATE users SET xp = ?, level = ? WHERE user_id = ?", (xp, level, member.id))
            await db.commit()

            roleset = LEVEL_ROLES.get(frakcja.lower(), {})
            for _, role_name in roleset.items():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role and role in member.roles:
                    await member.remove_roles(role)

            rola_do_dania = None
            for lvl, nazwa_roli in sorted(roleset.items()):
                if level >= lvl:
                    rola_do_dania = nazwa_roli

            if rola_do_dania:
                rola = await get_or_create_role(ctx.guild, rola_do_dania)
                await member.add_roles(rola)
                await ctx.send(f"{member.mention} ma teraz {xp} XP, poziom {level} i rolę {rola.name}")
            else:
                await ctx.send(f"{member.mention} ma teraz {xp} XP i poziom {level}")
        else:
            await ctx.send("Użytkownik nie ma jeszcze konta XP.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def resetxp(ctx, member: discord.Member):
    await database.add_xp(member.id, "brak", 0)
    async with aiosqlite.connect("frakcje.db") as db:
        await db.execute("UPDATE users SET xp = 0, level = 1 WHERE user_id = ?", (member.id,))
        await db.commit()

    frakcja, _, _ = await database.get_user_data(member.id)
    roleset = LEVEL_ROLES.get(frakcja.lower(), {})
    for _, role_name in roleset.items():
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role and role in member.roles:
            await member.remove_roles(role)

    start_role = roleset.get(1)
    if start_role:
        rola = await get_or_create_role(ctx.guild, start_role)
        await member.add_roles(rola)

    await ctx.send(f"{member.mention} zresetowany do poziomu 1 (0 XP).")

@bot.command()
async def poziom(ctx, member: discord.Member = None):
    member = member or ctx.author
    data = await database.get_user_data(member.id)
    if data:
        frakcja, xp, level = data
        await ctx.send(f"{member.mention} | Frakcja: {frakcja.title()} | XP: {xp} | Poziom: {level}")
    else:
        await ctx.send("Brak danych o użytkowniku.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def resetfrakcja(ctx, member: discord.Member):
    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT faction FROM users WHERE user_id = ?", (member.id,))
        row = await cursor.fetchone()
        if not row or row[0] in ["", "brak", None]:
            await ctx.send(f"{member.mention} nie ma przypisanej frakcji.")
            return
        frakcja = row[0]
        await db.execute("UPDATE users SET faction = ? WHERE user_id = ?", ("brak", member.id))
        await db.commit()

    frakcyjne = [r.lower() for r in REACTION_FRAKCJE.values()]
    for r in member.roles:
        if r.name.lower() in frakcyjne:
            await member.remove_roles(r)

    roleset = LEVEL_ROLES.get(frakcja.lower(), {})
    for _, role_name in roleset.items():
        r = discord.utils.get(ctx.guild.roles, name=role_name)
        if r and r in member.roles:
            await member.remove_roles(r)

    await ctx.send(f"✅ {member.mention} został zresetowany z frakcji **{frakcja.title()}**.")

@bot.command()
async def punktyfrakcji(ctx):
    wyniki = await database.get_faction_points()
    if not wyniki:
        await ctx.send("Brak danych.")
        return
    msg = "**🏆 Wyniki frakcji:**\n"
    for nazwa, punkty in wyniki:
        msg += f"**{nazwa.title()}** – {punkty} pkt\n"
    await ctx.send(msg)

@bot.command()
async def ranking(ctx, frakcja=None):
    async with aiosqlite.connect("frakcje.db") as db:
        if frakcja:
            cursor = await db.execute(
                "SELECT user_id, xp FROM users WHERE faction = ? ORDER BY xp DESC LIMIT 10",
                (frakcja.lower(),))
        else:
            cursor = await db.execute(
                "SELECT user_id, xp FROM users ORDER BY xp DESC LIMIT 10"
            )
        top = await cursor.fetchall()

    if not top:
        await ctx.send("Brak danych.")
        return

    msg = f"**🏅 Ranking {'frakcji ' + frakcja.title() if frakcja else 'globalny'}:**\n"
    for i, (uid, xp) in enumerate(top, start=1):
        user = await bot.fetch_user(uid)
        msg += f"{i}. {user.name} – {xp} XP\n"
    await ctx.send(msg)

@bot.command()
async def mojafrakcja(ctx):
    data = await database.get_user_data(ctx.author.id)
    if data:
        frakcja, xp, level = data
        await ctx.send(f"{ctx.author.mention} Frakcja: **{frakcja.title()}**, XP: {xp}, Poziom: {level}")
    else:
        await ctx.send("Nie masz przypisanej frakcji.")

@bot.command()
async def mojerole(ctx):
    rola_lista = [r.name for r in ctx.author.roles if r.name != "@everyone"]
    if rola_lista:
        await ctx.send(f"{ctx.author.mention} Twoje role: {', '.join(rola_lista)}")
    else:
        await ctx.send(f"{ctx.author.mention} Nie masz przypisanych żadnych ról.")

@bot.command()
async def misja(ctx):
    user_id = ctx.author.id
    now = datetime.utcnow()

    async with aiosqlite.connect("frakcje.db") as db:
        cursor = await db.execute("SELECT last_completed FROM missions WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            last_time = datetime.fromisoformat(row[0])
            if now - last_time < timedelta(hours=24):
                godziny = round((timedelta(hours=24) - (now - last_time)).total_seconds() / 3600)
                await ctx.send(f"{ctx.author.mention}, kolejna misja za {godziny}h.")
                return

        misje = [
            "Napisz wiadomość w kanale #eventy.",
            "Podziel się cytatem z książki.",
            "Odpowiedz komuś na pytanie.",
            "Napisz opinię o książce.",
            "Wrzuć coś pozytywnego do #ogólny.",
            "Zaproś znajomego na serwer.",
            "Użyj komendy !poziom i podziel się wynikiem.",
            "Zaproponuj nowy kanał na serwerze."
        ]
        wybrana = random.choice(misje)
        xp = random.randint(30, 80)
        frakcyjne = random.randint(1, 5)

        await database.add_xp(user_id, "brak", xp)
        frakcja, _, _ = await database.get_user_data(user_id)
        if frakcja != "brak":
            await database.add_faction_points(frakcja, frakcyjne)

        await db.execute("INSERT OR REPLACE INTO missions (user_id, last_completed) VALUES (?, ?)",
                         (user_id, now.isoformat()))
        await db.commit()

    await ctx.send(
        f"📝 {ctx.author.mention} Twoja misja: **{wybrana}**\n"
        f"🎁 Nagroda: {xp} XP + {frakcyjne} punktów frakcji"
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def paneladmin(ctx):
    try:
        user_data = await database.get_all_user_data()
        faction_points_data = await database.get_faction_points()
    except Exception as e:
        await ctx.send(f"❌ Błąd pobierania danych: {e}")
        return

    faction_points = dict(faction_points_data)
    stats = {}

    for faction, xp, level in user_data:
        if faction in [None, "", "brak"]:
            continue
        if faction not in stats:
            stats[faction] = {
                "użytkownicy": 0,
                "xp": 0,
                "lvl": 0
            }
        stats[faction]["użytkownicy"] += 1
        stats[faction]["xp"] += xp
        stats[faction]["lvl"] += level

    if not stats:
        await ctx.send("Brak aktywnych frakcji.")
        return

    embed = discord.Embed(
        title="📊 Panel Administratora – Aktywność Frakcji",
        color=discord.Color.gold()
    )

    for faction, dane in stats.items():
        sr_xp = round(dane["xp"] / dane["użytkownicy"]) if dane["użytkownicy"] > 0 else 0
        sr_lvl = round(dane["lvl"] / dane["użytkownicy"]) if dane["użytkownicy"] > 0 else 0
        punkty = faction_points.get(faction, 0)

        embed.add_field(
            name=f"🧱 {faction.title()}",
            value=(
                f"👥 Użytkowników: **{dane['użytkownicy']}**\n"
                f"⭐ Śr. XP: **{sr_xp}**\n"
                f"📈 Śr. Poziom: **{sr_lvl}**\n"
                f"🏆 Punkty frakcji: **{punkty}**"
            ),
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
async def pomoc(ctx):
    embed = discord.Embed(
        title="📚 FrakcjeBot – Spis komend",
        description="Oto dostępne komendy, które możesz używać w swojej frakcji:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🧭 Frakcje",
        value=(
            "`!frakcje` – Wybierz frakcję przez reakcję\n"
            "`!mojafrakcja` – Twoja frakcja, XP, poziom\n"
            "`!mojerole` – Twoje przypisane role"
        ),
        inline=False
    )

    embed.add_field(
        name="🧠 Poziomy i XP",
        value=(
            "`!poziom` – Sprawdź swój poziom i XP\n"
            "`!misja` – Wylosuj misję dzienną\n"
            "*XP zdobywasz też za pisanie na kanałach frakcyjnych*"
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Rywalizacja",
        value=(
            "`!ranking` – Ranking TOP 10 globalnie\n"
            "`!ranking <frakcja>` – Ranking we frakcji\n"
            "`!punktyfrakcji` – Punkty wszystkich frakcji"
        ),
        inline=False
    )

    embed.set_footer(text="Nie widzisz wszystkich kanałów? To dlatego, że frakcje działają w ukryciu 😉")

    await ctx.send(embed=embed)


@bot.command()
async def frakcjainfo(ctx, frakcja: str = None):
    if not frakcja:
        await ctx.send("📚 Użycie: `!frakcjainfo <nazwa>` (np. `!frakcjainfo potter`)")
        return

    frakcja = frakcja.lower()
    opis_data = FRAKCJA_OPISY.get(frakcja)
    poziomy = LEVEL_ROLES.get(frakcja)

    if not opis_data or not poziomy:
        await ctx.send("❌ Nie znaleziono takiej frakcji. Spróbuj: potter, hobbit, wiedzmin, zmierzch, igrzyska, sanderson.")
        return

    embed = discord.Embed(
        title=f"{opis_data['emoji']} Frakcja: {frakcja.title()}",
        description=opis_data["opis"],
        color=discord.Color.dark_gold()
    )

    poziomy_text = "\n".join([f"**{lvl}** – {rola}" for lvl, rola in sorted(poziomy.items())])
    embed.add_field(name="📈 Poziomy i role", value=poziomy_text, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def lore(ctx, *, rola: str = None):
    if not rola:
        await ctx.send("ℹ️ Użycie: `!lore <nazwa roli>` (np. `!lore Mistborn`)")
        return

    rola = rola.strip().title()
    opis = ROLE_LORE.get(rola)

    if not opis:
        await ctx.send(f"❌ Nie mam opisu dla roli **{rola}**.")
        return

    embed = discord.Embed(
        title=f"📖 Lore: {rola}",
        description=opis,
        color=discord.Color.teal()
    )
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignoruj boty

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return  # Nie dodawaj XP za komendy

    if message.channel.name in DOZWOLONE_KANAŁY:
        user_id = message.author.id
        await database.add_xp(user_id, "brak", 5)

        frakcja, xp, level = await database.get_user_data(user_id)

        # Sprawdź, czy należy nadać nową rolę
        rola_do_dania = None
        roleset = LEVEL_ROLES.get(frakcja.lower(), {})
        for lvl, nazwa_roli in sorted(roleset.items()):
            if level >= lvl:
                rola_do_dania = nazwa_roli

        if rola_do_dania:
            rola = discord.utils.get(message.guild.roles, name=rola_do_dania)
            if rola and rola not in message.author.roles:
                # Usuń inne role poziomowe z tej frakcji
                for _, role_name in roleset.items():
                    r = discord.utils.get(message.guild.roles, name=role_name)
                    if r and r in message.author.roles:
                        await message.author.remove_roles(r)

                await message.author.add_roles(rola)
                await message.channel.send(f"{message.author.mention} awansował na **{rola.name}**!")

    await bot.process_commands(message)


bot.run(os.getenv('DISCORD_TOKEN'))





