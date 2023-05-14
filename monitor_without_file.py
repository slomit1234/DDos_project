import os
import subprocess
import time
from scapy.all import *

# Define the target and attacker IP addresses
target_ip = "192.168.1.100"
attacker_ip = "192.168.1.101"

# Define the target port
target_port = 80

# Define the number of SYN packets to send in each iteration
num_packets = 10 # %% moment of truth need to change to 10K

# Define the number of iterations to perform
num_iterations = 100

# Define the commands to run the C and Python implementations
c_cmd = "sudo ./synflood_c {} {}".format(target_ip, target_port)
python_cmd = "python3 synflood_python.py {} {} {}".format(attacker_ip, target_ip, target_port)

# Run the C implementation in a subprocess
c_start_time = time.time()
c_process = subprocess.Popen(c_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the C implementation to finish
c_process.communicate()

# Record the time it took to send packets using the C implementation
c_end_time = time.time()
c_time_per_packet = (c_end_time - c_start_time) / (num_packets * num_iterations)

# Run the Python implementation in a subprocess
python_start_time = time.time()
python_process = subprocess.Popen(python_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the Python implementation to finish
python_process.communicate()

# Record the time it took to send packets using the Python implementation
python_end_time = time.time()
python_time_per_packet = (python_end_time - python_start_time) / (num_packets * num_iterations)


# Ping the target machine every 5 seconds and measure RTT
while True:
    ping_cmd = "ping -c 1 {}".format(target_ip)
    ping_start_time = time.time()
    ping_process = subprocess.Popen(ping_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output = ping_process.communicate()[0]
    ping_end_time = time.time()

    # Parse the ping output to extract the RTT
    ping_output = ping_output.decode("utf-8")
    rtt = float(ping_output.split("time=")[1].split(" ")[0])

    # Record the RTT measurement
    print("Ping RTT: {:.3f} ms".format(rtt))
    
    # Sleep for 5 seconds before pinging again
    time.sleep(5)
    
    # End the loop after the specified number of iterations
    if i == num_iterations:
        break

# Print the results
print("C implementation: {:.6f} seconds per packet".format(c_time_per_packet))
print("Python implementation: {:.6f} seconds per packet".format(python_time_per_packet))
