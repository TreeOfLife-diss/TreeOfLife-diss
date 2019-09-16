# -*- coding: utf-8 -*-
"""
Informative messages for the installation and update processes.
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
import os
import textwrap

from . import ToLCONTACT
from . import ToLHPV
from . import ToLSYSTEM
from . import ToLEXEC

# provide a link and e-mail with further documentation on the install process
install_wiki = ToLHPV.install_wiki
mailist = ToLHPV.mailist
software_name = ToLHPV.software_name
min_space_allowed = ToLHPV.min_space_allowed

# configure textwrapper

tw = textwrap.TextWrapper()
tw.fix_sentence_endings = False
tw.break_long_words = False
tw.drop_whitespace = True
tw.initial_indent = "* "
tw.subsequent_indent = "* "
tw.width = 70


class DisplayMessage:
    def __init__(
            self,
            msg,
            *args,
            title='message',
            stamp='*',
            msgchar='*',
            width=72,
            footer=True,
            **kwargs,
            ):
        
        self.msg = str(msg)
        self.args = args
        self.stamp = (f"{stamp.upper()} " if stamp else '')
        self.msgchar = msgchar
        self.width = width
        self.kwargs = kwargs
        
        self.title = title
        self.footer = footer
        
        self.titlemsg = ''
        self.bodymsg = ''
        self.footermsg = ''
        
        self.build()
    
    def __str__(self):
        return "\n".join(self.displaymessages)
    
    @property
    def displaymessages(self):
        return [
            self.titlemsg,
            self.bodymsg,
            self.footermsg,
            ]
    
    def build(self):
        self.maketitle()
        self.makemsg()
        self.makefooter()
    
    def maketitle(self):
        
        titleformatter = "{:" + self.msgchar + "^" + str(self.width) + "}"
        try:
            t = " {} ".format(self.title.upper())
        except (SyntaxError, AttributeError):
            self.titlemsg = ''
        else:
            self.titlemsg = titleformatter.format(t)
    
    def makemsg(self):
        
        _ = textwrap.dedent(self.msg)
        _ = [textwrap.wrap(s, width=self.width) for s in _.splitlines()]
        
        m = []
        for l in _:
            if l:
                for s in l:
                    m.append(f"{self.stamp}{s}")
        
        self.bodymsg = "\n".join(m)
        
        return
    
    def makefooter(self):
        if self.footer:
            self.footermsg = self.msgchar * self.width
    
def _formats_message_body(s):
    """
    s is a string
    """
    
    body = '\n*\n'.join(
        [tw.fill(line) for line in s.splitlines() if line.strip() != '']
        )
    
    return body + "\n"


def _formats_main_title(s):
    
    star = 72 * '*'
    title = "*** {: ^64} ***".format(s.upper())
    return "{}\n{}\n{}\n".format(star, title, star)


def _formats_short_title(s):
    """
    s is a string
    """
    s = " {} ".format(s.upper())
    return "{:*^72}\n".format(s)


# GENERAL MESSAGES
query = "-> provide a valid option: "

big_query = """
- [Press ENTER to continue]
- Type any '{}' to abort
""".format(", ".join(ToLSYSTEM.deny))

gen_files_msg_head = _formats_main_title("Generated executable files")


list_of_files = ""
for file_ in ToLEXEC.executable_files.keys():
    list_of_files += "-> {}\n".format(os.path.join('bin', file_))

gen_files_msg_tail = _formats_message_body(
    "Executable files were generated inside the installation folder:\n"
    + list_of_files
    )

# SUCCESS MESSAGES

_install_perfect = """
The software installation COMPLETED successfully
"""

install_completed = (
    _formats_main_title("perfect")
    + _formats_message_body(_install_perfect)
    )

# INSTALLATION

start_install = _formats_message_body("Starting installation...")

install_header = (
    _formats_short_title("The required Python libraries must be installed")
    + _formats_message_body("Choose an installation option")
    )

install_options_full = """
[1] Automatically configure Python dependencies and executables (recommended)
[2] I want to manually configure Python dependencies and executables (advanced)
[3] Abort Installation
[4] Show help
"""

# MINICONDA INSTALL

_auto_install_message = (
    "Miniconda (https://www.anaconda.com/) along with the "
    "Python dependencies will be installed in the following folder:\n"
    "{}\n"
    "This Miniconda installation will serve ONLY this folder "
    "not interfeering with your system's Python installation.\n"
    "\n"
    "Miniconda will be installed in SILENT mode, "
    "without additional queries to the user. If you continue, "
    "you accept Anaconda License and Terms and Conditions."
    "\n"
    "You can READ Anaconda Terms and Conditions in the link bellow:\n"
    "\n"
    "https://anaconda.org/about/legal/terms\n"
    "\n"
    "If you do NOT agree type 'exit', 'no', or 'abort' to abort installation. "
    "You can, instead, choose to install the required Python libraries "
    "manually and independently of the Anaconda distribution, "
    "just restart the installation process and choose install option [2].\n"
    "If you AGREE with Anaconda Terms just press ENTER to continue "
    "the installation.\n"
    )

install_miniconda_terms_and_conditions = (
    _formats_short_title("NOTICE")
    + _formats_message_body(_auto_install_message)
    )

install_miniconda_proceed = _formats_message_body(
    "A dedicated Miniconda distribution will be installed"
    )

_query_miniconda_reinstall = """
A Miniconda installation already exists in this folder.
Do you want to reinstall Miniconda"?

If YES, the current Miniconda will be DELETED and a NEW one installed.
If NO, the installation will abort.

[YES/no]:
"""

query_miniconda_reinstall = (
    _formats_short_title("QUERY")
    + _formats_message_body(_query_miniconda_reinstall)
    )

reinstall_canceled = """
* You chose not to reinstall Miniconda.
* Installation CANCELED
"""

envs_okay = "* OK * The Anaconda Environment installed SUCCESSFULLY"

# MANUAL INSTALL

_manual_install = (
    "You chose to configure {} manually, ".format(software_name)
    + "no Python libraries will be installed now.\n"
    "\n"
    "We assume that you are a proficient Python user and "
    "you can and want to READ, UNDERSTAND and INSTALL the "
    "required dependencies on your own.\n"
    "\n"
    "You can check the required Python libraries in the '.yml' env file "
    "inside the 'install' folder. Use this file to create your own "
    "Anaconda environment if you use Anaconda or as a guide to know "
    "which are the Python dependencies for {}.\n".format(software_name)
    + "\n"
    "The installer will now generate TEMPLATE executable files. You may "
    "WISH or NEED to MODIFY {}'s".format(software_name)
    + " executable files according to "
    "your system's and Python preferences.\n"
    "If you don't install the required Python libraries and don't correctly "
    "configure the executable files, "
    "{} MIGHT NOT WORK.".format(software_name)
    )

manual_install = (
    _formats_short_title("notice")
    + _formats_message_body(_manual_install)
    )

# UPDATER

update_var_missing = (
    _formats_short_title("error")
    + _formats_message_body(
        "An installation variable necessary for UPDATING"
        " is missing or broken in installation_vars.py"
        )
    )

update_continues = """
* Despite the ERRORS the update will continue
"""

consider_reinstall = (
    _formats_short_title("notice")
    + _formats_message_body(
        "Something went wrong during the updating process. "
        "The easiest method to solve this issue is to reinstall "
        "the software."
        )
    )

_update_perfect = """
{} update COMPLETED successfully
Press ENTER to finish
""".format(software_name)

update_completed = (
    _formats_main_title("perfect")
    + _formats_message_body(_update_perfect)
    )

# HELP MESSAGES

_add_help = (
    "For additional help write us a message in our mailing list:\n"
    f"{ToLCONTACT.mailist}\n"
    "or check out our web page:\n"
    f"{ToLCONTACT.webpage}"
    )

# additional_help = (
    # _formats_short_title("help")
    # + _formats_message_body(_add_help)
    # + 72 * '*'
    # + "\n"
    # )

additional_help = str(DisplayMessage(_add_help, title='help'))

# ERRORS

not_enough_space = """
* Not enought space available to install the required Miniconda packages.
* At lest {} GB are necessary.
""".format(min_space_allowed)

unknown_python = """
* ERROR * We detected a Python version that is not 2 nor 3.
"""

url_error = """
* ERROR * Could not reach the Miniconda URL
* ERROR * {}
"""

url_unknown = """
* ERROR * URL not found
* ERROR * {}
"""

fs_env_failed = """
* ERROR * The Anaconda Environment COULD NOT be installed.
* ERROR * Check the following error mensage:

{}
"""

path_with_spaces = """
* ERROR * the installation path '{}'
* ERROR * contains spaces. This is NOT allowed!
* ERROR * Please choose another folder
* ERROR * or rename this one.
"""

something_wrong = """
* ERROR * Something went wrong and we could not identify it
* ERROR * Please contact us via {}
* ERROR * and provide the log file created during the process
* ERROR * so that we can help you solve this problem
* ERROR * Thank you!
""".format(mailist)

abort = """
*** Aborting installation ***
"""

terminate = "Press ENTER to TERMINATE"


if __name__ == "__main__":
    print(query)
    print(big_query)
    print(gen_files_msg_head)
    print(gen_files_msg_tail)
    print(install_completed)
    print(start_install)
    print(install_header)
    print(install_options_full)
    print(install_miniconda_terms_and_conditions)
    print(install_miniconda_proceed)
    print(query_miniconda_reinstall)
    print(reinstall_canceled)
    print(envs_okay)
    print(manual_install)
    print(update_var_missing)
    print(update_completed)
    print(update_continues)
    print(consider_reinstall)
    print(additional_help)
    print(not_enough_space)
    print(unknown_python)
    print(url_error)
    print(url_unknown)
    print(fs_env_failed)
    print(abort)
