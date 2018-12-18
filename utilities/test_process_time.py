# -*- coding: utf-8 -*-

import time
from pandas import DataFrame
from process_time import PandasProcessTimeMeasure


# コンストラクタにdataを指定する場合

def method1(data):
    sample_size = data.shape[0]
    for _ in range(sample_size):
        time.sleep(0.1)
    return data

def method2(data):
    sample_size = data.shape[0]
    for _ in range(sample_size):
        time.sleep(0.2)
    return data

test_data = DataFrame(
    data={'a': [1, 2, 3, 4, 5, 6], 'b': [7, 8, 9, 10, 11, 12]},
    columns=['a', 'b']
)

process_time_measure = PandasProcessTimeMeasure(
    data=test_data,
    sample_sizes=[3, 5]
)
process_time_measure.set_method(name='method01', method=method1)
process_time_measure.set_method(name='method02', method=method2)
process_time_measure.measure_process_time_for_each_sample_sizes()
print(process_time_measure.process_time)
process_time_measure.plot_process_time()

# コンストラクタにdataを指定しない場合

def method3(sample_size):
    a = []
    b = []
    for _a in range(sample_size):
        for _b in range(sample_size):
            a.append(_a)
            b.append(_b)
    return DataFrame(
        data={'a': a, 'b': b},
        columns=['a', 'b']
    )

process_time_measure = PandasProcessTimeMeasure(
    sample_sizes=[3, 5]
)
process_time_measure.set_method(name='method03', method=method3)
process_time_measure.measure_process_time_for_each_sample_sizes()
print(process_time_measure.process_time)
process_time_measure.plot_process_time()