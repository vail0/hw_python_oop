from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    msg: str = ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.'
                )

    def get_message(self) -> str:
        '''Результаты тренировки'''
        return self.msg.format(self.training_type, self.duration,
                               self.distance, self.speed, self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM   # км

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration  # км/ч

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('не определён тип тренировки')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    BURN_KOEF_1: int = 18
    BURN_KOEF_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.BURN_KOEF_1 * self.get_mean_speed() - self.BURN_KOEF_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR
                )
#               км/ч * кг / (м/км) * ч * (мин/ч) -> кг * м/мин


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    BURN_KOEF_1: float = 0.035
    BURN_KOEF_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.BURN_KOEF_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * self.BURN_KOEF_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR
                )
#               ((своя ед. счисл.) * кг) * ч * мин/ч = () * кг * мин


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    BURN_KOEF_1: float = 1.1
    BURN_KOEF_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)
#                     м / ((м/км) * ч) = км/ч

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.BURN_KOEF_1)
                * self.BURN_KOEF_2 * self.weight)
#               км/ч * кг


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        raise ValueError('Тип тренировки не определён')


def main(training: Training) -> None:
    """Главная функция."""
    tr_message = training.show_training_info()
    print(tr_message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
