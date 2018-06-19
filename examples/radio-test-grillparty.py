# Eric Yihan Chen
# The Automatic Coordination of Teams (ACT) Lab
# University of Southern California
# ericyihc@usc.edu
'''
    Simple example that connects to the first Crazyflie found, triggers
    reading of rssi data and acknowledgement rate for every channel (0 to 125).
    It finally sets the Crazyflie channel back to default, plots link
    quality data, and offers good channel suggestion.

    Better used when the Crazyflie2-nrf-firmware is compiled with bluetooth
    disabled.
'''
import argparse

import matplotlib.pyplot as plt
import numpy as np

import cflib.drivers.crazyradio as crazyradio

import time

radio = crazyradio.Crazyradio()

# optional user input
parser = argparse.ArgumentParser(description='Key variables')
parser.add_argument(
    '-try', '--try', dest='TRY', type=int, default=50,
    help='the time to send data for each channel'
)
# by default my crazyflie uses channel 90
parser.add_argument(
    '-channel', '--channel', dest='channel', type=int,
    default=90, help='the default channel in crazyflie'
)
# by default my crazyflie uses datarate 2M
parser.add_argument(
    '-rate', '--rate', dest='rate', type=int, default=2,
    help='the default datarate in crazyflie'
)
parser.add_argument(
    '-frac', '--fraction',  dest='fraction', type=float,
    default=0.25, help='top fraction of suggested channels'
)
args = parser.parse_args()
init_channel = args.channel
channel = init_channel
# TRY = args.TRY
TRY = 100
try_chg_cf_chn = 500

Fraction = args.fraction
data_rate = args.rate

# monte_carlo_trial
cnt_monte_carlo = 1
rssi_monte_carlo = []
ack_rate_monte_carlo = []
sugg_chn_monte_carlo = []
fig, ax1 = plt.subplots()

radio.set_channel(init_channel)
# radio.set_data_rate(data_rate)
SET_RADIO_CHANNEL = 1

rssi_std = []
rssi = []
ack = []
radio.set_arc(0)
radio.set_address((0xE7,0xE7,0xE7,0xE7,0x14))
radio.set_power(3)
radio.set_data_rate(0)
# radio.set_address((0xFF,0xE7,0xE7,0xE7,0xE7))

count = 0
temp = []
acks = []

# change radio channel
#radio.set_channel(channel)

switch_channels = False

while True:
    #tic = time.time()
    pk = radio.send_packet((0xff, ))
    #toc = time.time()
    #print("Send at " + str(tic) + ", duration " + str(toc-tic))
    if pk.ack:
        count += 1
        acks.append(1)
    else:
        acks.append(0)
    if pk.ack and len(pk.data) > 2 and pk.data[0] & 0xf3 == 0xf3 and pk.data[1] == 0x01:
        # append rssi data
        rssi.append(pk.data[2])
    else:
        rssi.append(0)
    if len(acks) == 10:
        #print("Acks: " + str(np.mean(acks)) + ", RSSI: " + str(np.mean(rssi)))
        percent = int(np.round(np.mean(acks)*100))
        print(str(channel) + ":" + percent*"#" + (100-percent)*" " + "|")
        acks = []
        acks = []
        if switch_channels:
            channel = 45 if channel == 90 else 90
            for x in range(1000):
                radio.send_packet((0xff, 0x03, SET_RADIO_CHANNEL, channel))
            radio.set_channel(channel)
