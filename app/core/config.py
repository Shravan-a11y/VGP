from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
   PROJECT_NAME:str
   API_VERSION:str
   DEBUG:bool

   FIRESTORE_PROJECT_ID:str

   JWT_SECRET_KEY:str
   JWT_ALGORITHM:str
   ACCESS_TOKEN_EXPIRE_MINUTES:int

   model_config=SettingsConfigDict(
    env_file=".env",
    extra="ignore"
    )

settings=Settings()