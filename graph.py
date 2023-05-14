import matplotlib.pyplot as plt

# read data from files
with open("syns_results_c.txt") as f:
    lines = f.readlines()
    c_times = [float(line.split()[1]) for line in lines]

with open("syns_results_p.txt") as f:
    lines = f.readlines()
    p_times = [float(line.split()[1]) for line in lines]

# plot data
fig, ax = plt.subplots()
ax.hist(c_times, bins=100, alpha=0.5, label='C')
ax.hist(p_times, bins=100, alpha=0.5, label='Python')
ax.set_xscale('log')
ax.set_xlabel('Time to send a packet (seconds)')
ax.set_ylabel('Number of packets sent')
ax.legend()
plt.show()

# print statistics
print("C implementation:")
print("Average time to send a packet: {:.6f} seconds".format(sum(c_times)/len(c_times)))
print("Standard deviation: {:.6f} seconds".format(statistics.stdev(c_times)))
print("")

print("Python implementation:")
print("Average time to send a packet: {:.6f} seconds".format(sum(p_times)/len(p_times)))
print("Standard deviation: {:.6f} seconds".format(statistics.stdev(p_times)))

plt.savefig('ddos_attack_histogram.png')
