#coding:utf-8
import logging
import threading

from bll.AA import AA
from bll.CA import CA
from bll.CZ import CZ
from bll.MU import MU
from bll.Y8 import Y8
from bll.BR import BR
from bll.KE import KE
from bll.RU import RU
from bll.CX import CX
from bll.UA import UA
from bll.EK import EK
from bll.NH import NH
from bll.CI import CI
from bll.CV import CV
from bll.OZ import OZ
from bll.BA import BA

logging.basicConfig(level=logging.WARNING,
                    format='(%(threadName)s) %(message)s',)

#AA().startCapture()
#CA().startCapture()
#CZ().startCapture()
#MU().startCapture()
#Y8().startCapture()
#BR().startCapture()
#KE().startCapture()
#RU().startCapture()
#CX().startCapture()
#UA().startCapture()
#EK().startCapture()
#NH().startCapture()
#CI().startCapture()
#CV().startCapture()
#OZ().startCapture()
BA().startCapture()