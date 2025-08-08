from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, select, update, insert, func
from datetime import datetime

DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    faction = Column(String, default="brak")
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

class FactionPoints(Base):
    __tablename__ = "faction_points"

    faction = Column(String, primary_key=True)
    points = Column(Integer, default=0)

class Mission(Base):
    __tablename__ = "missions"

    user_id = Column(Integer, primary_key=True)
    last_completed = Column(DateTime, default=datetime.utcnow)


# ▶️ Inicjalizacja tabel
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ▶️ XP
async def add_xp(user_id, faction, amount):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.xp += amount
            user.level = user.xp // 100 + 1
        else:
            user = User(user_id=user_id, faction=faction, xp=amount, level=amount // 100 + 1)
            session.add(user)
        await session.commit()


async def get_user_data(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return user.faction, user.xp, user.level
        return None


async def get_all_user_data():
    async with async_session() as session:
        result = await session.execute(select(User.faction, User.xp, User.level))
        return result.all()


# ▶️ Punkty frakcji
async def setup_faction_table():
    async with async_session() as session:
        frakcje = ["potter", "wiedzmin", "hobbit", "zmierzch", "igrzyska", "sanderson"]
        for nazwa in frakcje:
            result = await session.execute(select(FactionPoints).where(FactionPoints.faction == nazwa))
            if not result.scalar_one_or_none():
                session.add(FactionPoints(faction=nazwa, points=0))
        await session.commit()


async def add_faction_points(faction, points):
    async with async_session() as session:
        result = await session.execute(select(FactionPoints).where(FactionPoints.faction == faction))
        frak = result.scalar_one_or_none()
        if frak:
            frak.points += points
        else:
            session.add(FactionPoints(faction=faction, points=points))
        await session.commit()


async def get_faction_points():
    async with async_session() as session:
        result = await session.execute(select(FactionPoints.faction, FactionPoints.points))
        return result.all()


# ▶️ Misje
async def get_mission_time(user_id):
    async with async_session() as session:
        result = await session.execute(select(Mission).where(Mission.user_id == user_id))
        misja = result.scalar_one_or_none()
        return misja.last_completed if misja else None


async def set_mission_time(user_id, dt):
    async with async_session() as session:
        result = await session.execute(select(Mission).where(Mission.user_id == user_id))
        misja = result.scalar_one_or_none()
        if misja:
            misja.last_completed = dt
        else:
            session.add(Mission(user_id=user_id, last_completed=dt))
        await session.commit()
