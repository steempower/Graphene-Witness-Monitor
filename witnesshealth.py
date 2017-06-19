#!/usr/bin/env python3
import telnetlib
import time, datetime
import requests
import json
import os
import sys
from grapheneapi import GrapheneAPI

# RPC wallet details
rpc_host		= "localhost" 	#Hostname or IP address of the RPC wallet you are connecting too
rpc_port		= 8092		#Port that RPC connection allows inbound communication too
rpc_username		= ""		#RPC username, default username in Graphene config is blank / ""
rpc_password		= ""		#RPC password, default password in Graphene config is blank / ""

# Witness/delegate/producer account name to check
witness 		= ""  		#witness name
witness_url 		= "" 		#URL for witness information/proposal
signing_key1 		= "" 		#Primary Signing Pub Key
signing_key2 		= "" 		#Secondary Signing Pub Key

# Hotswitch your signing keys on missed block? - APLHA not been live tested - I'm serious, don't use this feature
hotswitch		= "false"	# This setting is testing/ALPHA please leave this a "false" unless you understand the risks
hotswitch_threshold 	= int(5)	# This is the amount of block sucessfully signed before attempting to switch nodes (prevents ping pong)

# Telegram notification settings
telegram_token 		= "" 		# Create your Telegram bot at @BotFather (https://telegram.me/botfather)
telegram_id    		= ""    	# Get your telegram id at @MyTelegramID_bot (https://telegram.me/mytelegramid_bot)

# Health monitor settings
seed_timeout_check      = int(10)	# seconds before timeout is called on telnet public seed operation.
check_rate              = int(90)	# amount of time (seconds) for the script to sleep before next check! Every x seconds the script will check missed blocks. 
check_rate_feeds_seed   = int(3600)	# set this to a considerably higher amount of seconds than check_rate so this script won't check your price_feed and seed availibility as much as that.
currentmisses           = int(0)	# current block misses (note this is set at -1 missed blocks so you will get 1 initial notification if you have more than 0 blocks missed currently. You could set this to your current count of misses to prevent the inital notification) 
loopcounter             = int(0)	# this is an internal reference i++ counter needed for correct functioning of the script

check_rate_feeds_seed_ratio = round(check_rate_feeds_seed/check_rate, 0)


#Script starts

# Setup node instance
rpc = GrapheneAPI(rpc_host, rpc_port, rpc_username, rpc_password)

# Telegram barebones apicall 
def telegram(method, params=None):
    url = "https://api.telegram.org/bot"+telegram_token+"/"
    params = params
    r = requests.get(url+method, params = params).json()
    return r

# Telegram notifyer
def alert_witness(msg):
    # Send TELEGRAM NOTIFICATION
    payload = {"chat_id":telegram_id, "text":msg}
    m = telegram("sendMessage", payload)

# Check availability of Seednode:
def check_seednode():
  try:
    tn = telnetlib.Telnet(seed_host, seed_port,seed_timeout_check)
    print(tn.read_all())
  except Exception as e:
    tel_msg = "Your public seednode for bitshares is not responding!\n\nat *"+seed_host+"*.\n\n_"+str(e)+"_"
    alert_witness(tel_msg)


# Check how many blocks a witness has missed
def check_witness():
    global currentmisses
    global hotswitch_threshold
    status = rpc.get_witness(witness)
    missed = status['total_missed']
    print(str(loopcounter)+ ": Missed blocks = " + str(missed))
    if missed > currentmisses:
        alert_witness("You are missing blocks! Your current misses count = "+str(missed)+", which was "+str(currentmisses))
        print("You are missing blocks! Your current misses count = "+str(missed)+", which was "+str(currentmisses))
        if hotswitch == "true" and hotswitch_threshold == int(0):
            if status['signing_key'] == signing_key1:
                hotswitch_threshold = 5
                try:
                    rpc.update_witness(witness, witness_url, signing_key2, "true")
                    alert_witness("Updated to Secondary Signing Key")
                    print("Updated to Secondary Signing Key")
                except Exception as e:
                    print("Failed to update Signing Key - is your wallet unlocked? do you have enough PPY?")
                    print(e)
                    alert_witness("FAILED to Updated to Secondary Signing Key")
            else:
                hotswitch_threshold = 5
                try:
                    rpc.update_witness(witness, witness_url, signing_key1, "true")
                    alert_witness("Updated to Primary Signing Key")
                    print("Updated to Secondary Signing Key")
                except Exception as e:
                    print("Failed to update Signing Key - is your wallet unlocked? do you have enough PPY?")
                    print(e)
                    alert_witness("FAILED to Updated to Primary Signing Key")
        currentmisses = missed
    else:
        if hotswitch == "true" and hotswitch_threshold > 0:
            hotswitch_threshold -= 1
            print("Hotswitch Threshold: " + str(hotswitch_threshold))
# Main Loop
if __name__ == '__main__':
    while True:
        check_witness()
        sys.stdout.flush()
        loopcounter += 1
        if(loopcounter % check_rate_feeds_seed_ratio == 0): 
          check_seednode()
        time.sleep(check_rate)
