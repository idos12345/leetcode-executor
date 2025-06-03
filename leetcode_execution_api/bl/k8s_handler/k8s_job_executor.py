import yaml
from kubernetes import client, config
from leetcode_execution_api.core.config import settings
from leetcode_execution_api import constants


class K8sJobExecutor:

    def __init__(self):
        config.load_incluster_config()

    @staticmethod
    def execute_job(
        image_name: str, yaml_path=constants.K8S_JOB_YAML_PATH, namespace="default"
    ) -> None:
        """
        Create and execute k8s job for image
        :param image_name:
        :param yaml_path:
        :param namespace:
        """

        with open(yaml_path, "r") as f:
            job_manifest = yaml.safe_load(f)
        k8s_api = client.BatchV1Api()  # Initialize Kubernetes Batch API
        job = client.V1Job(
            api_version=job_manifest["apiVersion"],
            kind=job_manifest["kind"],
            metadata=client.V1ObjectMeta(name=f"{image_name}-job"),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=job_manifest["spec"]["template"]["spec"][
                                    "containers"
                                ][0]["name"],
                                image=f"{settings.REGISTRY_URL}/{image_name}:latest",
                                image_pull_policy=job_manifest["spec"]["template"][
                                    "spec"
                                ]["containers"][0]["imagePullPolicy"],
                                env=[
                                    client.V1EnvVar(
                                        name=env_var["name"], value=env_var["value"]
                                    )
                                    for env_var in job_manifest["spec"]["template"][
                                        "spec"
                                    ]["containers"][0].get("env", [])
                                ],
                            )
                        ],
                        restart_policy=job_manifest["spec"]["template"]["spec"][
                            "restartPolicy"
                        ],
                    )
                )
            ),
        )

        k8s_api.create_namespaced_job(namespace=namespace, body=job)
