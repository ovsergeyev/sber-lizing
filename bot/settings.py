from dataclasses import dataclass
from environs import Env


@dataclass
class Bot:
    token: str
    chat_id: str


@dataclass
class Settings:
    bot: Bot


def load_settins(path: str = ".env") -> Settings:
    env = Env()
    env.read_env(path)
    return Settings(
        bot=Bot(
            token=env.str("TG_BOT_TOKEN"),
            chat_id=env.str("TG_CHAT_ID"),
        )
    )


settings = load_settins(".env")
print(settings)
