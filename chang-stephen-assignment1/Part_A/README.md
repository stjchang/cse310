# Part A: mydig

`mydig.py` is an iterative DNS resolver. It starts at a root server, follows referrals to TLD and authoritative servers, resolves nameserver hostnames when glue is missing, and follows CNAME aliases until it finds an A record.

## External libraries

- **dnspython** (`dns.message`, `dns.query`, `dns.rdatatype`, `dns.exception`, `dns.rcode`): build DNS queries, send UDP queries, and parse answers, authority, and additional sections.

Install it with pip:

```
python -m pip install dnspython
```

If `import dns` fails, you are using a different Python than the one that has dnspython. Use that same `python` to run the program.

Standard library modules used: `sys`, `datetime`, `time`.

## How to run

From this directory (`Part_A`):

```
python mydig.py <domain>
```

Examples:

```
python mydig.py www.cnn.com
python mydig.py google.com
```

## Expected output

While resolving, the program prints each hop and whether it found a CNAME or A record. After that it prints the assignment-style sections.

TTL, IP addresses, query time, and the timestamp change from run to run. The sections and field order stay the same.

### Example: `python mydig.py www.cnn.com`

```
Resolving: www.cnn.com
Depth 0: www.cnn.com -> 198.41.0.4
Depth 1: www.cnn.com -> 192.41.162.30
Depth 2: www.cnn.com -> 205.251.193.122
FOUND CNAME: www.cnn.com -> cnn-tls.map.fastly.net
Depth 0: cnn-tls.map.fastly.net -> 198.41.0.4
Depth 1: cnn-tls.map.fastly.net -> 192.55.83.30
Depth 2: cnn-tls.map.fastly.net -> 23.235.32.32
FOUND A RECORD: ['151.101.35.5']
QUESTION SECTION:

www.cnn.com.                    IN      A

ANSWER SECTION:

cnn-tls.map.fastly.net. 60     IN      A       151.101.35.5

Query time: 150 ms
WHEN: 2026-09-22 11:39:02.323484
```

### Example: `python mydig.py google.com`

```
Resolving: google.com
Depth 0: google.com -> 198.41.0.4
Depth 1: google.com -> 192.41.162.30
Depth 2: google.com -> 216.239.34.10
FOUND A RECORD: ['142.250.217.14']
QUESTION SECTION:

google.com.                     IN      A

ANSWER SECTION:

google.com.             300    IN      A       142.250.217.14

Query time: 38 ms
WHEN: 2026-09-22 11:39:02.447583
```

