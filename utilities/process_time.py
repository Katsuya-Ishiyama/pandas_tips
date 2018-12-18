# -*- coding: utf-8 -*-

import logging
import sys
import timeit
from typing import Callable, List, Any
from matplotlib import pyplot as plt
from pandas import DataFrame


logger = logging.getLogger()
stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    level=logging.INFO,
    handlers=[stdout_handler],
    format='[%(asctime)s] %(levelname)s %(filename)s:%(funcName)s:L%(lineno)d - %(message)s'
)


class PandasProcessTimeMeasure(object):

    def __init__(self, data: DataFrame, sample_sizes: List[int], number: int=10):
        self.data = data
        self.sample_sizes = sample_sizes
        self.sample_datasets = [self.create_sample_data(n) for n in sample_sizes]
        self.number = number
        self.methods = {}
        self.process_time = None

    def set_method(self, name: str, method: Callable[[Any], DataFrame]):
        self.methods.setdefault(name, method)

    def measure_average_process_time(self, method: Callable[[Any], DataFrame], args: tuple=None, kwargs: dict=None) -> float:
        if (args is None) and (kwargs is None):
            def test_func():
                method()
        elif (args is not None) and (kwargs is None):
            def test_func():
                method(*args)
        elif (args is None) and (kwargs is not None):
            def test_func():
                method(**kwargs)
        else:
            def test_func():
                method(*args, **kwargs)

        _number = self.number
        logger.debug('number of iterations at timeit: {}'.format(_number))
        logger.debug('start timeit')
        total_process_time_sec = timeit.timeit('test_func()', globals=locals(), number=_number)
        logger.debug('end timeit')
        average_process_time_sec = total_process_time_sec / float(_number)
        logger.debug('average process time: {} [sec]'.format(average_process_time_sec))
        return average_process_time_sec

    def create_sample_data(self, n: int) -> DataFrame:
        return self.data.sample(n)

    def measure_process_time_for_each_sample_sizes(self) -> DataFrame:
        _measurement_time = {'sample_size': self.sample_sizes}
        logger.debug('sample sizes: {}'.format(self.sample_sizes))
        for method_name, method in self.methods.items():
            logger.debug('processing method: {}'.format(method_name))
            average_process_times = []
            for data in self.sample_datasets:
                logger.debug('shape of data: {}, {}'.format(*data.shape))
                _time = self.measure_average_process_time(method=method, args=(data,))
                logger.debug('processing time: {} [sec]'.format(_time))
                average_process_times.append(_time)
            _measurement_time.setdefault(method_name, average_process_times)
            logger.debug('_measurement_time: {}'.format(_measurement_time))
        process_time = DataFrame(data=_measurement_time)
        process_time.set_index('sample_size', inplace=True)
        process_time.sort_index(axis=1, inplace=True)
        self.process_time = process_time
    
    def plot_process_time(self):
        self.process_time.plot()
        plt.xlabel('Sample Size')
        plt.ylabel('Processing Time [sec]')
        plt.show()
