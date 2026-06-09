from Entities.EnemyDecorator import EnemyDecorator
from Parameters.Imports import *

class ArmoredEnemy(EnemyDecorator):

    def __init__(self, wrapped) -> None:

        super().__init__(wrapped)
        self.hits_remaining: int = 2

    def take_hit(self) -> bool:

        self.hits_remaining -= 1

        if self.hits_remaining <= 0:
            return True

        self.image = pygame.transform.laplacian(self._wrapped.image)

        return False