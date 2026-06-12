from Entities.Enemy.EnemyDecorator import EnemyDecorator
from Parameters.Imports import *

class ArmoredEnemy(EnemyDecorator):

    def __init__(self, wrapped) -> None:

        super().__init__(wrapped)
        self.hits_remaining: int = default_armored_enemy_hits

    def update(self) -> None:
        self._wrapped.update()
        self.image = ARMORED_ENEMY_SPRITES["right"] if self.rect.centerx \
                <= self.player.rect.centerx else ARMORED_ENEMY_SPRITES["left"]
        self.rect = self._wrapped.rect

    def take_hit(self) -> bool:

        self.hits_remaining -= 1

        if self.hits_remaining <= 0:
            return True

        self.image = pygame.transform.laplacian(self._wrapped.image)

        return False