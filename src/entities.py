from pydantic import BaseModel, Field


class PlayerData(BaseModel):

    name: str = Field(min_length=3,
                      max_length=10,
                      pattern=r"^[a-zA-Z0-9 ]+$",
                      default="   ")

    score: int = Field(ge=0, default=0)

    lives: int = Field(gt=0, default=3)


class GhostData(BaseModel):

    vunerable: bool = Field(default=False)
