import os
import subprocess
import time
from scapy.all import *


num_iterations=10

target_ip = "10.12.2.45"
target_port = 80

# Ping the target machine every 5 seconds and measure RTT
i = 1
c_rtt_sum = 0.0
p_rtt_sum = 0.0
with open("pings_results_c.txt", "w") as c_file, open("pings_results_p.txt", "w") as p_file:
    while True:
        ping_cmd = "ping {}".format(target_ip)
        ping_start_time = time.time()
        ping_process = subprocess.Popen(ping_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_output = ping_process.communicate()[0]
        ping_end_time = time.time()

        # Parse the ping output to extract the RTT
        ping_output = ping_output.decode("utf-8")
        frtt = ping_output.split("time ")
        frtt = frtt[1]
        frtt = frtt.split("ms")
        rtt = float(frtt[0])

        # Record the RTT measurement to the appropriate file
        try:
            if(sys.argv[1] == "c"): 
                c_file.write("{}\n".format(rtt))
                c_rtt_sum += rtt
            else:
                p_file.write("{}\n".format(rtt))
                p_rtt_sum += rtt
        except Exception as e:
            print("no argumets provided. usage python3 monitor.py p/c")
            print (e)
            exit
        # Sleep for 5 seconds before pinging again
        time.sleep(5)
       
        # End the loop after the specified number of iterations
        if i == num_iterations:
            break
       
        i += 1

# Calculate and print the average RTT for each implementation
try:
    if(sys.argv[1] == "c"): 
        c_avg_rtt = c_rtt_sum / num_iterations
        c_file.write("Average RTT = {:.3f} ms".format(c_avg_rtt))
        print("C implementation: Average RTT = {:.3f} ms".format(c_avg_rtt))
    else:
        p_avg_rtt = p_rtt_sum / num_iterations
        p_file.write("{}\n".format(rtt))
        print("=Average RTT = {:.3f} ms".format(p_avg_rtt))
except:
        print("no argumets provided. usage python3 monitor.py p/c")
        exit



