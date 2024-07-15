import copy
import csv
import os.path as op

import pytest
from mock import Mock, call, patch, mock_open
from lxml.etree import ElementTree
import paths
import subprocess
import datetime
from AndroidRunner.Plugins.batterymanager.Batterymanager import Batterymanager
import AndroidRunner.util as util




class TestBatterymanagerPlugin(object):
    @pytest.fixture()
    def mock_device(self):
        return Mock()

    @pytest.fixture()
    def fixture_dir(self):
        return op.join(op.dirname(op.abspath(__file__)), 'fixtures')

    @pytest.fixture()
    def batterymanager_plugin(self):
        test_config = {'sample_interval': 100, \
                       'data_points': ['BATTERY_PROPERTY_CURRENT_NOW', \
                                       'EXTRA_VOLTAGE'], \
                       'persistency_strategy': ['csv']}
        test_paths = {'path1': 'path/1'}
        return Batterymanager(test_config, test_paths)

    @staticmethod
    def csv_reader_to_table(filename):
        result = []
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                result.append(row)
        return result

    @staticmethod
    def get_dataset(filename):
        with open(filename, mode='r') as csv_file:
            dataset = set(map(tuple, csv.reader(csv_file)))
        return dataset

    @patch('AndroidRunner.Plugins.Profiler.__init__')
    def test_batterymanager_plugin_succes(self, super_init):
        test_config = {'sample_interval': 100, \
                       'data_points': ['BATTERY_PROPERTY_CURRENT_NOW', \
                                       'EXTRA_VOLTAGE'], \
                       'persistency_strategy': ['csv']}
        test_paths = {'path1': 'path/1'}
        bm = Batterymanager(test_config, test_paths)

        super_init.assert_called_once_with(test_config, test_paths)
        assert bm.output_dir == ''
        assert bm.paths == test_paths
        assert bm.profile is False
        assert bm.sampling_rate == 100
        assert bm.data_points == ['BATTERY_PROPERTY_CURRENT_NOW', \
                                  'EXTRA_VOLTAGE']
        assert bm.persistency_strategy == ['csv']


