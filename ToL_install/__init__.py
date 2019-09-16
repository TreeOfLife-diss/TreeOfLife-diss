import sys
import traceback

from . import contactus as ToLCONTACT
from . import host_project_vars as ToLHPV
from . import logger
from .logger import LogFormatter
from . import system as ToLSYSTEM
from . import executables as ToLEXEC
from . import messages as ToLMSG
# there are more imports at the end of the file

log = logger.get_logger(__name__)

# CONFIRMS PYTHON VERSION
python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

def something_wrong_with_python_version():
    log.info(ToLMSG.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    _name = ToLHPV.software_name
    log.info("* {} requires Python 2.7 or 3.x to execute".format(_name))
    log.info(ToLMSG.additional_help)
    log.info(ToLMSG.abort)
    user_input(ToLMSG.terminate)
    sys.exit(1)

if python_version not in (2, 3):
    something_wrong_with_python_version()

if ToLSYSTEM.installation_folder.find(" ") > 0:
    log.info(ToLMSG.path_with_spaces.format(system.installation_folder))
    log.info(ToLMSG.additional_help)
    log.info(ToLMSG.abort)
    user_input(ToLMSG.terminate)
    sys.exit(1)

try:
    import urlparse as urlparse
    import urllib as url
    user_input = raw_input
    url_not_found_error = IOError
    filenotfounderror = IOError
    user_input = raw_input
except (NameError, ModuleNotFoundError):
    import urllib.parse as urlparse
    import urllib.request as url
    from urllib.error import URLError as url_not_found_error
    filenotfounderror = FileNotFoundError
    user_input = input
except Exception:
    log.debug(traceback.format_exc())
    something_wrong_with_python_version()

# these imports are kept at the end of the file to keep consistency
# in the import statements. Where all imports should be done here
# and from here imported to the different modules.
from . import commons as ToLCOMM
from . import condamanager as ToLCM