import redis.asyncio as aioredis
from  src.config import Config

JTI_EXPIRY= 3600

token_blocklist = aioredis.from_url(
    f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    encoding="utf-8",
    decode_responses=True
)

async  def blacklist_token(jti:str) -> None:
    await token_blocklist.set(name=jti,value='',ex=JTI_EXPIRY)

async  def is_token_blacklisted(jti: str)->bool:
    return  await token_blocklist.exists(jti) > 0
