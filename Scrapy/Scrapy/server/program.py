import logging
from bll.AACargoCapture import aaCargoCapture
from bll.AirChinaCargoCapture import airChinaCargoCapture
from bll.CSCargoCapture import csCargoCapture 

import threading


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)


#aaCargoCapture().startCapture()
#airChinaCargoCapture().startCapture()
csCargoCapture().startCapture()