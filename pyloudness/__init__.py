# -*- coding: utf-8 -*-
import subprocess
import os

def get_loudness(file_location):
    command = ['ffmpeg', '-nostats', '-i', file_location,  '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-']
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
    summary = output.split("Summary:")[-1]
    output = None
    integrated_loudness = summary.split("Integrated loudness:",1)[1].split("Loudness range:",1)[0]
    integrated_loudness_I = integrated_loudness.split("I:",1)[1].split("Threshold:",1)[0].split("LUFS",1)[0].strip()
    integrated_loudness_Threshold = integrated_loudness.split("Threshold:",1)[1].strip().split("LUFS",1)[0]
    loudness_range = summary.split("Loudness range:",1)[1].split("True peak:",1)[0]
    loudness_range_LRA = loudness_range.split("LRA:",1)[1].split("Threshold:",1)[0].split("LU",1)[0].strip()
    loudness_range_Threshold = loudness_range.split("Threshold:",1)[1].split("LRA low:",1)[0].split("LUFS",1)[0].strip()
    loudness_range_LRA_Low = loudness_range.split("LRA low:",1)[1].split("LRA high:",1)[0].split("LUFS",1)[0].strip()
    loudness_range_LRA_Hight = loudness_range.split("LRA high:",1)[1].split("LUFS",1)[0].strip()
    true_peak = summary.split("True peak:",1)[1].strip()
    true_peak_Peak = true_peak.split("Peak:",1)[1].split("dBFS",1)[0].strip()
    stats = {}
    stats['Integrated Loudness'] = {}
    stats['Integrated Loudness']['I'] = float(integrated_loudness_I)
    stats['Integrated Loudness']['Threshold'] = float(integrated_loudness_Threshold)
    stats['Loudness Range'] = {}
    stats['Loudness Range']['LRA'] = float(loudness_range_LRA)
    stats['Loudness Range']['Threshold'] = float(loudness_range_Threshold)
    stats['Loudness Range']['LRA Low'] = float(loudness_range_LRA_Low)
    stats['Loudness Range']['LRA High'] = float(loudness_range_LRA_Hight)
    stats['True Peak'] = {}
    stats['True Peak']['Peak'] = float(true_peak_Peak)
    return stats

def set_loudness(file_location, loudness_in_dB=-23, ignore_clipping=False):
    # calculate gain needed such that integrated loudness is equal to loudness_in_dB
    stats = get_loudness(file_location)
    gain_in_dB = loudness_in_dB - stats['Integrated Loudness']['I']
    linear_gain = pow(10,gain_in_dB/20)
    # output file name (e.g. 'inputfilename_-23LUFS.wav')
    output_file = '.'.join(file_location.split('.')[:-1])+'_'+str(loudness_in_dB)+'LUFS.'+\
                    file_location.split('.')[-1]
    # warning if clipping
    command = ['ffmpeg', '-i', file_location, '-af', 'astats', '-f', 'null', '-'] # get stats
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
    peak = float(output.split('Peak level dB: ')[-1].split('\n')[0]) # take last, overall peak
    assert peak<=0.0, 'Peak allegedly positive (dB)'
    if peak + gain_in_dB >= 0.0: # check if clipping (liberally)
        if ignore_clipping:
            print 'WARNING: '+output_file+' clipped on writing!'
        else:
            print file_location+' would clip if gain applied to reach '+str(loudness_in_dB)+' LUFS; skipping!'
            return # skip, don't apply gain
    # apply gain
    command = ['ffmpeg', '-y', '-i', file_location,  '-af', 'volume='+str(linear_gain), output_file]
    _ = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True) # apply gain; don't print ffmpeg output
    
def equal_loudness(folder_location, loudness_in_dB=-23, ignore_clipping=False):
    for file_name in os.listdir(folder_location):
        if not file_name.startswith('.'):
            set_loudness(os.path.join(folder_location,file_name), loudness_in_dB, ignore_clipping)
