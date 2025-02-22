import time
from functools import wraps

import yaml
from kubernetes import client, config
from leetcode_execution_api.core.config import settings




class K8sJobLogsFetcher:

    def __init__(self):
        config.load_kube_config()

    @staticmethod
    def fetch_logs(image_name, namespace="default"):
        job_name = f"{image_name}-job"

        # Wait for job to end
        if not K8sJobLogsFetcher.wait_for_job(job_name, namespace):
            raise Exception("Job failed to complete")

        core_v1 = client.CoreV1Api()
        pod_list = core_v1.list_namespaced_pod(namespace, label_selector=f"job-name={job_name}").items
        pod_name = pod_list[0].metadata.name
        logs = core_v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        return logs

    @staticmethod
    def wait_for_job(job_name, namespace="default", max_time=60, poll_interval=1):
        """Wait for a Kubernetes Job to complete with a max timeout."""
        batch_v1 = client.BatchV1Api()

        start_time = time.time()
        while time.time() - start_time < max_time:
            job = batch_v1.read_namespaced_job_status(name=job_name, namespace=namespace).status
            if job.succeeded:
                return True  # Job completed
            if job.failed and job.failed > 0:
                return False  # Job failed
            time.sleep(poll_interval)

        return False  # Timeout reached