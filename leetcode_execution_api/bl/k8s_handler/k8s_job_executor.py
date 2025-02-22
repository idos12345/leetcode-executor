import yaml
from kubernetes import client, config
from leetcode_execution_api.core.config import settings


class K8sJobExecutor:

    def __init__(self):
        pass

    def execute_job(self, image_name, yaml_path=settings.K8S_JOB_YAML_PATH):
        config.load_kube_config()
        with open(yaml_path, "r") as f:
            job_manifest = yaml.safe_load(f)
        k8s_api = client.BatchV1Api()  # Initialize Kubernetes Batch API
        job = client.V1Job(
            api_version=job_manifest["apiVersion"],
            kind=job_manifest["kind"],
            metadata=client.V1ObjectMeta(name=job_manifest["metadata"]["name"]),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=job_manifest["spec"]["template"]["spec"]["containers"][0]["name"],
                                image=f"{image_name}:latest",
                                image_pull_policy=job_manifest["spec"]["template"]["spec"]["containers"][0]["imagePullPolicy"],
                                env=[
                                    client.V1EnvVar(
                                        name=env_var["name"],
                                        value=env_var["value"]
                                    ) for env_var in job_manifest["spec"]["template"]["spec"]["containers"][0].get("env", [])
                                ],
                            )
                        ],
                        restart_policy=job_manifest["spec"]["template"]["spec"]["restartPolicy"]
                    )
                )
            )
        )


        k8s_api.create_namespaced_job(namespace="default", body=job)