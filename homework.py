from dataclasses import asdict, dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    SEC_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weiht = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           mean_speed,
                           spent_calories,)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.SEC_IN_MIN
        mean_spead = self.get_mean_speed()
        spent_calories = ((
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * mean_spead + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weiht / self.M_IN_KM * duration_in_min
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1: float = 0.035
    K_2: float = 0.029
    CM_IN_M: int = 100
    DIV_FAC: float = 0.278

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_in_m = self.get_mean_speed() * self.DIV_FAC
        height_in_m = self.height / self.CM_IN_M
        duration_in_min = self.duration * self.SEC_IN_MIN
        spent_calories = ((self.K_1 * self.weiht
                           + (mean_speed_in_m**2 / height_in_m)
                           * self.K_2 * self.weiht) * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_1: float = 1.1
    K_2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + self.K_1)
                          * self.K_2
                          * self.weiht
                          * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    training_type: Training
    if workout_type in training:
        training_type = training[workout_type](*data)
    return training_type


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
