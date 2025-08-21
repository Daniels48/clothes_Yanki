from environs import Env
from dataclasses import dataclass
import os


@dataclass
class Mail:
    user: str
    password: str
    token: str
    key: str
    other_user: str
    host: str
    port: int


@dataclass
class Database:
    name: str
    port: int
    host: str
    password: str
    user: str
    type: str


@dataclass
class Project:
    key: str


@dataclass
class Config:
    mail: Mail
    db: Database
    project: Project


class Config_get:
    def __init__(self, env: Env):
        self.env = env

    def _get_project_data(self) -> Project:
        key = self.env("SECRET_KEY")
        return Project(key=key)

    def _get_mail_data(self) -> Mail:
        user = self.env("MAIL_USER")
        password = self.env("MAIL_PASSWORD")
        token = self.env("MAIL_TOKEN_ID")
        key = self.env("MAIL_KEY")
        other_user = self.env("OTHER_MAIL")
        host = self.env("MAIL_HOST")
        port = self.env.int("MAIL_PORT")

        return Mail(
            user=user,
            password=password,
            token=token,
            key=key,
            other_user=other_user,
            host=host,
            port=port,
        )

    def _get_database_data(self) -> Database:
        name = self.env("DBName", default="django-project")
        user = self.env("DBUser", default="postgres")
        password = self.env("DBPassword", default="1234")
        port = self.env.int("DBPort", default="5432")
        host = self.env("DBHost", default="db")
        type = self.env("DbType", default="postgresql")

        return Database(
            name=name,
            user=user,
            password=password,
            port=port,
            host=host,
            type=type
        )

    def get_all_data(self) -> dict:
        new_dict = {"mail": self._get_mail_data(), "db": self._get_database_data(), "project": self._get_project_data()}
        return new_dict


def load_config() -> Config:
    env = Env()

    path = ".env" if os.path.exists(".env") else ".env.example"  # Если нет .env, использовать .env_example
    env.read_env(path=path)

    data = Config_get(env).get_all_data()

    return Config(mail=data.get("mail"), db=data.get("db"), project=data.get("project"))


