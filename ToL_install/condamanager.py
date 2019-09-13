# -*- coding: utf-8 -*-
"""
Manages Miniconda and Python ENV installation.
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
import re

from . import (
    ToLHPV,
    log,
    LogFormatter,
    ToLSYSTEM,
    ToLMSG,
    ToLEXEC,
    ToLCOMM,
    )

from . import (
    urlparse,
    url,
    url_not_found_error,
    filenotfounderror,
    user_input,
    )


class CondaCommands(object):
    
    def __new__(cls):
        if system.platform in ("Linux", "MacOSX"):
            return CondaLinux()
        elif platform in ("Windows"):
            return CondaWindows()
        else:
            return CondaLinux()


class CondaLinux(object):
    def __init__(self):
        return
    
    def get_install_command(self, install_file, install_folder):
        return "{} -b -p {}".format(install_file, install_folder)
    
    def get_conda_exec(self, install_folder):
        return os.path.join(install_folder, 'bin', 'conda')
    
    def get_env_python_exec(self, install_folder):
        return os.path.join(install_folder, 'bin', 'python')


class CondaWindows(object):
    def __init__(self):
        return
    
    def get_install_command(self, install_file, install_folder):
        cmd = "{} /InstallationType=JustMe /RegisterPython=0 /S /D={}".format(
            install_file,
            install_folder,
            )
        return cmd
    
    def get_conda_exec(self, install_folder):
        # https://stackoverflow.com/questions/37117571/where-does-anaconda-python-install-on-windows
        # https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10
        # https://stackoverflow.com/questions/28612500/why-anaconda-does-not-recognize-conda-command
        return os.path.join(install_folder, 'Scripts', 'conda.exe')
    
    def get_env_python_exec(self, install_folder):
        # https://docs.anaconda.com/anaconda/user-guide/tasks/integration/python-path/
        return os.path.join(install_folder, 'python.exe')


class MinicondaWebLinks(object):
    def __init__(self):
        self.base_weblink = ToLSYSTEM.base_miniconda_weblink
        
        self.miniconda_installer_weblink = \
            ToLSYSTEM.miniconda_installer_weblink
        
        
       
        
        
        return
    
    @property
    def base_weblink(self):
        """
        base web link where to download Miniconda from.
        
        Example: https://repo.continuum.io/miniconda/
        """
        return self._base_weblink
    
    @base_weblink.setter
    def base_weblink(self, link):
        # TODO: set some ping check here?
        self._base_weblink = link
        debug_msg = "<base_weblink> set to: {}"
        log.debug(debug_msg.format(self._base_weblink))
    
    @property
    def miniconda_installer_weblink(self):
        """
        Miniconda download file
        """
        return self._miniconda_installer_weblink
        
    @miniconda_installer_weblink.setter
    def miniconda_web_file(self, file_name):
        self._miniconda_installer_weblink = file_name
        debug_msg = "<miniconda_installer_weblink> set to: {}"
        log.debug(debug_msg.format(self._miniconda_installer_weblink))
    

class CondaManager(object):
    """
    Manages Miniconda installation and ENV configuration.
    """
    
    def __init__(self, cwd=None, env=None):
        """
        Parameters:
            
            - cwd (opt, str): the Miniconda installation path.
                Defaults to os.get_cwd()
            
            - env (opt): a YML env file. If None provided, can't install
                environment.
        """
        
        if system.platform not in ("Linux", "MacOSX", "Windows"):
            warmsg = (
                "Your platform is not Linux, MacOSX or Windows. "
                "Miniconda installation command will be "
                "same as if this was a UNIX machine. "
                "If the installation fails please contact us for support."
                )
            log.info(LogFormatter(warmsg, stamp='warning'))
        
        self.install_folder = cwd or os.getcwd()
        
        self.minicondaweblinks = MinicondaWebLinks()
        
        # ~ self.miniconda_base_web_link = system.base_miniconda_web_link
        

        
        self.miniconda_download_link = urlparse.urljoin(
            self.miniconda_base_web_link,
            self.miniconda_web_file,
            )
        
        self.miniconda_install_file = os.path.join(
            self.install_folder,
            self.miniconda_web_file,
            )
        
        self.miniconda_install_folder = os.path.join(
            self.install_folder,
            system.default_miniconda_folder
            )
        
        self.env_nane = 'treeoflife'
        self.env_file = env
        
        self.conda_commands = CondaCommands()
        
        return
    
    @property
    def install_folder(self):
        """
        Installation directory.
        """
        return self._install_folder
    
    @install_folder.setter
    def install_folder(self, folder):
        self._install_folder = folder
    

    

    
    @property
    def miniconda_download_link(self):
        return self._miniconda_download_link
    
    @miniconda_download_link.setter
    def miniconda_download_link(self, link):
        self._miniconda_download_link = link
        debug_msg = "<miniconda_download_link> set to: {}"
        log.debug(debug_msg.format(self._miniconda_download_link))
    
    @property
    def miniconda_install_file(self):
        return self._miniconda_install_file
    
    @miniconda_install_file.setter
    def miniconda_install_file(self, exec_file):
        self._miniconda_install_file = exec_file
        debug_msg = "<miniconda_install_file> set to: {}"
        log.debug(debug_msg.format(self._miniconda_install_file))
    
    @property
    def miniconda_install_folder(self):
        """
        Miniconda installation folder.
        """
        return self._miniconda_install_folder
    
    @miniconda_install_folder.setter
    def miniconda_install_folder(self, folder):
        self._miniconda_install_folder = folder
        debug_msg = "<miniconda_install_folder> set to: {}"
        log.debug(debug_msg.format(self._miniconda_install_folder))
    
    @property
    def env_file(self):
        """
        Miniconda environment file for host project.
        """
        return self._env_file
    
    @env_file.setter
    def env_file(self, env_file):
        """
        Parameters
        ----------
        env_file :obj:`str`
            Path to Anaconda Env (.yml) file.
        """
        
        if env_file is None:
            self._env_file = None
            log.debug("<env_file>: ".format(self._env_file))
            self.env_name = None
            self.env_version = None
            return
        
        log.debug("reading env_file: {}".format(env_file))
        
        valid_file = all((
            isinstance(env_file, str),
            env_file.endswith('.yml'),
            os.path.exists(env_file),
            os.path.isfile(env_file),
            ))
        
        log.debug("<valid_file>: {}".format(valid_file))
            
        if valid_file:
            
            self._env_file = env_file
            
            with open(self._env_file, 'r') as f:
                for line in f:
                    
                    if line.startswith("name:"):
                        env_name = line.strip().split()[-1]
                        self.env_name = env_name
                    
                    elif line.startswith("# version:"):
                        env_version = line.strip().split()[-1]
                        self.env_version = env_version
        
        elif not(isinstance(env_file, str)):
            raise ValueError("Miniconda env file name not a string")
        
        elif not(env_file.endswith('.yml')):
            err_msg = "* ERROR * '{}' should have .yml extension"
            log.info(err_msg.format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        elif not(os.path.exists(env_file)):
            log.info("* ERROR * '{}' does not exists.".format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        elif not(os.path.isfile(env_file)):
            log.info("* ERROR * '{}' is not a file.".format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        log.debug("<env_file>: {}".format(self._env_file))
        
        return
    
    @property
    def conda_exec(self):
        return self._conda_exec
    
    @conda_exec.setter
    def conda_exec(self, conda_exec):
        """
        Sets path to Miniconda 'conda' executable.
        """
        
        if not(os.path.exists(conda_exec)):
            err_msg = "* ERROR * conda exec file does NOT exist: {}"
            log.info(err_msg.format(conda_exec))
            log.info(messages.something_wrong)
            log.info(messages.additional_help)
            log.info(messages.abort)
            commons.sys_exit()
        
        self._conda_exec = conda_exec
        debug_msg = "Miniconda conda bin exec set to: {}"
        log.debug(debug_msg.format(self._conda_exec))
    
        return
    
    @property
    def env_name(self):
        """
        Conda environment name for the host project.
        """
        return self._env_name
    
    @env_name.setter
    def env_name(self, name):
        self._env_name = name
        log.debug("<env_name>: {}".format(self._env_name))
        return
    
    @property
    def env_python_exec(self):
        """Python executable for host project."""
        return self._env_python_exec
    
    @env_python_exec.setter
    def env_python_exec(self, python_exec):
        self._env_python_exec = python_exec
        log.debug("<env_python_exec>: {}".format(self._env_python_exec))
    
    @property
    def env_version(self):
        return self._env_version
    
    @env_version.setter
    def env_version(self, env_version):
        """
        Sets Miniconda environment version.
        Should be integer.
        """
        try:
            int(env_version)
        
        except TypeError as e:
            self._env_version = None
            log.debug(e)
            log.debug("<env_version>: None")
            return
        
        except ValueError as e:
            log.info(
                "* ERROR * Python environment version"
                "should be integer type"
                )
            log.info("* ERROR * env version not set")
            log.debug(e)
            commons.sys_exit()
            return
        
        self._env_version = env_version
        log.debug("<env_version>: {}".format(self._env_version))
        return
    
    @property
    def env_folder(self):
        return self._env_folder
    
    @env_folder.setter
    def env_folder(self, env_folder):
        """
        Defines an existent ENV folder
        """
        
        if not(os.path.exists(env_folder)):
            log.info(
                "* ERROR* folder does NOT exists: {}".format(env_folder)
                )
            log.info(messages.something_wrong)
            log.info(messages.additional_help)
            log.info(messages.abort)
            commons.sys_exit()
        
        self._env_folder = env_folder
        log.debug("<env_folder>: {}".format(self._env_folder))
        return
    
    def check_previous_miniconda_folder(self, folder='[M|m]iniconda.*'):
        """
        Checks if a Miniconda related folder exists inside
        the host project installation folder. Accepts regex.
        
        Returns folder name, False otherwise.
        """
        log.debug("checking if miniconda install exists")
        
        dirlist = self._get_all_subfolders(self.install_folder)
        
        miniconda_folder = self._get_miniconda_folder(dirlist, folder)
        
        n_matches = len(miniconda_folder)
        
        if n_matches == 0:
            # no Miniconda folders found
            log.debug("returning False")
            return False
        
        elif n_matches == 1:
            log.debug("returning: {}".format(miniconda_folder[0]))
            return miniconda_folder[0]
            
        elif n_matches > 1:
            log.info("More than one Miniconda folder found")
            log.info("You may wish to remove them manually")
            log.info(messages.something_wrong)
            log.info(messages.abort)
            commons.sys_exit()
            return
    
    def _get_all_subfolders(self, folder):
        list_dir = os.listdir(folder)
        dirlist = [a for a in list_dir if os.path.isdir(a)]
        log.debug("<dirlist>: {}".format("\n".join(dirlist)))
        return dirlist
    
    def _get_miniconda_folder(self, dirlist, folderregex):
        mask = re.compile(folderregex)
        miniconda_folder = [a for a in dirlist if mask.match(a)]
        log.debug("<miniconda_folder>: {}".format(miniconda_folder))
        return miniconda_folder
    
    def download_miniconda(self):
        """
        Downloads Miniconda installation file.
        """
        
        log.info("* Downloading Miniconda...")
        log.debug("url: {}".format(self.miniconda_download_link))
        log.debug("destination: {}".format(self.miniconda_install_file))
        
        commons.download_file(
            self.miniconda_download_link,
            self.miniconda_install_file,
            )
        
        commons.change_permissions_777(self.miniconda_install_file)
        log.debug("permissions changed")
        
        return
    
    def install_miniconda(self):
        """
        Routine to install Miniconda.
        """
        
        exec_line = self.conda_commands.get_install_command(
            self.miniconda_install_file,
            self.miniconda_install_folder,
            )
        
        log.debug("<exec_line>: {}".format(exec_line))
        
        # installs miniconda
        commons.sub_call(exec_line)
        
        # sets miniconda conda and python exec files
        self.conda_exec = self.conda_commands.get_conda_exec(self.miniconda_install_folder)
        self.env_python_exec = self.conda_commands.get_env_python_exec(self.miniconda_install_folder)
        
        return
    
    def install_package(self, package):
        """
        Install a given package in Miniconda.
        
        Parameters:
        
            - package (str): the name of the package.
                If desired, version can be given, example:
                    'conda-build=3.16.0'
        """
        
        # https://conda.io/docs/user-guide/tasks/manage-pkgs.html#installing-packages
        
        log.debug("installing package: {}".format(package))
        
        exec_line = "{} install -y {}".format(
            self.conda_exec,
            package
            )
        
        exec_output = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        log.debug("\n".join(exec_output))
        
        log.debug("package installaged")
        
        logs_package_installation(package)
        
        return
    
    def logs_package_installation(self, package):
        """
        Logs package installation with 'conda list'
        """
        
        package_name = package.split('=')[0]
        
        exec_line = "{} list {}".format(
            self.conda_exec,
            package_name
            )
        
        exec_output = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        log.debug("\n".join(exec_output))
        
        return
    
    def install_env(self):
        """
        Installs Anaconda Environment.
        """
        
        if self.env_name is None:
            log.debug("no environment to install... ignoring...")
            return
        
        log.info("* Starts Miniconda Environment Installation")
        
        # defines command to create environment from .yml file
        exec_line = '{} env create -f {}'.format(
            self.conda_exec,
            self.env_file
            )
        
        log.debug("<exec_line>: {}".format(exec_line))
        
        commons.sub_call(exec_line)
        
        # sets python env variables
        
        self.env_folder = os.path.join(
            self.miniconda_install_folder,
            'envs',
            self.env_name,
            )
        
        self.env_python_exec = self.conda_commands.get_env_python_exec(self.env_folder)
        
        # self.set_python_version_folder()
        
        return
    
    def logs_env_information(self):
        """
        Registers installed env to log file.
        """
        
        if self.env_name is None:
            log.debug("no environment to install... ignoring...")
            return
        
        log.info("* Registering environment...")
        
        # confirm environment was installed correctly
        exec_line = "{} list -n {}".format(
            self.conda_exec,
            self.env_name,
            )
        
        # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        installed_env = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        log.debug("\n".join(installed_env))
        
        return
    
    def add_install_folder_to_site_packages(self):
        """
        Adds the host project directory to the Miniconda environment.
        """
        
        # https://stackoverflow.com/questions/37006114/anaconda-permanently-include-external-packages-like-in-pythonpath
        # https://stackoverflow.com/questions/32715261/how-to-add-folder-to-search-path-for-a-given-anaconda-environment
        # https://conda.io/docs/commands/build/conda-develop.html
        
        exec_line = " ".join(
            [
                self.conda_exec,
                'develop',
                '-p',
                self.env_folder,
                self.install_folder,
                ]
            )
        
        result = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        log.debug("\n".join(result))
        log.debug("Host project folder added to site-packges")
    
        return
    
    def remove_env(self):
        """
        Removes Miniconda Environment.
        """
        
        if self.env_name is None:
            log.debug("no environment to remove... ignoring...")
            return
        
        log.info("* Removing Miniconda Environment")
        
        exec_line = '{} remove -vy --name {} --all'.format(
            self.conda_exec,
            self.env_name,
            )
        
        commons.sub_call(exec_line)
        
        return


if __name__ == "__main__":
    
    print('I am Tree-of-Life')
    # ~ cm = CondaManager()
    cm = CondaCommands()
    print(type(cm))