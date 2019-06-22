import requests
import time


def print_header():
    """Печать шапки таблицы для последних блоков в сети BCH"""
    print('LAST 11 BLOCKS')
    height = 'height'
    timestamp = 'timestamp'
    name = 'name'
    print(f'{height:^6}|{timestamp:^10}|{name:^7}')


def is_bch_forked(activation_timestamp):
    """
    Проверяем, произошел ли форк сети BCH. Форк определяется
    заданным средним временем последних 11 блоков сети.
    """

    # Запрашиваем последний блок сети BCH, получаем его номер
    last_block = requests.get('https://bch-chain.api.btc.com/v3/block/latest')
    last_height = last_block.json()['data']['height']

    # Создаем шаблон для запроса последних 11 блоков
    request_template = 'https://bch-chain.api.btc.com/v3/block/'
    for height in range(last_height - 10, last_height + 1):
        request_template += str(height) + ','
    request_template = request_template.strip(',')

    # Запрашиваем информацию о последних 11 блоках
    last_blocks_req = requests.get(request_template)
    last_blocks = {}

    # Записываем интересующую нас информацию в словарь
    for block in last_blocks_req.json()['data']:
        last_blocks[block['height']] = {
            'timestamp': block['timestamp'],
            'name': block['extras']['pool_name'],
        }

    print_header()
    timestamps = []
    for k, v in last_blocks.items():
        timestamps.append(v['timestamp'])  # Собираем список временных отметок
        print(k, v['timestamp'], v['name'])

    # Получаем медианное время последних 11 блоков
    median_time = int(sum(timestamps) / len(timestamps))
    print(f'\nMTP-11 is {median_time}\n')

    if median_time >= activation_timestamp:
        # Если медианное время превышает заданный порог - произошел форк
        print(f'{median_time} >= {activation_timestamp}')
        print('BCH was forked.')
        return True

    return False


if __name__ == '__main__':
    activation_timestamp = int(input('Enter activation timestamp: '))
    bch_forked = False
    while not bch_forked:
        bch_forked = is_bch_forked(activation_timestamp)
        time.sleep(60 * int(not bch_forked))
