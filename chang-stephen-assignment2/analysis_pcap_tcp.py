import argparse
import socket
import dpkt

SENDER_IP = "130.245.145.12"
RECEIVER_IP = "128.208.2.198"



def analyze_pcap(filename):
    flows = {}
    
    with open(filename, "rb") as file:
        pcap = dpkt.pcap.Reader(file)

        for timestamp, packet_bytes in pcap:
            # decode the ethernet frame

            ethernet = dpkt.ethernet.Ethernet(packet_bytes)

            # skip packets that do not contain IPv4
            if not isinstance(ethernet.data, dpkt.ip.IP):
                continue

            ip = ethernet.data

            # skip IPv4 packets that do not contain TCP
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue

            tcp = ip.data

            # convert binary IPv4 addresses to readable strings
            source_ip = socket.inet_ntoa(ip.src)
            destination_ip = socket.inet_ntoa(ip.dst)
            
            # determine the packet's direction.
            
            # if the packet is from the sender to the receiver
            if (source_ip == SENDER_IP and destination_ip == RECEIVER_IP):
                from_sender = True

                flow_key = (
                    tcp.sport,
                    source_ip,
                    tcp.dport,
                    destination_ip
                )

            # if the packet is from the receiver to the sender
            elif (source_ip == RECEIVER_IP and destination_ip == SENDER_IP):
                from_sender = False

                # reverse the fields
                flow_key = (
                    tcp.dport,
                    destination_ip,
                    tcp.sport,
                    source_ip
                )

            else:
                continue

            # check whether the SYN and ACK flags are set
            is_syn = bool(tcp.flags & dpkt.tcp.TH_SYN)
            is_ack = bool(tcp.flags & dpkt.tcp.TH_ACK)

            # a sender SYN without ACK initiates a flow
            if from_sender and is_syn and not is_ack:
                if flow_key not in flows:
                    flows[flow_key] = {
                        "packets": [],
                        "fin_seen": False
                    }

            # ignore packets whose initiating SYN was not captured
            if flow_key not in flows:
                continue

            # save this packet in its flow
            flows[flow_key]["packets"].append({
                "timestamp": timestamp,
                "from_sender": from_sender,
                "tcp": tcp
            })

            # record whether a FIN has appeared.
            if tcp.flags & dpkt.tcp.TH_FIN:
                flows[flow_key]["fin_seen"] = True

    # print results after reading the entire capture
    print(f"Number of TCP flows: {len(flows)}")

    for flow_number, (flow_key, flow) in enumerate(
        flows.items(), start=1
    ):
        print(f"\nFlow {flow_number}:")
        print(f"  Tuple: {flow_key}")
        print(f"  Packets captured: {len(flow['packets'])}")
        print(f"  FIN observed: {flow['fin_seen']}")

    return flows    
            
def main():
    parser = argparse.ArgumentParser(
        description="Analyze TCP flows in a PCAP file"
    )

    parser.add_argument("pcap", help="Path to the PCAP file")
    args = parser.parse_args()

    analyze_pcap(args.pcap)

if __name__ == "__main__":
    main()