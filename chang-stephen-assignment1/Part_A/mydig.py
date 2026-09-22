import sys
import dns.message
import dns.query
import dns.rdatatype

ROOT_SERVERS = [
    "198.41.0.4"
]

# Function to query a DNS server for a given domain
def query_dns_server(domain, server):
    query = dns.message.make_query(domain, "A")

    response = dns.query.udp(
        query,
        server,
        timeout=5
    )

    return response


# Function to get the nameserver from the response
def get_nameserver(response):
    for section in response.authority:
        for record in section:
            if record.rdtype == dns.rdatatype.NS:
                return str(record.target)

    return None

# 
# Function to get the IP address of the nameserver from the response
def get_nameserver_ip(response, nameserver):
    for section in response.additional:
        for record in section:
            if record.rdtype == dns.rdatatype.A:
                if str(record.name) == nameserver:
                    return str(record.address)

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python mydig.py <domain>")
        sys.exit(1)

    domain = sys.argv[1].rstrip(".")

    print(f"Resolving: {domain}")

    root_server = ROOT_SERVERS[0]

    print(f"Starting DNS server: {root_server}")

    response = query_dns_server(domain, root_server)
    
    nameserver = get_nameserver(response)
    
    if nameserver is None:
        print("Error: Could not find a nameserver in the response.")
        sys.exit(1)
        
    
    print(f"\nNext nameserver: {nameserver}")


    nameserver_ip = get_nameserver_ip(response, nameserver)

    if nameserver_ip is None:
        print("Error: Could not find the IP address of the nameserver in the response.")
        sys.exit(1)

    print(f"Next nameserver IP: {nameserver_ip}")
    
if __name__ == "__main__":
    main()