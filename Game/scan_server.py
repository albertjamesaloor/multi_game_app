import socket
import threading

# Shared variable to store the found server IP
found_server_ip = None
lock = threading.Lock()  # Ensure thread-safe access to shared variables

def get_local_ip():
    """ Get the local IP address of the client machine. """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def scan_ip(ip, port):
    """ Helper function to scan a single IP for an open port. """
    global found_server_ip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.1)
        if s.connect_ex((ip, port)) == 0:
            with lock:
                if not found_server_ip:  # Only set if no server is found yet
                    found_server_ip = ip
                    print(f"Server found: {found_server_ip}:{port}")

def scan_network_and_check_port(port):
    """ Scan the local network concurrently for active devices on a specified port. """
    global found_server_ip
    local_ip = get_local_ip()
    ip_parts = local_ip.split('.')
    base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."

    found_server_ip = None  # Reset the found server IP

    threads = []
    for i in range(1, 255):
        ip = base_ip + str(i)
        t = threading.Thread(target=scan_ip, args=(ip, port))
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    if found_server_ip:
        print(f"Found server at {found_server_ip}:{port}")
    else:
        print("No servers found listening on the specified port.")

    return found_server_ip
