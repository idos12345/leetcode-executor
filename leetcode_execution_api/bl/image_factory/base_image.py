import base64
import tempfile
import os
from abc import abstractmethod

from docker.client import from_env


@abstractmethod
class BaseImageGenerator:

    def __init__(self):
        self.client = from_env()
        self.template = None
        self.dockerfile_content = None

    def build_image(self, image_name:str, encoded_solution_code:str , encoded_tests_code:list[str]) -> None:
        """
        Build docker image for the solution
        :param image_name: docker image name
        :param encoded_solution_code: base64 encoded solution code
        :param encoded_tests_code: base64 encoded tests code list
        """

        # Decode solution and tests
        decoded_solution_code = base64.b64decode(encoded_solution_code).decode("utf-8")
        decoded_tests_code = [base64.b64decode(test_code).decode("utf-8") for test_code in encoded_tests_code]

        script_content = self.inject_code_to_test_script(decoded_solution_code, decoded_tests_code)

        # Build app in tmp dir
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile_path = os.path.join(tmpdir, "Dockerfile")
            app_py_path = os.path.join(tmpdir, "test.py")

            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)

            with open(app_py_path, "w") as f:
                f.write(script_content)

            # Build the Docker image
            image, _ = self.client.images.build(path=tmpdir, tag=image_name)

    @abstractmethod
    def inject_code_to_test_script(self, question, tests):
        pass
