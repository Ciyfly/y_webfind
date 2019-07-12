import concurrent.futures
import tqdm  
import time

def scan(i):
    time.sleep(i)
    print("sleep: "+str(i) )



def run(task):
    print("test ......")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=100) as executor:
        futures = [executor.submit(scan, i) for i in range(task)]
        for future in tqdm.tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures)):
            future.result()

task = 200

run(task)
