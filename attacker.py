from scapy.all import *
import time

# define target IP and port
target_ip = "10.12.15.255"
target_port = 80

# create SYN packet
syn_pkt = IP(dst=target_ip)/TCP(sport=RandShort(), dport=target_port, flags="S")
total_time = 0
# send packets in loop, %% change j to 10K
with open("syns_results_p.txt", "w") as f:
    for i in range(100):
        for j in range(100):
            start = time.time()
            send(syn_pkt, verbose=0)
            end = time.time()
            total_time = total_time +(end-start)
            f.write(f"{i*100 + (j+1)}\t{end - start}\n")
            print(f"{i*100 + (j+1)}\t{end - start}\n")
    
    
    avg_time = total_time / 10000 #%%change to 1m
    f.write(f"Total time: {total_time}\nAverage time per packet: {avg_time}")
    print(f"Total time: {total_time}\nAverage time per packet: {avg_time}")
    f.close()