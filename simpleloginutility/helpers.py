# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Simple Login
# Copyright (C) 2016 byteShaft
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

CONFIG_SECTION_DEFAULT = 'defaults'
CONFIG_SECTION_EMAIL_CREDENTIALS = 'email_credentials'


class ConfigHelpers:

    def __init__(self, config_file):
        self.config_file = config_file
        if os.path.isfile(self.config_file):
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)
        else:
            raise RuntimeError('Config file does not exist.')

    def read_config_parameter(self, config_section, config_key):
        try:
            return self.config.get(config_section, config_key)
        except configparser.NoOptionError or configparser.NoSectionError:
            return None

    def get_email_credential_by_key(self, key):
        return self.read_config_parameter(
            CONFIG_SECTION_EMAIL_CREDENTIALS,
            key
        )

    def get_debug_setting(self):
        value = self.read_config_parameter(CONFIG_SECTION_DEFAULT, 'debug')
        return value == 'True'
