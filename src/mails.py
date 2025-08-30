from fastapi_mail import FastMail ,ConnectionConfig ,MessageSchema,MessageType
from src.config import Config
from typing import List


mail_conf = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_STARTTLS = Config.MAIL_STARTTLS,
    MAIL_SSL_TLS = Config.MAIL_SSL_TLS,
    USE_CREDENTIALS = Config.USE_CREDENTIALS,
    VALIDATE_CERTS = Config.VALIDATE_CERTS
)

mail = FastMail(config=mail_conf)

def create_message(recipients:list[str],subject:str,body:str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body = body,
        subtype=MessageType.html
    )
    return message