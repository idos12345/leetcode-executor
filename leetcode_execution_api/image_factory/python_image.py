from leetcode_execution_api.image_factory.base_image import BaseImageGenerator
from resources.docker_files.python.python_dockerfile import python_dockerfile
from resources.excution_script_templates.python.python_executer import python_template


class PythonImageGenerator(BaseImageGenerator):

    def __init__(self):
        super().__init__()
        self.template = python_template
        self.dockerfile_content = python_dockerfile

    def inject_code_to_test_script(self, solution, test_list):
        tests = "\n\n".join(test_list)
        test_script = self.template.substitute(solution=solution, tests=tests)
        return test_script