import subprocess
from subprocess import check_output
import json

def get_loudness(file_location):
    command = ['ffmpeg', '-nostats', '-i', file_location,  '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-']
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    summary = output.split("Summary:",1)[1]
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


stats = get_loudness('test.wav')
print json.dumps(stats, sort_keys=True, indent=4, separators=(',', ': '))
