from dataclasses import dataclass


@dataclass
class Repo:
    owner: str
    repo: str

    def __str__(self) -> str:
        return f'{self.owner}/{self.repo}'
