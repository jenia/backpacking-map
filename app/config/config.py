from dataclasses import dataclass

import yaml


@dataclass
class Config():
    environ: str

def config() -> Config:
    with open("config.yaml", 'r', encoding="utf-8") as f:
        return Config(**yaml.load(f.read(), Loader=yaml.CLoader))
