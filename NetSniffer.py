import socket
import ipaddress

def discover_hosts(network):
    """Discover active hosts in the given network."""
    active_hosts = []
    for ip in ipaddress.IPv4Network(network, strict=False):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)  # Timeout for host discovery
            result = sock.connect_ex((str(ip), 80))  # Ping port 80 (HTTP)
            if result == 0:
                active_hosts.append(str(ip))
            sock.close()
        except socket.error:
            pass
    return active_hosts

def scan_ports(host, port_range):
    """Scan ports on a single host."""
    open_ports = []
    for port in port_range:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except socket.error:
            pass
    return open_ports

def main():
    network = input("Enter the network (e.g., 192.168.1.0/24): ")
    port_range = range(1, 1025)  # Define the range of ports to scan (1-1024)
    
    print(f"Scanning network {network} for active hosts...")
    hosts = discover_hosts(network)
    
    if not hosts:
        print("No active hosts found.")
        return
    
    print(f"Discovered hosts: {hosts}")
    
    for host in hosts:
        print(f"\nScanning {host} for open ports...")
        open_ports = scan_ports(host, port_range)
        if open_ports:
            print(f"Open ports on {host}: {open_ports}")
        else:
            print(f"No open ports found on {host}.")

if __name__ == "__main__":
    main()
