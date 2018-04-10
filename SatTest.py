import time
import os
import queue
from houston_utils import *

# SatTest class

class SatTest():
    def __init__(self, tx_queue):
        self.new = [] # commands that have not yet been sent out to the OBC
        self.pending = [] # commands waiting on valid response or timeout
        self.acknowledged = [] # commands that have been acknowledged properly
        self.errored = [] # commands that timed out
        self.tx_queue = tx_queue # handle for the serial transmit queue
        self.epoch = time.time
        self.raw_data = [] # raw stuff coming in from the sat
        self.zero_epoch()
    
    def check_response(self, telem, rx_time):
        # print ("SatTest rx: ", self.sat_epoch_at_unix(rx_time))
        # in the pending list, see if any expected responses match the telemetry
        # if yes, put the one with the lowest epoch + timeout

        # print("Telem to match: ", telem)
        telem = telem.strip()
        # print("Pending: ", self.pending[0].expect, telem)
        matches = [cmd for cmd in self.pending[:] if str(cmd.expect) == telem]  # list of all elements with .n==30
        # print("MATCH: ", [match.cmdid for match in matches]) 
        
        if len(matches) > 0:
            # sort matches and stuff
            for match in matches:
                print('Command #', match.cmdid, match.cmd, 'acknowledged at :', self.sat_epoch_at_unix(rx_time))
                i = index_of_cmdid(self.pending, match.cmdid)
                self.acknowledged.append(match)
                del self.pending[i]

            
        # time.sleep(0.3)

    def zero_epoch(self):
        self.unix_at_0 = time.time()

    def sat_epoch(self):
        return time.time() - self.unix_at_0

    def sat_epoch_at_unix(self, unix):
        return unix - self.unix_at_0 

    def add_schedule(self, data_in):
        # add a list of command objects
        self.new = data_in

    def uplink(self, cmdid, dt):
        print("CMDID_in", str(cmdid))
        i = index_of_cmdid(self.new, cmdid)
        command = self.new[i]
        
        # rm from new list, put on pending list
        del self.new[i]
        self.pending.append(command)
        print("Command: ", command.cmd_dict(), str(i))
        print("SCHEDULED COMMAND SEND: " + command.cmd)
        self.tx_queue.append(command.cmd)
        return

    def process_telem(self, telem):
        receive_time = self.sat_epoch()

        # telemetry comes back as several things:
        #   - orphan messages from testing
        #   - standard telem sets
        #   - responses to immediate commands
        #   - responses to scheduled commands are stored and can be requested, since we won't always be in contact 


        # Standard telem:
        # - parse telem packet and update views. This is things like epoch, battery state, etc.
        # - every time we get one, update the HUD. Have each set available as an expandable row in a list for examination
        # - if standard telem said there were errors in the queue, we would issue a command to retrieve them 
        # - for real mission: if there were errors, automatically request them 

        # Responses to command:
        # - search pending list for any commands with timeout >= receive time
        # - sort that by ID 
        # - search that list of commands for expected response matching this one
        # - if multiple matches, go with lowest ID. put the matched command on the acknowledged list

        # Command handling on sat: 
        # - if it's an immediate command, send out the response on radio/uart right away (this is for mission and testing)
        # - if it's a sat-scheduled command, log the response so we can pull it down later 
        # - if you want to do something like read a file, you could schedule a read command of that file at the time of next downlink

        # Ottawa test:
        # put in/out of different modes, observe that the telem is reflecting that
        #       - ex: safe mode, a bunch of tasks should be suspended. we can check that from a get tasks command
        #       - ex: low power mode, check that current has dropped
        #       - these things could be different modules that we load up to create a full test, then we run the whole thing
        # schedule commands for the future (such as a chime pass), verify that they execute
        # check that telem is nominal


    def command_timeout(self, cmdid, dt): # anything called by Clock should have dt argument
        """ Called by Kivy at timeout of command. 
        - if command is still on pending, it hasn't received a good response, so time it out
        """

        print('Checking timeout of command ID: ', cmdid)
        i = index_of_cmdid(self.pending[:], cmdid)
        if i != -1: # command is in pending and therefore timed out
            self.errored.append(self.pending[i])
            del self.pending[i]
            print("Command ID ", cmdid, " placed in errored.")
        return
        # pass
        # this will be called at the timeout time for a command by kivy clock
        # search the pending list for the command ID
        #   - if not there, no worries we've processed the command before timeout
        #   - if there, pull off and add to failed command list