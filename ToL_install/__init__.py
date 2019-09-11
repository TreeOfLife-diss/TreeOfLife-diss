import sys

from . import logger
from . import host_project_vars as ToLHPV
from . import system as ToLSYSTEM
from . import executables as ToLEXEC
from . import messages as ToLMSG

log = logger.get_logger(__name__)

# CONFIRMS PYTHON VERSION
python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

# could use try: except: though fill this clarifies intentions
if python_version == 2:
    user_input = raw_input

elif python_version == 3:
    user_input = input

else:
    log.info(ToLMSG.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    _name = ToLHPV.software_name
    log.info("* {} requires Python 2.7 or 3.x to execute".format(_name))
    log.info(ToLMSG.additional_help)
    log.info(ToLMSG.abort)
    user_input(ToLMSG.terminate)
    sys.exit(1)