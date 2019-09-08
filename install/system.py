# -*- coding: utf-8 -*-
"""
Manages system information and other parameters for
installation and updating.
"""
# TreeOfLife - DISS (2019-)
# https://github.com/TreeOfLife-diss
#
# Contributors to this file:
# - João M.C. Teixeira (https://github.com/joaomcteixeira)
#
# Tree-of-Life is free software: you can redistribute it and/or modify
# it under the terms of the LGPL - GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# LGPL - GNU Lesser General Public License for more details.
#
# You should have received a copy of the this license along
# with this library. If not, see <http://www.gnu.org/licenses/>.
import platform as pltfrm
import os
from install import host_project_vars

# about the default installation folder
_file_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
installation_folder = os.path.abspath(os.path.join(_file_path, os.pardir))

# about the running system
_platforms = {"Linux": "Linux", "Darwin": "MacOSX", "Windows": "Windows"}
_executable_file_extensions = {"Linux": "", "MacOSX": "", "Windows": "py"}

platform = _platforms[pltfrm.system()]
bits = "x86_64" if (pltfrm.machine().endswith('64')) else "x86"
exec_file_extension = _executable_file_extensions[platform]

# about conda env
latest_env_file = os.path.join(_file_path, host_project_vars.env_file)
default_miniconda_folder = os.path.join(
    installation_folder,
    host_project_vars.miniconda_folder
    )

with open(latest_env_file, 'r') as f:
    for line in f:
        if line.startswith('name:'):
            latest_env_name = line.strip().split()[-1]
        elif line.startswith('# version:'):
            latest_env_version = int(line.strip().split()[-1])


# about downloading Miniconda
base_miniconda_web_link = "https://repo.continuum.io/miniconda/"
_miniconda_file_extensions = {
    "Linux": "sh",
    "MacOSX": "sh",
    "Windows": "exe"
    }
miniconda_file_extension = _miniconda_file_extensions[platform]


# other variables
approve = ["Y", "YES"]
deny = ["N", "NO", "EXIT", "E", "A", "ABORT"]
