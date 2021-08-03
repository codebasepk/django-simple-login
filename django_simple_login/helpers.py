# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Copyright (C) CODEBASE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import configparser

CONFIG_FILE_PATH = os.path.expanduser('~/sample_config.ini')
CONFIG_SECTION_DEFAULT = 'defaults'
CONFIG_SECTION_EMAIL_CREDENTIALS = 'email_credentials'
CONFIG_SECTION_DATABASE_CREDENTIALS = 'database_credentials'
CONFIG_SECTION_TWITTER_CREDENTIALS = 'twitter'


class ConfigHelpers:
    def __init__(self, config_file=CONFIG_FILE_PATH):
        if not os.path.isfile(config_file):
            raise RuntimeError('Config file \'{}\' does not exist.'.format(config_file))
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def read_config_parameter(self, config_section, config_key):
        return self.config.get(config_section, config_key, fallback=None)

    def get_email_credential_by_key(self, key):
        return self.read_config_parameter(CONFIG_SECTION_EMAIL_CREDENTIALS, key)

    def get_database_credential_by_key(self, key):
        return self.read_config_parameter(CONFIG_SECTION_DATABASE_CREDENTIALS, key)

    def get_debug_setting(self):
        return self.read_config_parameter(CONFIG_SECTION_DEFAULT, 'debug') == 'True'

    def get_twitter_cred_by_key(self, key):
        return self.read_config_parameter(CONFIG_SECTION_TWITTER_CREDENTIALS, key)
