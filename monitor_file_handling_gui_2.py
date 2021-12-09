# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:15:27 2021

@author: Zoletnik
"""

#from tdms_get_data2 import *

import matplotlib.pyplot as plt
import numpy as np
from nptdms import TdmsFile
import datetime
import os

    
def heater_calibration(V):  
    V_set_ref = np.array([1.25 ,1.3,1.35 ,1.4 ,1.45 ,1.5 ,1.55]) 
    I_ref = np.array([24 ,42 ,61 ,94 ,120 ,156 ,185])
    V_ref = np.array([0.606 ,1.02 ,1.58 ,2.22 ,3.2 ,3.8 ,4.48]) 
    P_ref = I_ref *1e-3 * V_ref
    P = np.interp(V,V_ref,P_ref)
    return P


def find_files(startdate=None,starttime='0000',start_datetime=None,
               enddate=None,endtime='2359',end_datetime=None,
               datapath='C:\\ShendR\\Python\\SPI tDMS\\TDMS files',UTC_offset_minutes=60,verbose=True
               ):
    """
    Finds the files in which data for the indicated time interval (local time) can be found.

    Parameters
    ----------
    startdate : string, optional
        The start date YYYYMMDD. If not set the actual daye is assumed.
    starttime : string, optional
        The start time HHMM. The default is '0000'. The time is local time
    start_datetime: numpy datetime64 object
        Alternative to specify the start time. If this is set startdate and stattime is not used.
    enddate: string, optional
        The end date YYYYMMDD. If not set the same day is assumed as the start date.
    endtime: string, optional
        The end time HHMM. The default is '2459'. The time is local time.
    end_datetime: numpy datetime64 object
        Alternative to specify the end time. If this is set enddate and endtime is not used.
    datapath : string
        The data path.
    UTC_offset_minutes: int, optional
        The offset of the local time timpared to UTC in minutes.
    verbose: boolean
        Print messages about progress of processing.

    Raises
    ------
    ValueError
        No suitable file found.

    Returns
    -------
    Returns the filenames, start and end times sorted by increasing starttime.
    file_list: list of strings
        The list of suitable filenames (with full path)
    file_starttime_list: list of np.datetime64 objects
        The start times of the files in local times.
    file_endtime_list: list of np.datetime64 objects
        The end times of the files in local times.
        

    """
    if (start_datetime is None):
        if (startdate is None):
            _startdate = str(datetime.date.today().year) + str(datetime.date.today().month) + str(datetime.date.today().day)
        else:
            _startdate = startdate
        _start_datetime = np.datetime64(_startdate[:4]+'-'+_startdate[4:6]+'-'+_startdate[6:8]+'T'+
                                        starttime[:2]+':'+starttime[2:4]
                                        )
    else:
        _start_datetime = start_datetime

    if (end_datetime is None):        
        if (enddate is None):
            _enddate = _startdate
        else:
            _enddate = enddate
        _end_datetime = np.datetime64(_enddate[:4]+'-'+_enddate[4:6]+'-'+_enddate[6:8]+'T'+
                                      endtime[:2]+':'+endtime[2:4]
                                      )
    else:
        _end_datetime = end_datetime
    file_starttime_list = []
    file_endtime_list = []
    fname_list = []
    act_datetime = _start_datetime
    while act_datetime <= _end_datetime:
        act_date_str = str(act_datetime)
        dirname = os.path.join(datapath,act_date_str[:4]+act_date_str[5:7]+act_date_str[8:10])
        try:
            l = os.listdir(dirname)
        except FileNotFoundError:
            raise ValueError("Wrong datapath.")
        for f in l:
            ind = f.find('.tdms')
            if (ind < 0):
                continue
            if (f[ind:] != '.tdms'):
                continue
            file_start_datetime = np.datetime64(f[:4]+'-'+f[4:6]+'-'+f[6:8]+'T'+f[9:11]+':'+f[11:13]+':'+f[13:15])
            if (file_start_datetime > _end_datetime):
                continue
            fname = os.path.join(dirname,f)
            if (verbose):
                print('Checking {:s}'.format(fname),flush=True)
            with TdmsFile.open(fname) as tdms_file:
                ch_t = tdms_file['MonitorData']['TimeStamp']
                file_start_datetime_from_file = ch_t[0] + np.timedelta64(UTC_offset_minutes, 'm')
                file_end_datetime_from_file = ch_t[-1] + np.timedelta64(UTC_offset_minutes, 'm')
            MAXDIFF = 10 # maximum time difference between time in file name and contents [s]
            if (abs(file_start_datetime_from_file - file_start_datetime) > np.timedelta64(MAXDIFF,'s')):    
                raise ValueError("Warning: File start time from file and file name are different. (file: {:s}".format(fname))
            if (file_start_datetime_from_file > _end_datetime):
                continue
            if (file_end_datetime_from_file < _start_datetime):
                continue
            fname_list.append(fname)
            file_starttime_list.append(file_start_datetime)
            file_endtime_list.append(file_end_datetime_from_file)
        act_datetime += np.timedelta64(1,'D')
    if (len(fname_list) == 0):
        raise ValueError('No data found.')
    rel_starttime = (np.array(file_starttime_list) - np.amin(np.array(file_starttime_list))).astype(float)
    ind = np.argsort(rel_starttime)
    fname_sorted = []
    starttime_sorted = []
    endtime_sorted = []
    for i in ind.tolist():
        fname_sorted.append(fname_list[i])
        starttime_sorted.append(file_starttime_list[i])
        endtime_sorted.append(file_endtime_list[i])
    return fname_sorted,starttime_sorted,endtime_sorted
            
def read_data(data_names=None,startdate=None,starttime='0000',start_datetime=None,
              enddate=None,endtime='2359',end_datetime=None,
               datapath='C:\\ShendR\\Python\\SPI tDMS\\TDMS files\\',UTC_offset_minutes=60,verbose=True):
    """
    Reads multiple data from the TDMS files specified by the start and end dates/times.

    Parameters
    ----------
    data_names : string or list of strings
        The channel names to read. The default is None.
    startdate : string, optional
        The start date YYYYMMDD. If not set the actual daye is assumed.
    starttime : string, optional
        The start time HHMM. The default is '0000'. The time is local time
    start_datetime: numpy datetime64 object
        Alternative to specify the start time. If this is set startdate and stattime is not used.
    enddate: string, optional
        The end date YYYYMMDD. If not set the same day is assumed as the start date.
    endtime: string, optional
        The end time HHMM. The default is '2459'. The time is local time.
    end_datetime: numpy datetime64 object
        Alternative to specify the end time. If this is set enddate and endtime is not used.
    datapath : string
        The data path.
    UTC_offset_minutes: int, optional
        The offset of the local time timpared to UTC in minutes.
    verbose: boolean
        Print messages about progress of processing.

    Raises
    ------
    ValueError
        No suitable file found.
    IOError
        Error deadeing data.

    Returns
    -------
    time : numpy datetime64 array
        The timstamps for the measurements. 
        Use (time-time[0])/np.timedelta64(1,'s') to convert to time relative to first time in seconds.
    data : List of numpy float arrays
        The data.

    """
    
    if (data_names is None):
        raise ValueError('Data names should be set.')
    if (type(data_names) is not list):
        _data_names = [data_names]
    else:
        _data_names = data_names
    if (start_datetime is None):
        if (startdate is None):
            _startdate = str(datetime.date.today().year) + str(datetime.date.today().month) + str(datetime.date.today().day)
        else:
            _startdate = startdate
        _start_datetime = np.datetime64(_startdate[:4]+'-'+_startdate[4:6]+'-'+_startdate[6:8]+'T'+
                                        starttime[:2]+':'+starttime[2:4]
                                        )
    else:
        _start_datetime = start_datetime

    if (end_datetime is None):        
        if (enddate is None):
            _enddate = _startdate
        else:
            _enddate = enddate
        _end_datetime = np.datetime64(_enddate[:4]+'-'+_enddate[4:6]+'-'+_enddate[6:8]+'T'+
                                      endtime[:2]+':'+endtime[2:4]
                                      )
    else:
        _end_datetime = end_datetime
    fnames, starttimes, endtimes = find_files(start_datetime=_start_datetime,end_datetime=_end_datetime,
                                              datapath=datapath,UTC_offset_minutes=UTC_offset_minutes,verbose=verbose
                                              )

    time = np.ndarray(0,dtype=np.datetime64)
    data = [np.ndarray(0,dtype=float)]*len(_data_names)
    for fn in fnames:
        if (verbose):
            print('Processing {:s}'.format(fn),flush=True)
        with TdmsFile.open(fn) as tdms_file:
            ch_t = tdms_file['MonitorData']['TimeStamp']
            t = ch_t[:]
            try:
                start_ind = np.nonzero(t > _start_datetime)[0][0]
            except IndexError:
                continue
            try:
                end_ind = np.nonzero(t < _end_datetime)[0][-1]
            except IndexError:
                continue            
            time = np.concatenate((time,t[start_ind:end_ind+1]))
            data_unit=[]
            for i,signame in enumerate(_data_names):
                if (verbose):
                    print("Reading {:s}".format(signame),flush=True)
                ch = tdms_file['MonitorData'][signame]
                data_unit.append(ch.properties['Unit'])
                data[i] = np.concatenate((data[i],ch[start_ind:end_ind+1].astype(float)))
    dt = np.diff((time - time[0]) / np.timedelta64(1,'s'))
    ind_bad = np.nonzero(dt <= 0)[0]
    if (len(ind_bad) != 0):
        print('Removed {:d} bad time points.'.format(len(ind_bad)),flush=True)
        ind_good = np.nonzero(dt > 0)[0]
        if (len(ind_good) == 0):
            raise ValueError("No good time points found.")
        time = np.concatenate((np.array([time[0]]),time[ind_good + 1]))
        for i in range(len(data)):
            data[i] = np.concatenate((np.array([data[i][0]]),data[i][ind_good + 1]))
    
    return time,data,data_unit

#data = read_data(['Cryo Press 3 (PM4)','Cryo Press 4 (PM5)','T1 - Barrel Temp','T2 - CHead Bottom'],'20211202', '1630')

