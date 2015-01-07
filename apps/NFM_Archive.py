#!/usr/bin/env python
##################################################
# Title: Narrow Band FM Decoder and Archiver
# Coded by: Luis Colunga (sinnet3000)
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr

class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.target_rate = target_rate = 48000
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, 2000, 30000, firdes.WIN_HAMMING, 6.76)

        self.freqs = freqs = [462.5625e6, 462.5875e6, 462.6125e6] # Channel 1, 2, 3 FRS
        
        self.freqs_names = freqs_names = ["Channel 1", "Channel 3"]

        self.capture_freq = capture_freq = ( max(freqs) + min(freqs) ) / 2

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(capture_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          

        fir_filters = []
        pwr_squelchs = []
        nbfm_rxs = []
        file_sinks = []
        float_shorts = []
        multiply_consts = []
        complex_magsqs = []
        burst_taggers = []
        iir_filters = []
        burst_settings = []
        
        count = 0
        for freq in freqs:
		fir_filters.append(filter.freq_xlating_fir_filter_ccc(int(samp_rate/target_rate), (firdes_tap), -(capture_freq-freq), samp_rate))

                file_sinks.append(blocks.tagged_file_sink(gr.sizeof_float*1, 48000))
                multiply_consts.append(blocks.multiply_const_vff((2**16, )))
                float_shorts.append(blocks.float_to_short(1, 1))
                complex_magsqs.append(blocks.complex_to_mag_squared(1))
                burst_taggers.append(blocks.burst_tagger(gr.sizeof_float))
                pwr_squelchs.append(analog.pwr_squelch_cc(-20, .001, 1, False))
                nbfm_rxs.append(analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=48000,
        	tau=75e-6,
        	max_dev=5e3,))
                iir_filters.append(filter.single_pole_iir_filter_ff(.001, 1))
                count += 1

	for tagger in burst_taggers:
		tagger.set_true_tag("burst",True)
                tagger.set_false_tag("burst",False)
 
       
        ##################################################
        # Connections
        ##################################################

        for index in range(0, len(freqs)-1):
        	self.connect((nbfm_rxs[index], 0), (burst_taggers[index], 0))
                self.connect((pwr_squelchs[index], 0), (nbfm_rxs[index], 0))
                self.connect((pwr_squelchs[index], 0), (complex_magsqs[index], 0))
                self.connect((burst_taggers[index], 0), (file_sinks[index], 0))
                self.connect((complex_magsqs[index], 0), (iir_filters[index], 0))
                self.connect((float_shorts[index], 0), (burst_taggers[index], 1)) 
                self.connect((multiply_consts[index], 0), (float_shorts[index], 0))    
                self.connect((fir_filters[index], 0), (pwr_squelchs[index], 0))    
                self.connect((self.osmosdr_source_0, 0), (fir_filters[index], 0))    
                self.connect((iir_filters[index], 0), (multiply_consts[index], 0))


if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass
