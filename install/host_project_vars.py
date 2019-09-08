"""
Specific variables for the host project.
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

# CONFIGURE ACCORDING TO THE HOST PROJECT
# host project name, this will be displayed in messages and throughout
software_name = "TreeOfLife"

# host project version
software_version = (1, 0, 0)

# provide a link and e-mail with further documentation on the install process
install_wiki = "https://github.com/joaomcteixeira/Tree-of-Life/wiki"
mailist = "https://github.com/joaomcteixeira/Tree-of-Life/issues"

# min GB required to install the host project
# usually depends on the Miniconda ENV
min_space_allowed = 3

# name of the LOG files
installation_log_name = "tree_of_life_install.log"
update_log_name = "tree_of_life_update.log"

# the Miniconda ENV file specific of the host project
env_file = "template_env.yml"

# Miniconda installation folder
miniconda_folder = "miniconda"

# the path where the host project is hosted
# serves updating purposes
new_version_url = \
    "https://github.com/joaomcteixeira/Tree-of-Life/archive/master.zip"
    
# temporary ZIP file for the new version during update
new_version_zip = "master.zip"

# folders to remove during the update
folders_to_remove = ["install", ".github"]

# http://patorjk.com/software/taag/#p=display&h=1&f=Sweet&t=Tree%20of%20Life
banner = r"""
 ___                                          .-.      ___        .-.            
(   )                                        /    \   (   ) .-.  /    \          
 | |_    ___ .-.     .--.    .--.     .--.   | .`. ;   | | ( __) | .`. ;  .--.   
(   __) (   )   \   /    \  /    \   /    \  | |(___)  | | (''") | |(___)/    \  
 | |     | ' .-. ; |  .-. ;|  .-. ; |  .-. ; | |_      | |  | |  | |_   |  .-. ; 
 | | ___ |  / (___)|  | | ||  | | | | |  | |(   __)    | |  | | (   __) |  | | | 
 | |(   )| |       |  |/  ||  |/  | | |  | | | |       | |  | |  | |    |  |/  | 
 | | | | | |       |  ' _.'|  ' _.' | |  | | | |       | |  | |  | |    |  ' _.' 
 | ' | | | |       |  .'.-.|  .'.-. | '  | | | |       | |  | |  | |    |  .'.-. 
 ' `-' ; | |       '  `-' /'  `-' / '  `-' / | |       | |  | |  | |    '  `-' / 
  `.__. (___)       `.__.'  `.__.'   `.__.' (___)     (___)(___)(___)    `.__.'  
                                                                                 
                                                                                 
"""
