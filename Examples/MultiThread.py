import threading
import time

def worker(name, delay):
    for i in range(3):
        time.sleep(delay)
        print(f"[{name}] Durchlauf {i+1}")

threads = [
    threading.Thread(target=worker, args=("Worker-A", 1)),
    threading.Thread(target=worker, args=("Worker-B", 0.7))
]

for t in threads:  
    t.start()

for t in threads:
    t.join()

print("Alle Threads fertig!")
