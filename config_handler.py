import requests
import getpass
import win32api
import win32con
import os
from configparser import ConfigParser


class Config_Handler(object):

    def __init__(self):
        self.current_user = os.getlogin()
        self.acc_file = os.path.join(
            'C:\\Users', self.current_user, 'AppData\\Local\\opl_settings.ini')
        self.create_data_file()
        self.config = ConfigParser()
        self.config.read(self.acc_file)

    def create_data_file(self):
        if not os.path.exists(self.acc_file):
            with open(self.acc_file, 'w+') as f:
                win32api.SetFileAttributes(
                    self.acc_file, win32con.FILE_ATTRIBUTE_HIDDEN)

    def check_data(self, section, *data):
        return section in self.config and all(i in self.config[section] for i in data)

    def write_data(self, section, **data):
        if not section in self.config:
            self.config.add_section(section)

        for key, value in data.items():
            self.config.set(section, key, value)

        with open(self.acc_file, 'r+') as config_file:
            self.config.write(config_file)

    def read_data(self, section):
        if not section in self.config:
            return None
        else:
            return [self.config[section][i] for i in self.config[section]]

    def flush_data(self, section):
        flush_ok = self.config.remove_section(section)

        with open(self.acc_file, 'r+') as config_file:
            config_file.truncate(0)
            self.config.write(config_file)

        return flush_ok


test_config = Config_Handler()

# test_config.write_data('user_data', username='test_user', password='test_pass')
# test_config.write_data('opl_data', folder='test_folder')

# test = test_config.read_data('user_data')
# print(test)

# print(test_config.flush_data('opl_data'))

input('Press Enter')
