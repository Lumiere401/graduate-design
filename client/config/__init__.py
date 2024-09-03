from .config import Conf
import os

path = os.path.abspath(".") + "/client/res/config.cfg"
CONF = Conf(path)
