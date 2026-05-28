
import subprocess
import json
import time
from datetime import datetime
def __init__(self, namespace):
        self.namespace = namespace

def run_kubectl_command(command):
       """
       Executes kubectl command and returns output

       """
       result = subprocess.run(
            command, 
            capture_output=True,
            text=True,
            shell=True
        
     )
       
       if result.returncode != 0:
          print(f"Error executing command")
          print(result.stderr)
          return None
       
       return result.stdout
    
# ============================================
# Get all pod details from Kubernetes
# ============================================

def get_pods():

    command =         [
        "kubectl",
        "get",
        "pods",
        "-A",
        "-o",
        "json"
         ]

    output = run_kubectl_command(command)

    if output:
        return json.loads(output)

    return None

# ============================================
# Analyze pod health
# ============================================

def analyze_pods(pod_data):

    print("\n======================================")
    print(" Kubernetes Pod Health Monitor")
    print("======================================")

    print(f"\nScan Time: {datetime.now()}\n")

    items = pod_data.get("items", [])

    total_pods = len(items)

    running_pods = 0
    pending_pods = 0
    healthy_pods = 0
    unhealthy_pods = 0
    failed_pods = 0
    warning_pods = 0

    for pod in items:
        
        namespace = pod["metadata"]["namespace"]
        pod_name = pod["metadata"]["name"]

        phase = pod["status"].get("phase", "Unknown")

        containers_status = pod["status"].get("containerStatuses", [])

        restart_count = 0
        waiting_reasons = ""

        for container in containers_status:

            restart_count += container.get("restartCount", 0)

            state = container.get("state", {})

            if "waiting" in state:

                waiting_reasons += state["waiting"].get("reason", "") + " "

    # ====================================
    # Health Logic
    # ====================================

    health_status = "HEALTHY"

    if phase != "Running":
        health_status = "Failed"
        failed_pods += 1

    elif restart_count >= 3:
        health_status = "WARNING"
        warning_pods += 1

    elif waiting_reasons == "CrashLoopBackOff":
        health_status = "CRITICAL"
        unhealthy_pods += 1

    else:

        running_pods += 1

    # ====================================
    # Display Pod Status
    # ==================================== 

    print("--------------------------------------")
    print(" Cluster Summary")
    print("======================================")


    print(f"Total Pods: {total_pods}")
    print(f"Running Pods: {running_pods}")  
    print(f"Pending Pods: {pending_pods}")
    print(f"Healthy Pods: {healthy_pods}")
    print(f"Unhealthy Pods: {unhealthy_pods}")
    print(f"Failed Pods: {failed_pods}")
    print(f"Warning Pods: {warning_pods}")

    print(f"\nMonitoring completed at: {datetime.now()}\n")
    print("--------------------------------------")

# ============================================
# Main Function
# ============================================

def main():

    print("Starting Kubernetes Pod Health Monitor...")

    pod_data = get_pods()

    if pod_data:

        analyze_pods(pod_data)
    else:
        print("Failed to retrieve pod data.")

# ============================================
# Program Entry Point
# ============================================

if __name__ == "__main__":
    main()



        








    


    


        

    



       
