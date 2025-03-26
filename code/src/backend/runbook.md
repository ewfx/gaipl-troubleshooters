# Runbook: Mortgagelending Application Incidents (INC-1 & INC-4)

## Executive Summary

This runbook addresses two critical incidents (INC-1 and INC-4) affecting the "mortgagelending" application. INC-1 involves a replica mismatch, with two replicas running instead of the desired one. INC-4 involves resource starvation, preventing pod scheduling due to insufficient CPU and memory. This document outlines the steps to resolve both incidents, including verification, rollback, and troubleshooting procedures.

## Detailed Issue Description and Impact

* **INC-1 (Replica Mismatch):** The mortgagelending application has two running replicas despite the desired replica count being one. This can lead to data inconsistency, resource contention, and unpredictable application behavior.

* **INC-4 (Resource Starvation):**  Pods for the mortgagelending application are failing to schedule due to insufficient CPU and memory resources within the Kubernetes cluster. This prevents new instances of the application from starting, impacting availability and potentially causing outages.  This may also affect other applications running in the cluster.

## Prerequisites

* **Tools:**
    * `kubectl` command-line tool configured to access the Kubernetes cluster.
    * Access to the Kubernetes cluster dashboard (optional, but helpful).
    * Monitoring tools (e.g., Prometheus, Grafana) to observe resource utilization.

* **Access:**
    * Kubernetes cluster administrator or equivalent privileges.

* **Credentials:**
    * Valid Kubernetes configuration file (`kubeconfig`).


## Step-by-Step Implementation Instructions

### Resolving INC-1 (Replica Mismatch)

1. **Identify the extra replica:**
   ```bash
   kubectl get pods -l app=mortgagelending
   ```
2. **Delete the extra replica:**  Replace `<pod-name>` with the name of the extra pod.
   ```bash
   kubectl delete pod <pod-name>
   ```
3. **Verify the replica count:**
   ```bash
   kubectl get deployments mortgagelending
   ```
   Ensure the "DESIRED" and "CURRENT" replica counts are both 1.

### Resolving INC-4 (Resource Starvation)

1. **Investigate resource usage:**
   ```bash
   kubectl top nodes
   kubectl top pods -n <namespace>  # Replace <namespace> with the application's namespace
   ```
2. **Option 1: Scale down other non-critical applications:**  If other applications are consuming excessive resources, consider scaling them down temporarily to free up resources for mortgagelending.
3. **Option 2: Increase cluster resources:**  If scaling down other applications is not feasible, add more nodes to the cluster or increase the resource limits of existing nodes. This usually involves interacting with your cloud provider or infrastructure team.
4. **Option 3: Optimize resource requests and limits for mortgagelending:**  Review the resource requests and limits defined in the mortgagelending deployment YAML file. If they are too high, adjust them to more appropriate values.  If they are too low and causing throttling, carefully increase them.
   ```bash
   kubectl describe deployment mortgagelending
   kubectl edit deployment mortgagelending # Edit resource requests and limits
   ```


## Verification Procedures

* **INC-1:** Verify that only one replica of the mortgagelending application is running using `kubectl get pods -l app=mortgagelending`.
* **INC-4:** Verify that new pods for the mortgagelending application are scheduling successfully and entering a running state. Monitor resource utilization to ensure that sufficient resources are available.  Check application logs for any errors related to resource constraints.

## Rollback Instructions

### INC-1 (Replica Mismatch):

If accidentally deleting the wrong pod, the deployment will automatically recreate a new pod to maintain the desired replica count of 1. No manual rollback is required.

### INC-4 (Resource Starvation):

* **If you scaled down other applications:** Scale them back up to their original replica counts.
* **If you modified resource requests/limits:** Revert the deployment YAML to its previous version:
    ```bash
    kubectl rollout undo deployment/mortgagelending
    ```
* **If you added nodes:**  The process for removing nodes depends on your cloud provider or infrastructure setup. Consult your provider's documentation.


## Troubleshooting

* **Pods still failing to schedule:** Check for other potential issues like PersistentVolumeClaim (PVC) binding failures, image pull errors, or security context misconfigurations. Examine pod logs and events (`kubectl describe pod <pod-name>` and `kubectl get events`) for clues.
* **Replica mismatch persists:** Check the deployment configuration for any unintentional updates or scaling events. Review the replicaset controller to ensure it is functioning correctly.
* **Resource usage remains high:**  Investigate potential memory leaks or inefficient code within the application. Profile the application to identify performance bottlenecks.


This runbook provides a comprehensive guide to resolving the mortgagelending application incidents. Remember to adapt the steps and commands to your specific environment and configuration.  Regularly review and update this runbook to reflect changes in your infrastructure and application.
