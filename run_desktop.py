import os
import time
import sys

import signal
import subprocess


# A top-level script for generating page load results from browsertime
#  For each site in sites.txt
#    For each set of defined preferences
#      Run the one.sh script, passing in reload parameters

def cleanUrl(url):
    cleanUrl = url.replace("http://", '')
    cleanUrl = cleanUrl.replace("https://", '')
    cleanUrl = cleanUrl.replace("/", "_")
    cleanUrl = cleanUrl.replace("?", "_")
    cleanUrl = cleanUrl.replace("&", "_")
    cleanUrl = cleanUrl.replace(":", ";")
    cleanUrl = cleanUrl.replace('\n', ' ').replace('\r', '')
    cleanUrl = cleanUrl[:50]
    return cleanUrl

host_ip = '192.168.86.180'
iterations = '5'

firefox_args = '--firefox.preference dom.performance.time_to_first_interactive.enabled:true '
browsertime_path = 'node ../bin/browsertime.js  '
#firefox_args += '--firefox.geckoProfiler true --firefox.geckoProfilerParams.interval 10   --firefox.geckoProfilerParams.features "js,stackwalk,leaf" --firefox.geckoProfilerParams.threads "GeckoMain,Compositor,ssl,socket,url,bhm,dns" '

# WebPageReplay
wpr = '--firefox.preference network.dns.forceResolve:' + host_ip + ' --firefox.acceptInsecureCerts true '

# Visual metrics:
#firefox_args += '--visualMetrics true --videoParams.addTimer false --video true --firefox.windowRecorder true --videoParams.createFilmstrip false '

prefs = [('chrome', ''), ('firefox', ' --browser firefox')]

file = open('sites.txt', 'r')
for line in file:
    url = line.strip()
    print("loading site: " + url)

    for p, pref in enumerate(prefs):        
        experimentName = pref[0]
        experimentPref = pref[1]
        print(experimentName)
        print(experimentPref)

        common_args = '--pageCompleteWaitTime 8000 --skipHar '
        common_args += '-n ' + iterations + ' ' + url + ' '

        resultUrl = cleanUrl(url)
        resultArg = '--resultDir "browsertime-results/' + resultUrl + '/' + experimentName + '/" '

        completeCommand = browsertime_path + common_args + resultArg + firefox_args + experimentPref
        print( "\ncommand " + completeCommand)
        os.system(completeCommand)
