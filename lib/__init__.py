"""
   epics python module
   Matthew Newville <newville@cars.uchicago.edu>
   CARS, University of Chicago

   version    :  3.0.1 (beta version of epics Py3)
   last update:  20-Feb-2010
         
== Overview:
   rewrite of EpicsCA v 2.*, with major goals of:
      a) replacing swig interface with ctypes
      b) better support for thread safety
      c) more complete low-level support to epics channel access interface
      
   major classes will be:
      PV -- Process Variable which will work largely as in EpicsCA 2.*
"""


__version__ = '3.0.1'

import time
import ca
import dbr
import pv
import alarm
import motor
import record
PV    = pv.PV
Alarm = alarm.Alarm
Motor = motor.Motor
Record = record.Record
poll  = ca.poll

def __createPV(pvname,timeout=5.0):
    "create PV, wait for connection: "

    t0 = time.time()
    thispv = PV(pvname)
    if not thispv.connected:
        thispv.connect()
    while not thispv.connected:
        time.sleep(0.001)
        ca.poll()
        if time.time()-t0 > timeout: break
    if not thispv.connected:
        print 'cannot connect to %s' % pvname
        return None

    return thispv

def caput(pvname, value, wait=False, timeout=60):
    """caput(pvname, value, wait=False, timeout=60)
    simple put to a pv's value.
       >>> caput('xx.VAL',3.0)

    to wait for pv to complete processing, use 'wait=True':
       >>> caput('xx.VAL',3.0,wait=True)
    """ 
    pv = __createPV(pvname)
    if pv is not None:
        ret = pv.put(value,wait=wait,timeout=timeout)
        ca.poll()
        return ret

def caget(pvname, as_string=False):
    """caget(pvname, as_string=False)
    simple get of a pv's value..
       >>> x = caget('xx.VAL')

    to get the character string representation (formatted double, enum string, etc):
       >>> x = caget('xx.VAL', as_string=True)
    """
    pv = __createPV(pvname)
    if pv is not None:
        val = pv.get()
        ca.poll()
        if as_string: return pv.char_value
        return val

def cainfo(pvname,print_out=False):
    """cainfo(pvname,print_out=False)

    return printable information about pv
       >>>cainfo('xx.VAL')

    will return a status report for the pv.

    If print_out=True, the status report will be printed,
    and not returned.
    """
    pv = __createPV(pvname)
    if pv is not None:
        pv.get()
        pv.get_ctrlvars()
        if print_out:
            print pv.info
        else:     
            return pv.info
    
