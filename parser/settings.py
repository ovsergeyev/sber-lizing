from dataclasses import dataclass
from environs import Env
import os

@dataclass
class Log:
    log_level_file: str
    log_level_console: str
    log_dir_path: str

@dataclass
class DB:
    host: str
    name: str
    user: str
    password: str
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
  
@dataclass
class Bot:
    token: str
    chat_id: str

@dataclass
class Settings:
    mode: str
    db: DB
    log: Log
    bot: Bot

    
def load_settings(path: str = ".env") -> Settings:
    # os.environ.clear()
    env = Env()
    env.read_env(path)
    return Settings(
        mode=env.str('MODE'),
        log=Log(
            log_dir_path=env.str('LOG_DIR_PATH'),
            log_level_file=env.str('LOG_LEVEL_FILE'),
            log_level_console=env.str('LOG_LEVEL_CONSOLE'),
        ),
        db=DB(
            host=env.str("DB_HOST"),
            name=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            port=env.int("DB_PORT"),
        ),
        bot=Bot(
            token=env.str("TG_BOT_TOKEN"),
            chat_id=env.str("TG_CHAT_ID"),
        )
    )

  
settings = load_settings('.env')
print(settings)