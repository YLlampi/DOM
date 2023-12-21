import time
import psutil
import memory_profiler

@profile
def run_scraping_test(scraping_function, num_executions=10):
    total_execution_time = 0
    total_cpu_usage = 0
    total_memory_usage = 0

    for _ in range(num_executions):
        execution_time, cpu_usage, memory_usage = execute_once(scraping_function)
        total_execution_time += execution_time
        total_cpu_usage += cpu_usage
        total_memory_usage += memory_usage

    average_execution_time = total_execution_time / num_executions
    average_cpu_usage = total_cpu_usage / num_executions
    average_memory_usage = total_memory_usage / num_executions

    print(f"Avg. Execution Time: {average_execution_time} seconds")
    print(f"Avg. CPU Usage: {average_cpu_usage}%")
    print(f"Avg. Memory Usage: {average_memory_usage} MB")

@profile
def execute_once(scraping_function):
    start_time = time.time()
    cpu_before = psutil.cpu_percent(interval=None)
    memory_before = psutil.virtual_memory().used / (1024 * 1024)

    try:
        scraping_function()
    except Exception as e:
        print(f"Error during scraping: {e}")

    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=None)
    memory_after = psutil.virtual_memory().used / (1024 * 1024)

    execution_time = end_time - start_time
    cpu_usage = (cpu_before + cpu_after) / 2
    memory_usage = memory_after - memory_before

    print(f"Execution Time: {execution_time} seconds")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage} MB")

    return execution_time, cpu_usage, memory_usage

@profile
def scraping_function():
    time.sleep(2)

run_scraping_test(scraping_function)
