#!/usr/bin/python3

import socket
import sys
import time
import threading
from queue import Queue

# Usage instructions
usage = "python3 portscanner.py TARGET START_PORT END_PORT"

# Print banner
print("*" * 70)
print("Python Port Scanner")
print("*" * 70)

# Start time
start_time = time.time()

# Command-line argument validation
if len(sys.argv) != 4:
    print(usage)
    sys.exit()

# Resolve target hostname
try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name resolution error")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

print(f"Scanning Target: {target}")

# Define the queue and threading lock
queue = Queue()
lock = threading.Lock()


# Define the worker function for scanning ports
def scan_port():
    while not queue.empty():
        port = queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            conn = s.connect_ex((target, port))
            if not conn:
                with lock:
                    print(f"Port {port} is OPEN")
            s.close()
        except Exception as e:
            pass
        finally:
            queue.task_done()


# Populate the queue with the range of ports to scan
for port in range(start_port, end_port + 1):
    queue.put(port)

# Define the number of threads (optimal number depends on the system's resources)
num_threads = 500  # Adjust this number if needed

# Create and start threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=scan_port)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
queue.join()

# End time
end_time = time.time()
print(f"Time elapsed: {end_time - start_time:.2f} seconds")

