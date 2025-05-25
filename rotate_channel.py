from time import sleep
import logging
import os
import re
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_channels(adapter):
    ch_list = []
    cmd = 'iwlist %s channel' % (adapter)
    channels = os.popen(cmd).read().splitlines()
    for ch in channels:
        if "Channel " in ch and not "Current" in ch:
            ch_num = re.search('Channel (\d+)', ch).group(1)
            ch_freq = re.search('(\d\.\d+) GHz', ch).group(1)
            logger.info('%s: %s Ghz' % (ch_num, ch_freq))
            ch_list.append((ch_num, ch_freq))
    return ch_list

def get_curr_channel(adapter):
    cmd = 'iwlist %s channel' % (adapter)
    ch_num = None
    ch_freq = None
    iwlist_output = os.popen(cmd).read()
    for ch in iwlist_output.splitlines():
        if "Current Frequency" in ch:
            ch_freq = re.search('(\d\.\d+) GHz', ch).group(1)
            ch_num = re.search('\(Channel (\d+)\)', ch).group(1).zfill(2)
    return (ch_num, ch_freq, iwlist_output)
    

#import ipdb; ipdb.set_trace()
if __name__ == "__main__":
    adapter = os.environ.get('ADAPTER')
    time_period = int(os.environ.get('TIME', 600))
    ch_list = get_channels(adapter)
    while True:
       for ch in ch_list:
           logger.info('Switching %s to channel: %s' % (adapter, ch[0]))
           cmd = 'iwconfig %s channel %s' % (adapter, str(ch[0]))
           os.popen(cmd).read()

           curr_ch = get_curr_channel(adapter)
           if curr_ch[:2] == ch:
              logger.info('Ok! Current channel: %s : %s GHz' % (curr_ch[0], curr_ch[1]))
           else:
              logger.info('ERROR! Channel not set! iwlist output was:')
              logger.info(curr_ch[2])
              import ipdb; ipdb.set_trace()
           sleep(time_period)
