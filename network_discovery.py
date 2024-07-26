from scapy.all import ARP, Ether, srp
import socket
from datetime import datetime

# Manually specify the IP range
target_ip = "192.168.1.1/24"  # Replace with your actual IP range

# Create an ARP request packet
arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether/arp

print("Sending ARP requests...")

# Send the packet and receive the response
result = srp(packet, timeout=10, verbose=1)[0]

# Check if we received any responses
if not result:
    print("No devices found. Try increasing the timeout or check your network settings.")
else:
    print("Processing responses...")

# Parse the response
devices = []
for sent, received in result:
    # Try to resolve the hostname
    try:
        hostname = socket.gethostbyaddr(received.psrc)[0]
    except socket.herror:
        hostname = "Unknown"
    
    devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})

# Generate a timestamp for the filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"C:\\temp\\network_discovery_{timestamp}.txt"

# Save the discovered devices to a file
with open(filename, "w") as file:
    file.write("Discovered devices on the network:\n")
    for device in devices:
        file.write(f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}\n")

print(f"Results saved to {filename}")

# Print the discovered devices
print("Discovered devices on the network:")
for device in devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}")

# If no devices are found, inform the user
if not devices:
    print("No devices found. Ensure you are connected to the correct network and have the necessary permissions.")
