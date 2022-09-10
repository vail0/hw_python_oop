class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 avg_speed: float,
                 cal_burnt: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.avg_speed = avg_speed
        self.cal_burnt = cal_burnt

    def get_message(self) -> str:
        get_mess = (f'Тип тренировки: {self.training_type:}; '
                    f'Длительность тренировки: {self.duration:.3f} ч.; '
                    f'Дистанция: {self.distance:.3f} км; '
                    f'Ср. скорость: {self.avg_speed:.3f} км/ч; '
                    f'Потрачено ккал: {self.cal_burnt:.3f}.'
                    )
        return get_mess


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
#    LEN_PADDLE = 1.38
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

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
        dist = self.action * self.LEN_STEP / self.M_IN_KM   # для бега и ходьбы
        return dist  # км

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed  # км/ч

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass    # Не трогай (по заданию)

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
    def get_spent_calories(self) -> float:
        koef_1 = 18
        koef_2 = 20
        spent = ((koef_1 * self.get_mean_speed() - koef_2)
                 * self.weight / self.M_IN_KM
                 * self.duration * self.MIN_IN_HOUR
                 )
#               км/ч * кг / (м/км) * ч * (мин/ч) -> кг * м/мин
        return spent


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
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
        koef_1 = 0.035
        koef_2 = 0.029
        spent = ((koef_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * koef_2 * self.weight)
                 * self.duration * self.MIN_IN_HOUR
                 )
#               ((своя ед. счисл.) * кг) * ч * мин/ч = () * кг * мин

        return spent


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.35

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        pool_length: float,
        count_pool: int
    ):
        super().__init__(action, duration, weight)
        self.pool_length = pool_length
        self.count_pool = count_pool

    def get_mean_speed(self):
        pool_speed = (self.pool_length * self.count_pool
                      / self.M_IN_KM / self.duration)
#                     м / ((м/км) * ч) = км/ч
        return pool_speed

    def get_spent_calories(self) -> float:
        koef_1 = 1.1
        koef_2 = 2
        spent = (self.get_mean_speed() + koef_1) * koef_2 * self.weight
#               км/ч * кг
        return spent


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


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
