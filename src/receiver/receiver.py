#!/usr/bin/env python



from gnuradio import gr, gru, modulation_utils
from gnuradio import usrp
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser

import random
import time
import struct
import sys
import os

sys.path.append("../misc/")

# from current dir
from transmit_path import transmit_path
from receive_path import receive_path
from receiverMAC import receiverMAC
import fusb_options




# /////////////////////////////////////////////////////////////////////////////
#                             the flow graph
# /////////////////////////////////////////////////////////////////////////////


class my_top_block(gr.top_block):

    def __init__(self, mod_class, demod_class,
                 rx_callback, options):

        gr.top_block.__init__(self)
        self.txpath = transmit_path(mod_class, options)
        self.rxpath = receive_path(demod_class, rx_callback, options)
        self.connect(self.txpath);
        self.connect(self.rxpath);
    
    def send_pkt(self, payload='', eof=False):
        return self.txpath.send_pkt(payload, eof)

    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()



# /////////////////////////////////////////////////////////////////////////////
#                                   main
# /////////////////////////////////////////////////////////////////////////////

global n_rcvd, n_right,data_rcvd,last_packet_time,pack_delay_f, pack_drop_pat,pack_delay_u_f,last_packet_time_u

def main():
    mac_addr = '00:00:00:00:00:01'  
    mac = receiverMAC(mac_addr,'simpsonrecvd.mp4')      
            
    def send_pkt(payload):
        tb.send_pkt(payload)

    mods = modulation_utils.type_1_mods()
    demods = modulation_utils.type_1_demods()

    parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")

    parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(),
                      default='gmsk',
                      help="Select modulation from: %s [default=%%default]"
                            % (', '.join(mods.keys()),))

    parser.add_option("-v","--verbose", action="store_true", default=False)
    expert_grp.add_option("-c", "--carrier-threshold", type="eng_float", default=30,
                          help="set carrier detect threshold (dB) [default=%default]")
    expert_grp.add_option("","--tun-device-filename", default="/dev/net/tun",
                          help="path to tun device file [default=%default]")
    parser.add_option("","--filename", default=None,
                      help="use file for packet contents")

    transmit_path.add_options(parser, expert_grp)
    receive_path.add_options(parser, expert_grp)

    for mod in mods.values():
        mod.add_options(expert_grp)

    for demod in demods.values():
        demod.add_options(expert_grp)

    fusb_options.add_options(expert_grp)

    (options, args) = parser.parse_args ()
    if len(args) != 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.rx_freq is None or options.tx_freq is None:
        sys.stderr.write("You must specify -f FREQ or --freq FREQ\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if options.filename is not None:
        file_sink = open(options.filename, 'w')


    # Attempt to enable realtime scheduling
    r = gr.enable_realtime_scheduling()
    if r == gr.RT_OK:
        realtime = True
    else:
        realtime = False
        print "Note: failed to enable realtime scheduling"


    # If the user hasn't set the fusb_* parameters on the command line,
    # pick some values that will reduce latency.

    if options.fusb_block_size == 0 and options.fusb_nblocks == 0:
        if realtime:                        # be more aggressive
            options.fusb_block_size = gr.prefs().get_long('fusb', 'rt_block_size', 1024)
            options.fusb_nblocks    = gr.prefs().get_long('fusb', 'rt_nblocks', 16)
        else:
            options.fusb_block_size = gr.prefs().get_long('fusb', 'block_size', 4096)
            options.fusb_nblocks    = gr.prefs().get_long('fusb', 'nblocks', 16)
    

    # build the graph (PHY)
    tb = my_top_block(mods[options.modulation],
                      demods[options.modulation],
                      mac.rx_callback,
                      options)
    
    mac.set_tb(tb)

    #mac.set_top_block(tb)    # give the MAC a handle for the PHY

    if tb.txpath.bitrate() != tb.rxpath.bitrate():
        print "WARNING: Transmit bitrate = %sb/sec, Receive bitrate = %sb/sec" % (
            eng_notation.num_to_str(tb.txpath.bitrate()),
            eng_notation.num_to_str(tb.rxpath.bitrate()))
             
    print "modulation:     %s"   % (options.modulation,)
    print "freq:           %s"      % (eng_notation.num_to_str(options.tx_freq))
    print "bitrate:        %sb/sec" % (eng_notation.num_to_str(tb.txpath.bitrate()),)
    print "samples/symbol: %3d" % (tb.txpath.samples_per_symbol(),)


    tb.rxpath.set_carrier_threshold(options.carrier_threshold)
    print "Carrier sense threshold:", options.carrier_threshold, "dB"
    

    tb.start()    # Start executing the flow graph (runs in separate threads)
    tb.wait()     # wait for it to finish
   
                



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
