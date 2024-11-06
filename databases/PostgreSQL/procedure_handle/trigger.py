import psycopg2
import dotenv 
import time
import logging
import os


dotenv.load_dotenv()
DISTANCE_THRESHOLD = 0.1 # В метрах
DBNAME = os.getenv("DBNAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("log.txt")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def meters_to_degrees_approx(meters: float) -> float:
    """
    Преобразует расстояние в метрах в градусы без учета широты.

    :param meters: Расстояние в метрах.
    :return: Градусы.
    """
    return meters / 111321.0
    


def call_stored_procedure(distance_threshold: float, max_retries: int=5 , delay: float=5) -> None:
    """
    Вызывает хранимую процедуру update_empty_districts с заданным порогом расстояния.
    Если возникает ошибка, пытаемся повторить вызов с задержкой.

    :param distance_threshold: Порог расстояния для замены в метрах 
    :param max_retries: Максимальное количество повторных попыток.
    :param delay: Задержка между повторными попытками в секундах.
    """
    retries = 0
    while retries < max_retries:
        try:
            # Подключение к базе данных
            conn = psycopg2.connect(
                dbname=DBNAME,
                user=USERNAME,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            cursor = conn.cursor()

            argument = meters_to_degrees_approx(distance_threshold)
            argument = max(10 ** -14, argument)

            # Вызов хранимой процедуры
            cursor.callproc('update_empty_districts', (argument,))

            # Фиксация изменений
            conn.commit()

            # Закрытие соединения
            cursor.close()
            conn.close()

            logger.info("Процедура успешно выполнена.")
            return

        except psycopg2.Error as e:
            logger.error(f"Ошибка при выполнении процедуры: {e}")
            retries += 1
            if retries < max_retries:
                logger.info(f"Повторная попытка через {delay} секунд")
                time.sleep(delay)
            else:
                logger.critical("Превышено количество попыток. Процедура не выполнена.")



call_stored_procedure(DISTANCE_THRESHOLD)