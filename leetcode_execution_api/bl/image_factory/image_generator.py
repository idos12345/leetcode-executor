import base64
import tempfile
import os
from abc import abstractmethod
from string import Template

from django.templatetags.i18n import language
from docker.client import from_env

from resources.docker_files.java.java_dockerfile import java_dockerfile
from resources.docker_files.python.python_dockerfile import python_dockerfile
from resources.excution_script_templates.java.java_executor import java_template
from resources.excution_script_templates.python.python_executor import python_template

image_generator_parameters = {
    "python": {
        "code_template": python_template,
        "dockerfile": python_dockerfile,
        "tests_seperator": "\n\r",
        "file_format": "py"
    },
    "java": {
        "code_template": java_template,
        "dockerfile": java_dockerfile,
        "tests_seperator": "\n",
        "file_format": "java"
    }
}


@abstractmethod
class ImageGenerator:

    def __init__(self, code_template: Template, dockerfile: str, file_format: str, tests_seperator):
        self.client = from_env()
        self.code_template = code_template
        self.dockerfile_content = dockerfile
        self.tests_seperator = tests_seperator
        self.file_format = file_format

    def build_image(self, image_name: str, encoded_solution_code: str, encoded_tests_code: list[str]) -> None:
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
            app_py_path = os.path.join(tmpdir, f"TestSolution.{self.file_format}")

            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)

            with open(app_py_path, "w") as f:
                f.write(script_content)

            # Build the Docker image
            image, _ = self.client.images.build(path=tmpdir, tag=image_name)
    @staticmethod
    def indent_string(text: str, spaces: int = 4) -> str:
        """Indents a given string by a specified number of spaces (default: 4)."""
        indentation = " " * spaces
        return "\n".join(indentation + line for line in text.splitlines())

    def inject_code_to_test_script(self, solution_code: str, tests_code_list: list[str]) -> str:
        """
        Inject solution and tests code to test script
        :param solution_code: solution code
        :param tests_code_list: list of tests code
        :return: injected test script
        """
        tests = self.tests_seperator.join(tests_code_list)
        test_script = self.code_template.substitute(solution=self.indent_string(solution_code), tests=self.indent_string(tests))
        return test_script
