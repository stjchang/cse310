import sys

if len(sys.argv) != 2:
    print("Usage: python mydig.py <domain>")
    sys.exit(1)
    
domain = sys.argv[1]

print(f"Resolving: {domain}")