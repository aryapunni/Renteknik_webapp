from pydantic import BaseSettings

class Settings(BaseSettings):
    arc_primary_key: str
    arc_secondary_key: str
    arc_client_id: str
    arc_secret: str
    arc_url: str


settings = Settings()

# if __name__ == "__main__":
#     print(settings.dict())
