#!/usr/bin/env python

from optparse import OptionParser

def write_to_file(data):
  f = open('data.dat', 'w+')
  for time in data:
    f.write(str(time) + "\t" + str(data[time]) + "\n")

def parse(out_file):
  drops_from_1_to_2 = 0
  bytes_received = 0
  current_bytes_received = 0
  start_time = None
  end_time = None
  interval_size = .1
  recieved_packets = {}
  for line in open(out_file):
    #print line
    split =  line.replace('\n', '').split(' ')
    #print split
    data = {}
    data['event'] = split[0]
    data['time'] = split[1]
    data['from_node'] = split[2]
    data['to_node'] = split[3]
    data['packet_type'] = split[4]
    data['packet_size'] = split[5]
    data['flags'] = split[6]
    data['fid'] = split[7]
    data['src_addr'] = split[8]
    data['dest_addr'] = split[9]
    data['seq_num'] =split[10]
    data['packet_id'] = split[11]
    if data['event'] == 'd' and data['from_node'] == '1' and data['to_node'] == '2':
      drops_from_1_to_2 += 1
    elif data['event'] == 'r' and data['from_node'] == '1' and data['to_node'] == '2' and data['packet_type'] == 'tcp':
      current_bytes_received = int(data['packet_size'])
      bytes_received += current_bytes_received
      time = float(data['time'])
      recieved_packets[time] = current_bytes_received
      #print time_interval
      end_time = data['time']

  print recieved_packets
  write_to_file(recieved_packets)
  print "Received " + str(bytes_received) + " bytes"
  #print "Throuput is " + str((bytes_received/(float(end_time)-float(start_time)))) + " bytes/second"
  print "Dropped " + str(drops_from_1_to_2) + " packets"


# parses the command line args
parser = OptionParser()
parser.add_option("-o", "--output", dest="out_file",
help="The destination of the output file to parse", default=None)
(options, args) = parser.parse_args()

if options.out_file == None:
  print "Need to have an ouput file"
  exit()
else:
  parse(options.out_file)
