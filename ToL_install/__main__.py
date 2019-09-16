import time

from . import log
from . import ToLHPV
from . import ToLSYSTEM
from . import ToLMSG
from . import ToLEXEC
from . import user_input
from . import ToLCOMM


# STARTS INSTALLATION
log.debug("{} installation initiated".format(ToLHPV.software_name))
log.debug("<installation_folder>: {}".format(ToLSYSTEM.installation_folder))
log.info(ToLHPV.banner)
log.info(ToLMSG.start_install)
time.sleep(0.5)   # little human feeling

log.info(ToLMSG.install_header)
log.info(ToLMSG.install_options_full)

install_choice = ToLCOMM.install_choice()