/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_NFM_ARCHIVE_NAME_TIMESTAMP_FILE_SINK_IMPL_H
#define INCLUDED_NFM_ARCHIVE_NAME_TIMESTAMP_FILE_SINK_IMPL_H

#include <nfm_archive/name_timestamp_file_sink.h>
#include <cstdio>  // for FILE

namespace gr {
  namespace nfm_archive {

    class name_timestamp_file_sink_impl : public name_timestamp_file_sink
    {
    private:
      enum {
	NOT_IN_BURST = 0,
	IN_BURST
      };

      size_t   d_itemsize;
      int      d_state;
      FILE    *d_handle;
      int      d_n;
      double   d_sample_rate;
      uint64_t d_last_N;
      double   d_timeval;
      const char *d_channel_name;
      char d_timestamp[25];

    public:
      name_timestamp_file_sink_impl(size_t itemsize, double samp_rate, const char *channel_name);
      ~name_timestamp_file_sink_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace nfm_archive
} // namespace gr

#endif /* INCLUDED_NFM_ARCHIVE_NAME_TIMESTAMP_FILE_SINK_IMPL_H */

