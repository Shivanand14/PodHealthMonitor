# PodHealthMonitor
Kubernetes Pod Health Monitor
****Why This Script Was Created?**

When managing microservices, checking the health of every single pod across multiple namespaces using standard terminal commands can be tedious. You usually have to run several commands just to find out which pods are failing, crash-looping, or constantly restarting.This script was built to automate that process. It provides a quick, central health check for your entire Kubernetes cluster by scanning all namespaces at once and translating raw cluster data into a simple, readable dashboard summary.

****What This Script Does?**

The script interacts with your cluster to pull and evaluate live pod configurations. Here is exactly what it handles during execution:

**Cluster Data Retrieval:** 
It automatically executes a background kubectl command to fetch details for every pod across all namespaces in a single JSON payload.

**Automatic Error Handling:**
If kubectl is not installed or your cluster context is down, it catches the error and cleanly notifies you instead of crashing.

**Health Evaluation:**
It loops through every container inside your pods to track active status phases, string patterns for startup failures, and individual container restart counts.

**Status Classification:** 
It categorizes pods into distinct states like Healthy, Warning, or Failed based on live cluster metrics (such as identifying pods with 3 or more restarts).

**Console Reporting:** 
It prints a neat dashboard layout in your terminal showing individual pod details alongside a total cluster health summary count.

**How to Use It**

Prerequisites
Before running the script, make sure your local environment has the following components set up:
Python 3.x installed on your system.
kubectl CLI tool installed and configured.
An active connection to a Kubernetes cluster (ensure your active context is set up properly by verifying that a regular kubectl get nodes command works in your terminal).
Installation and SetupClone or download this project folder onto your local machine.
Save the script file inside your preferred project directory (e.g., E:\KubernetesPodHealthMonitor\PodHealthMonitor.py).
Running the ScriptOpen your preferred terminal application, navigate to your script folder, and execute the Python file using the following command:powershell python PodHealthMonitor.py
Use code with caution.
Understanding the OutputOnce executed, the script will output information directly to your console:It will display a initialization message showing that the scan has started.
If successful, it prints out a structured summary table showing the live totals for your pods broken down by state (Running, Pending, Healthy, Unhealthy, Failed, and Warning) along with the exact completion timestamp.
