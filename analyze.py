#!/usr/bin/env python

from optparse import OptionParser

def write_to_file(data, filename):
  f = open(filename, 'w+')
  for time in sorted(data):
    f.write(str(time) + "\t" + str(data[time]) + "\n")

def get_latency(recieved, sent):
  latency = {}
  for seq_num in recieved:
    time = str(float(recieved[seq_num]) - float(sent[seq_num]))
    #print time
    if float(time) < 0:
      print float(recieved[seq_num]), float(sent[seq_num])
    #print sent[seq_num] + '\t' + recieved[seq_num] + '\t' + time
    latency[int(seq_num)] = time
  return latency

def normalize_seq_num(recieved):
  acc = {}
  for seq_num in recieved:
    acc[float(recieved[seq_num])] = int(seq_num) 
  return acc

def normalize_time(throughput):
  normalized = {}
  for time in throughput:
    normalized[float(time)/10] = throughput[time]
  return normalized

def parse(out_file):
  drops_from_1_to_2 = 0
  bytes_received = 0
  current_bytes_received = 0
  start_time = None
  end_time = None
  interval_size = .1
  recieved_packets = {}
  dropped_packets = {}
  sequence_numbers_sent = {}
  sequence_numbers_received = {}
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
    if data['event'] == 'd' and data['packet_type'] == 'tcp':
      drops_from_1_to_2 += 1
      dropped_packets[data['time']] = 3#data['packet_size']
    elif data['event'] == '+' and data['packet_type'] == 'tcp' and data['from_node'] == '0':
      sequence_numbers_sent[data['seq_num']] = data['time']
    elif data['event'] == 'r' and data['packet_type'] == 'tcp':
      sequence_numbers_received[data['seq_num']] = data['time']
      current_bytes_received = int(data['packet_size'])
      bytes_received += current_bytes_received
      time = float(data['time'])
      seconds = int(str(time).split(".")[0])
      time_interval = int(data['time'].split('.')[1][0]) + (10 * seconds)
      if time_interval in recieved_packets:
        recieved_packets[time_interval] += current_bytes_received
      else:
        recieved_packets[time_interval] = current_bytes_received
      #print time_interval
      #print str(time) + "\t" + str(time_interval) 
      end_time = data['time']
    #elif data['event'] == 'r' and data['packet_type'] == 'ack':
    #  sequence_numbers_received[data['seq_num']] = data['time']

  #print recieved_packets
  print sequence_numbers_received
  write_to_file(normalize_seq_num(sequence_numbers_received), "received1.dat")
  write_to_file(normalize_time(recieved_packets), "throuput3.dat")
  write_to_file(dropped_packets, "dropped.dat")
  write_to_file(get_latency(sequence_numbers_received, sequence_numbers_sent), "latency.dat")
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
