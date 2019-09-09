# -*- coding: utf-8 -*-
"""
Common fuctions that serve installation and update.
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
import sys
import os
import subprocess
import stat
import shutil
import ctypes

from install import logger
from install import host_project_vars
from install import system
from install import messages
from install import executables

log = logger.InstallLogger(__name__).gen_logger()

python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

if python_version < 3:
    import urllib as url
    url_not_found_error = IOError
    user_input = raw_input

elif python_version == 3:
    import urllib
    import urllib.request as url
    url_not_found_error = urllib.error.URLError
    user_input = input

else:
    log.info(messages.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    log.info(messages.something_wrong)
    log.info(messages.additional_help)
    log.info(messages.abort)
    user_input(messages.terminate)
    sys.exit(1)


def check_available_disk_space(min_space=None):
    """
    Checks available disk space.
    
    Parameters
    ----------
    min_space : :obj:`float
        The minimum space allowed in GBs.
        Defaults to host_project_vars.min_space_allowed
    
    Returns
    -------
    bool
        ``True`` if available space is higher than `min_space`,
        ``False`` otherwise.
    """
    
    min_space = min_space or host_project_vars.min_space_allowed
    log.debug("<min_space>: {}".format(min_space))
    
    try:
        min_space = float(min_space)
    except ValueError as e:
        log.exception(e)
        log.info("<min_space> should be integer")
        sys_exit()
    
    log.info("* Checking available diskspace...")
    
    dirname = os.path.expanduser("~")
    
    if system.platform == "Windows":
        calc_space = _available_space_windows
    else:
        calc_space = _available_space_linux_unix
    
    free_space_GB = calc_space(dirname)
    
    log.info("* ... available space: approx. {} GB".format(free_space_GB))
    
    if free_space_GB > min_space:
        log.info("* Enough disk space. Continuing...\n")
        return True
    
    elif free_space_GB <= min_space:
        return False
        
    else:  # expect the unexpected
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()


def _available_space_windows(dirname):
    """
    Calculates the available free space for Windows platforms.
    """
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p(dirname),
        None,
        None,
        ctypes.pointer(free_bytes)
        )
    free_space_GB = int(free_bytes.value / 1024 / 1024 / 1024)
    return free_space_GB


def _available_space_linux_unix(dirname):
    """
    Calculates the available free space for Linux/Unix platforms.
    """
    statvfs = os.statvfs(dirname)
    free_space_GB = \
        int(statvfs.f_frsize * statvfs.f_bavail / 1024 / 1024 / 1024)
    return free_space_GB


def reporthook(blocknum, blocksize, totalsize):
    """
    Modified from:
    
    https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("\r downloaded... %d" % (readsofar,))


def download_file(link, destination):
    """
    Downloads file.
    
    Parameters
    ----------
    link : :obj:`str`
        the file URL
    
    destination :obj:`str`
        Where to save the downloaded file in disk
    
    Returns
    -------
    None
    """
    log.info("* Downloading {}...".format(link))
    log.info("* ... to destination: {}".format(destination))
    
    try:
        url.urlretrieve(
            link,
            destination,
            reporthook
            )
    except url_not_found_error as e:
        log.info(messages.url_error)
        log.info(messages.something_wrong)
        log.debug(e)
        log.info(messages.abort)
        sys_exit()
    except ValueError as e:
        log.info(messages.url_unkown)
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.abort)
        sys_exit()
    except Exception as e:
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.abort)
        sys_exit()
    
    if os.path.exists(destination):
        log.debug("destination file found: {}".format(destination))
        log.info("... Download completed")
    
    else:
        log.info("* ERROR * Couldn't find the downloaded file")
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    return


def change_permissions_777(file_):
    """
    Changes <file_> permissions to 777.
    """
    log.debug("changing permissions to file: {}".format(file_))
    
    try:
        os.chmod(file_, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except FileNotFoundError as e:
        log.exception(e)
        log.info("* ERROR * File '{}' not found!".format(file_))
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    log.debug("... OKAY")
    
    return


def remove_folders(folder_list):
    """
    Removes a list of folders
    
    Parameters
    ----------
    folder_list :obj:`list`
        The list of folders to remove.
    
    Returns
    -------
    None
    """
    
    if not(isinstance(folder_list, list)):
        log.info("*ERROR * folder_list parameters should be list")
        log.info("*ERROR * found instance of {}".format(type(folder_list)))
        sys_exit()
    
    log.debug("removing folders: {}".format("\n".join(folder_list)))
    
    for folder in folder_list:
        
        if os.path.exists(folder) and os.path.isdir(folder):
            log.debug("removing folder: {}".format(folder))
            shutil.rmtree(folder)
            log.info("*** Removed folder: {}".format(folder))
        
        else:
            log.debug("folder '{}' not found or is not dir".format(folder))
    
    log.debug("folders removed OKAY")
    
    return


def sub_call(exec_line):
    """
    Executes a subprocess.
    
    Parameters
    ----------
    exec_line : :obj:`str`
        The command to execute.
    
    Returns
    -------
    The output of execution.
    """
    log.info("* Executing ...{}".format(exec_line))
    args = exec_line.strip().split()
    log.debug("args passed: {}".format(args))
    
    try:
        # maintains compatiblity with Python3 < 3.5
        # https://docs.python.org/3.5/library/subprocess.html#call-function-trio
        proc = subprocess.check_output(args)
    
    except FileNotFoundError as e:
        log.info("* ERROR * Could not find '{}'".format(args[0]))
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    except subprocess.CalledProcessError as e:
        log.info("* ERROR * subprocess.CalledProcessError ocurred.")
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    return proc


def create_executables(installation_folder, python_exec):
    """
    Creates executables based on user.executables module.
    
    Parameters
    ----------
    installation_folder :obj:`str`
        The software installation folder, where the 'bin' folder 
        will reside.
        
    python_exec : :obj:`str`
        The full path for the python executable.
        Will be written to the shebang line.
    
    Returns
    -------
    None
    """
    
    log.info(messages.gen_files_msg_head)
    
    bin_folder = os.path.join(installation_folder, 'bin')
    if not os.path.exists(bin_folder):
        os.mkdir(bin_folder)
        log.debug("'bin' folder didn't exists, created")
    
    else:
        log.debug("'bin' folder already existed")
    
    log.debug("<python_exec>: {}".format(python_exec))
    
    for exec_name, code in executables.executable_files.items():
        
        exec_file = os.path.join(bin_folder, exec_name)
        
        fout = open(exec_file, 'w')
        log.debug("opened {}".format(exec_file))
        
        fout.write(executables.shebang.format(python_exec) + code)
        fout.close()
        
        change_permissions_777(exec_file)
    
    log.info(messages.gen_files_msg_tail)
    
    return


def register_install_vars(
        install_dir,
        python_exec=None,
        install_option=None,
        conda_exec=None,
        env_file=None,
        env_name=None,
        env_version=None,
        miniconda_folder=None
        ):
    """
    Writes installation variables to .py file.
    """
    
    install_reg_name = os.path.join(install_dir, 'installation_vars.py')
    
    fout = open(install_reg_name, 'w')
    log.debug("install_reg.py openned: {}".format(install_reg_name))
    
    installation_vars = """
# This file registers the installation variables
# which are required for debugging and updating purposes.
#
# Please do not delete it from the installation folder
#
# For additional help, please write us at:
# {}

from pathlib import Path

install_option = {}
install_dir = Path(r'{}')
conda_exec = {}
python_exec = {}
miniconda_folder = {}
installed_env_file = {}
installed_env_name = {}
installed_env_version = {}
""".format(
        messages.mailist,
        install_option,
        install_dir,
        "Path(r'{}')".format(conda_exec) if conda_exec else None,
        "Path(r'{}')".format(python_exec) if python_exec else None,
        "Path(r'{}')".format(miniconda_folder) if miniconda_folder else None,
        "Path(r'{}')".format(env_file) if env_file else None,
        "'{}'".format(env_name) if env_name else None,
        env_version
        )
    
    log.debug(installation_vars)
    
    fout.write(installation_vars)
    fout.close()
    log.debug("install_reg created")
    
    return


def sys_exit(number=1):
    user_input(messages.terminate)
    sys.exit(number)
    return
