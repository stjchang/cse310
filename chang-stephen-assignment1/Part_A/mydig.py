import sys
import dns.message
from datetime import datetime

import dns.query
import dns.rdatatype
import dns.flags
import dns.exception
import dns.rcode
import time

# IPv4 addresses of the DNS root servers
ROOT_SERVERS = [
    "198.41.0.4",       # a.root-servers.net
    "170.247.170.2",    # b.root-servers.net
    "192.33.4.12",      # c.root-servers.net
    "199.7.91.13",      # d.root-servers.net
    "192.203.230.10",   # e.root-servers.net
    "192.5.5.241",      # f.root-servers.net
    "192.112.36.4",     # g.root-servers.net
    "198.97.190.53",    # h.root-servers.net
    "192.36.148.17",    # i.root-servers.net
    "192.58.128.30",    # j.root-servers.net
    "193.0.14.129",     # k.root-servers.net
    "199.7.83.42",      # l.root-servers.net
    "202.12.27.33"      # m.root-servers.net
]

MAX_DEPTH = 20
TIMEOUT = 5


# Function to query a DNS server for a given domain
def query_dns_server(domain, server):
    query = dns.message.make_query(domain, "A")

    # gracefully handle timeouts and DNS exceptions
    try:
        response = dns.query.udp(
            query,
            server,
            timeout=TIMEOUT
        )
    except dns.exception.Timeout:
        raise RuntimeError(
            f"DNS server {server} timed out."
        )
    except dns.exception.DNSException as e:
        raise RuntimeError(
            f"DNS query failed for {server}: {e}"
        )

    return response


# Function to get the nameservers from the response
def get_nameservers(response):
    nameservers = []

    for section in response.authority:
        for record in section:
            if record.rdtype == dns.rdatatype.NS:
                nameservers.append(
                    str(record.target)
                )

    return nameservers


# 
# Function to get the IP address of the nameservers from the response
def get_nameservers_ip(response):
    nameservers = get_nameservers(response)
    server_ips = []

    for section in response.additional:
        if section.rdtype != dns.rdatatype.A:
            continue

        section_name = str(section.name)

        for nameserver in nameservers:
            if section_name == nameserver:
                for record in section:
                    server_ips.append(
                        str(record.address)
                    )

    return server_ips

# Function to get the A records from the response
def get_a_records(response, domain):
    addresses = []

    for section in response.answer:
        if section.rdtype != dns.rdatatype.A:
            continue

        if str(section.name).rstrip(".") != domain.rstrip("."):
            continue

        for record in section:
            addresses.append(
                str(record.address)
            )

    return addresses


# Function to get a CNAME target from the response
def get_cname(response, domain):
    for section in response.answer:
        if section.rdtype != dns.rdatatype.CNAME:
            continue

        if str(section.name).rstrip(".") != domain.rstrip("."):
            continue

        return str(section[0].target).rstrip(".")

    return None

# Function to resolve the domain (taken from main())
def resolve(domain):
    current_servers = ROOT_SERVERS

    for depth in range(MAX_DEPTH):

        response = None

        # Try each available server
        for server in current_servers:
            try:
                candidate = query_dns_server(
                    domain,
                    server
                )

                print(
                    f"Depth {depth}: "
                    f"{domain} -> {server}"
                )

            except RuntimeError:
                continue

            if candidate.rcode() == dns.rcode.NXDOMAIN:
                raise RuntimeError(
                    f"Domain does not exist: {domain}"
                )

            if candidate.rcode() != dns.rcode.NOERROR:
                continue

            response = candidate

            # Check for A record
            a_records = get_a_records(response, domain)

            if a_records:
                print(f"FOUND A RECORD: {a_records}")
                return response

            # Check for CNAME and resolve the alias
            cname = get_cname(response, domain)

            if cname:
                print(f"FOUND CNAME: {domain} -> {cname}")
                return resolve(cname)

            break

        # If no server gave us a usable response
        if response is None:
            raise RuntimeError(
                "All available DNS servers failed."
            )

        # We got a referral, so find the next servers
        next_servers = get_next_servers(response)

        if not next_servers:
            raise RuntimeError(
                "Could not find IP address for any nameserver."
            )

        current_servers = next_servers

    raise RuntimeError(
        "Maximum DNS resolution depth exceeded."
    )
    
# Function to get the next servers to query
def get_next_servers(response):
    # First, look for glue records
    server_ips = get_nameservers_ip(response)

    if server_ips:
        return server_ips

    # No glue was provided.
    # Get the nameserver hostnames.
    nameservers = get_nameservers(response)

    if not nameservers:
        return []

    # Resolve one nameserver hostname to an IP address.
    for nameserver in nameservers:
        print(
            f"Resolving nameserver hostname: {nameserver}"
        )

        try:
            nameserver_response = resolve(
                nameserver.rstrip(".")
            )

            addresses = get_a_records(
                nameserver_response,
                nameserver.rstrip(".")
            )

            if addresses:
                return addresses

        except RuntimeError:
            continue

    return []

def main():
    if len(sys.argv) != 2:
        print("Usage: python mydig.py <domain>")
        sys.exit(1)

    domain = sys.argv[1].rstrip(".")
    
    print(f"Resolving: {domain}")

    start_time = time.time()

    try:
        response = resolve(domain)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    elapsed_time = (time.time() - start_time) * 1000

    # formatting purposes to match assignments output
    print("QUESTION SECTION:\n")
    qname = domain.rstrip(".") + "."
    print(f"{qname:<32}IN      A")

    print("\nANSWER SECTION:\n")

    # Print the answer section with the correct format
    for section in response.answer:
        name = str(section.name)
        rdtype = dns.rdatatype.to_text(section.rdtype)

        for record in section:
            print(
                f"{name:<24}"
                f"{section.ttl:<7}"
                f"IN      "
                f"{rdtype:<8}"
                f"{record}"
            )
        
    print(f"\nQuery time: {elapsed_time:.0f} ms")
    print(f"WHEN: {datetime.now()}")
            
if __name__ == "__main__":
    main()