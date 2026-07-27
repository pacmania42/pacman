import json
from pydantic import BaseModel, Field


class Config(BaseModel):

    highscore_filename: str = Field(default="")

    width: int = Field(gt=5, default=20)
    hight: int = Field(gt=5, default=20)

    lives: int = Field(ge=0, default=3)

    pacgum_points: int = Field(default=10)
    s_pacgum_points: int = Field(default=50)
    ghost_points: int = Field(default=200)

    level_max_time: int = Field(default=90)

    seed: int = Field(default=42)

    def load(self, file_path: str):

        try:
            with open(file_path, "r") as file:
                data = json.load(file)

                self.highscore_filename = data["highscore_filename"]

                self.width = data["width"]
                self.hight = data["hight"]

                self.lives = data["lives"]

                self.level_max_time = data["level_max_time"]
                self.seed = data["seed"]

                self.pacgum_points = data["scoring"]["points_per_pacgum"]
                self.s_pacgum_points = data[
                    "scoting"][
                        "points_per_super_pacgum"
                            ]
                self.ghost_points = data["scoring"]["points_per_ghost"]

        except Exception as e:
            print(e)


config = Config()

config.load("config.json")
print(config)
