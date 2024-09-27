import os
import gc
import psutil
import subprocess
import signal
import tensorflow as tf

def kill_python_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name contains 'python'
            if 'python' in proc.info['name']:
                print(f"Killing Python process {proc.info['pid']} using {proc.memory_info().rss / (1024 * 1024):.2f} MB.")
                # Terminate the process
                proc.send_signal(signal.SIGKILL)  # Forceful termination
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Skip processes that no longer exist or we don't have access to

def clear_memory_caches():
    print("Garbage collection done.")
    gc.collect()  # Garbage collection
    try:
        # Execute only the drop_caches with sudo
        subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], check=True)
        print("Memory caches dropped.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to drop memory caches: {e}")


def clear_tensorflow_session():
    tf.keras.backend.clear_session()
# if __name__ == "__main__":
#     clear_memory_caches()
#     kill_python_processes()
#     tf.keras.backend.clear_session()  # Clear TensorFlow session
