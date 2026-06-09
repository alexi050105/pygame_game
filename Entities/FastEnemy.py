from Entities.EnemyDecorator import EnemyDecorator

class FastEnemy(EnemyDecorator):

    def __init__(self, wrapped, multiplier: float = 2.0) -> None:

        super().__init__(wrapped)
        self.multiplier = multiplier

    def move_x(self) -> None:

        original_speed = self._wrapped.speed

        self._wrapped.speed = int(original_speed * self.multiplier)
        self._wrapped.move_x()
        self._wrapped.speed = original_speed

    def move_y(self) -> None:

        original_speed = self._wrapped.speed

        self._wrapped.speed = int(original_speed * self.multiplier)
        self._wrapped.move_y()
        self._wrapped.speed = original_speed





