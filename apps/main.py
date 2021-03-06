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
import nfm_archive

class my_top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.target_rate = target_rate = 8000
        self.channel_bandwidth = channel_bandwidth = 8000
        self.firdes_tap = firdes_tap = firdes.low_pass(1, samp_rate, channel_bandwidth, 2000, firdes.WIN_HAMMING, 6.76)

        self.freqs = freqs = [460.35000e6, 460.45000e6, 460.22500e6, 460.40000e6, 460.50000e6, 460.17500e6, 460.30000e6, 460.12500e6, 460.07500e6, 460.25000e6, 460.05000e6, 460.15000e6, 460.27500e6 ] 

        self.freqs_names = freqs_names = ["BPD CW 1", "BPD A1-A7", "BPD B2-B3", "BPD E5-13-18", "BPD D4-D14", "BPD C6-C11", "BPD TA 7", "BPD List 8", "BPD TA 9", "BPD CMD 10", "BPD SOps 12", "BPD Detc 13", "BPD IA 14" ]

        self.squelch_settings = squelch_settings = [-75] * 13

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
        self.osmosdr_source_0.set_gain(7, 0)
        self.osmosdr_source_0.set_if_gain(10, 0)
        self.osmosdr_source_0.set_bb_gain(7, 0)
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

        for freq in freqs:
		fir_filters.append(filter.freq_xlating_fir_filter_ccc(int(samp_rate/target_rate), (firdes_tap), -(capture_freq-freq), samp_rate))

                file_sinks.append(nfm_archive.name_timestamp_file_sink(gr.sizeof_float*1, channel_bandwidth, freqs_names[freqs.index(freq)]))
                multiply_consts.append(blocks.multiply_const_vff((2**16, )))
                float_shorts.append(blocks.float_to_short(1, 1))
                complex_magsqs.append(blocks.complex_to_mag_squared(1))
                burst_taggers.append(blocks.burst_tagger(gr.sizeof_float))
                pwr_squelchs.append(analog.pwr_squelch_cc(squelch_settings[freqs.index(freq)], .001, 0, False))
                nbfm_rxs.append(analog.nbfm_rx(
        	audio_rate=8000,
        	quad_rate=8000,
        	tau=75e-6,
        	max_dev=5e3,))
                iir_filters.append(filter.single_pole_iir_filter_ff(.001, 1))

	for tagger in burst_taggers:
		tagger.set_true_tag("burst",True)
                tagger.set_false_tag("burst",False)
 
       
        ##################################################
        # Connections
        ##################################################

        for index in range(0, len(freqs)):
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
