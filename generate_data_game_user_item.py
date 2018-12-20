# -*- coding: utf-8 -*-

from typing import List, Tuple
import numpy as np
import pandas as pd

USER_NUM = 10000
DATE_RANGE_START = '2018-01-01'
DATE_RANGE_END = '2018-12-31'
ITEM_NUM = 10
ITEM_PRICE = 1500
SAMPLE_SIZE = 10000000


def generate_user_id_master(user_num: int) -> List[int]:
    user_id_list = list(range(1, user_num+1))
    return user_id_list


def generate_date_master(start_date: str, end_date: str) -> List[pd.Timestamp]:
    tmp_date_list = pd.date_range(start=start_date, end=end_date).tolist()
    date_list = [d.strftime('%Y-%m-%d') for d in tmp_date_list]
    return date_list


def generate_item_master(item_num: int) -> Tuple[List[int], List[str]]:
    item_id_master = list(range(1, item_num+1))
    item_name_master = ['item{:03}'.format(i) for i in item_id_master]
    return item_id_master, item_name_master


def generate_item_purchase_count(sample_size):
    np.random.seed(0)
    return np.random.poisson(lam=2.2, size=sample_size).tolist()


def generate_game_user_item():
    user_id_master = generate_user_id_master(USER_NUM)
    date_master = generate_date_master(DATE_RANGE_START, DATE_RANGE_END)
    item_id_master, item_name_master = generate_item_master(ITEM_NUM)

    user_id_list = []
    date_list = []
    item_id_list = []
    item_name_list = []
    for user_id in user_id_master:
        for date in date_master:
            user_id_list.extend([user_id] * ITEM_NUM)
            date_list.extend([date] * ITEM_NUM)
            item_id_list.extend(item_id_master)
            item_name_list.extend(item_name_master)

    master = pd.DataFrame(
        data={
            'user_id': user_id_list,
            'date': date_list,
            'item_id': item_id_list,
            'item_name': item_name_list
        },
        columns=['user_id', 'date', 'item_id', 'item_name']
    )
    data = master.sample(n=SAMPLE_SIZE, random_state=0)
    item_purchase_count = generate_item_purchase_count(SAMPLE_SIZE)
    data.loc[:, 'item_purchase_count'] = item_purchase_count
    payment = [cnt * ITEM_PRICE for cnt in item_purchase_count]
    data.loc[:, 'payment'] = payment
    return data


def main():
    data = generate_game_user_item()
    data.to_csv(
        path_or_buf='./data/game_user_item.csv',
        index=False,
        encoding='utf-8'
    )


if __name__ == '__main__':
    main()
