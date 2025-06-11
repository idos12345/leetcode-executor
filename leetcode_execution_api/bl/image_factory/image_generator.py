import base64
import tempfile
import os
from abc import abstractmethod
from string import Template
import docker
from resources.docker_files.java.java_dockerfile import java_dockerfile
from resources.docker_files.python.python_dockerfile import python_dockerfile
from resources.excution_script_templates.java.java_executor import java_template
from resources.excution_script_templates.python.python_executor import python_template
from docker.errors import BuildError, APIError
from leetcode_execution_api.core.config import settings

image_generator_parameters = {
    "python": {
        "code_template": python_template,
        "dockerfile": python_dockerfile,
        "tests_seperator": "\n\r",
        "file_format": "py",
    },
    "java": {
        "code_template": java_template,
        "dockerfile": java_dockerfile,
        "tests_seperator": "\n",
        "file_format": "java",
    },
}


@abstractmethod
class ImageGenerator:

    def __init__(
        self,
        code_template: Template,
        dockerfile: str,
        file_format: str,
        tests_seperator,
    ):
        self.client = docker.from_env()
        self.code_template = code_template
        self.dockerfile_content = dockerfile
        self.tests_seperator = tests_seperator
        self.file_format = file_format

    def build_image(
        self, image_name: str, encoded_solution_code: str, encoded_tests_code: list[str]
    ) -> None:
        """
        Build docker image for the solution
        :param image_name: docker image name
        :param encoded_solution_code: base64 encoded solution code
        :param encoded_tests_code: base64 encoded tests code list
        """

        # Decode solution and tests
        decoded_solution_code = base64.b64decode(encoded_solution_code).decode("utf-8")
        decoded_tests_code = [
            base64.b64decode(test_code).decode("utf-8")
            for test_code in encoded_tests_code
        ]

        script_content = self.inject_code_to_test_script(
            decoded_solution_code, decoded_tests_code
        )
        image_full_name = f"{settings.REGISTRY_URL}/{image_name}"

        # Build app in tmp dir
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile_path = os.path.join(tmpdir, "Dockerfile")
            app_py_path = os.path.join(tmpdir, f"TestSolution.{self.file_format}")

            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)

            with open(app_py_path, "w") as f:
                f.write(script_content)

            # Build the Docker image
            try:
                image, logs = self.client.images.build(
                    path=tmpdir, tag=f"{image_name}:latest"
                )
                print("✅ Build succeeded!")
                print("Image ID:", image.short_id)
            except BuildError as e:
                print("❌ Build failed!")
                for line in e.build_log:
                    print(line.get("stream", ""), end="")
                raise e
            except APIError as e:
                print("❌ Docker API error:", str(e))
                raise e

            # Tag the image for registry
            image.tag(image_full_name, tag="latest")

            print(f"Image tagged as {image_full_name}")

            # Push the image to registry

            if not settings.REGISTRY_AUTH_NEEDED:
                push_logs = self.client.images.push(
                    image_full_name,
                    auth_config={
                        "username": settings.SWR_LOGIN_U,
                        "password": settings.SWR_LOGIN_P,
                    },
                    stream=True,
                    decode=True,
                )
            else:
                push_logs = self.client.images.push(
                    f"{image_full_name}:latest", stream=True, decode=True
                )

            for log in push_logs:
                if "error" in log:
                    print("❌ Push failed:", log["error"])
                    raise Exception(f"Failed to push image: {log['error']}")
            print(f"Image {image_full_name} pushed successfully to registry.")

            print("Delete image from local docker")
            self.client.images.remove(image.id, force=True)

            # List dangling images (untagged)
            print("Clean dangling images from local docker")
            dangling_images = [
                img for img in self.client.images.list(filters={"dangling": True})
            ]

            for img in dangling_images:
                try:
                    self.client.images.remove(img.id, force=True)
                    print(f"Removed image {img.id}")
                except Exception as e:
                    print(f"Failed to remove {img.id}: {e}")

            print(f"Image {image_name} removed from local docker.")

    @staticmethod
    def indent_string(text: str, spaces: int = 4) -> str:
        """Indents a given string by a specified number of spaces (default: 4)."""
        indentation = " " * spaces
        return "\n".join(indentation + line for line in text.splitlines())

    def inject_code_to_test_script(
        self, solution_code: str, tests_code_list: list[str]
    ) -> str:
        """
        Inject solution and tests code to test script
        :param solution_code: solution code
        :param tests_code_list: list of tests code
        :return: injected test script
        """
        tests = self.tests_seperator.join(tests_code_list)
        test_script = self.code_template.substitute(
            solution=self.indent_string(solution_code), tests=self.indent_string(tests)
        )
        print("Test script:")
        print(test_script)
        return test_script
