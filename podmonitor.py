# ============================================
# Kubernetes Pod Health Monitor (Self-Testing)
# ============================================

import subprocess
import json
from datetime import datetime

# ============================================
# Mock Data for testing without a cluster
# ============================================
MOCK_KUBERNETES_DATA = {
    "items": [
        {
            "metadata": {"namespace": "default", "name": "web-server-pod"},
            "status": {
                "phase": "Running",
                "containerStatuses": [{"restartCount": 0, "state": {"running": {}}}]
            }
        },
        {
            "metadata": {"namespace": "production", "name": "database-pod"},
            "status": {
                "phase": "Running",
                "containerStatuses": [{"restartCount": 5, "state": {"running": {}}}]
            }
        },
        {
            "metadata": {"namespace": "kube-system", "name": "broken-service-pod"},
            "status": {
                "phase": "Running",
                "containerStatuses": [{"restartCount": 12, "state": {"waiting": {"reason": "CrashLoopBackOff"}}}]
            }
        },
        {
            "metadata": {"namespace": "default", "name": "failed-deployment-pod"},
            "status": {
                "phase": "Failed",
                "containerStatuses": [{"restartCount": 0, "state": {"terminated": {"reason": "Error"}}}]
            }
        }
    ]
}

# ============================================
# Function to execute kubectl command
# ============================================
def run_kubectl_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            return None
        return result.stdout
    except Exception:
        return None

# ============================================
# Get all pod details from Kubernetes
# ============================================
def get_pods():
    command = ["kubectl", "get", "pods", "-A", "-o", "json"]
    output = run_kubectl_command(command)

    if output:
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            pass

    # FALLBACK: If no cluster is found, use the mock data seamlessly
    print("⚠️  No active Kubernetes cluster found. Using Mock Test Environment...")
    return MOCK_KUBERNETES_DATA

# ============================================
# Analyze pod health
# ============================================
def analyze_pods(pod_data):
    print("\n======================================")
    print(" Kubernetes Pod Health Monitor")
    print("======================================")
    print(f"Scan Time: {datetime.now()}\n")

    items = pod_data.get("items", [])
    total_pods = len(items)
    running_pods = 0
    failed_pods = 0
    warning_pods = 0

    for pod in items:
        namespace = pod["metadata"]["namespace"]
        pod_name = pod["metadata"]["name"]
        phase = pod["status"].get("phase", "Unknown")
        container_statuses = pod["status"].get("containerStatuses", [])

        restart_count = 0
        waiting_reason = ""

        for container in container_statuses:
            restart_count += container.get("restartCount", 0)
            state = container.get("state", {})
            if "waiting" in state:
                waiting_reason = state["waiting"].get("reason", "")

        # ====================================
        # Fixed Health Logic Order
        # ====================================
        health_status = "HEALTHY"

        if phase != "Running":
            health_status = "FAILED"
            failed_pods += 1
        elif waiting_reason == "CrashLoopBackOff":
            health_status = "CRITICAL"
            failed_pods += 1
        elif restart_count >= 3:
            health_status = "WARNING"
            warning_pods += 1
        else:
            running_pods += 1

        # ====================================
        # Display Pod Status
        # ====================================
        print("--------------------------------------")
        print(f"Namespace       : {namespace}")
        print(f"Pod Name        : {pod_name}")
        print(f"Pod Phase       : {phase}")
        print(f"Restart Count   : {restart_count}")
        if waiting_reason:
            print(f"Waiting Reason  : {waiting_reason}")
        print(f"Health Status   : {health_status}")

    # ========================================
    # Summary
    # ========================================
    print("\n======================================")
    print(" Cluster Summary")
    print("======================================")
    print(f"Total Pods      : {total_pods}")
    print(f"Healthy Pods    : {running_pods}")
    print(f"Warning Pods    : {warning_pods}")
    print(f"Failed Pods     : {failed_pods}")
    print("\nMonitoring completed.\n")

# ============================================
# Main Function
# ============================================
def main():
    print("\nConnecting to Kubernetes Cluster...\n")
    pod_data = get_pods()
    if pod_data:
        analyze_pods(pod_data)
    else:
        print("Failed to fetch pod information.")

if __name__ == "__main__":
    main()
