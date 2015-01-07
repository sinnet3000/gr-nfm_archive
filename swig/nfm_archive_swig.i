/* -*- c++ -*- */

#define NFM_ARCHIVE_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "nfm_archive_swig_doc.i"

%{
#include "nfm_archive/name_timestamp_file_sink.h"
%}


%include "nfm_archive/name_timestamp_file_sink.h"
GR_SWIG_BLOCK_MAGIC2(nfm_archive, name_timestamp_file_sink);
