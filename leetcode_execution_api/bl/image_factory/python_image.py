from leetcode_execution_api.bl.image_factory.base_image import BaseImageGenerator
from resources.docker_files.python.python_dockerfile import python_dockerfile
from resources.excution_script_templates.python.python_executor import python_template


class PythonImageGenerator(BaseImageGenerator):

    def __init__(self):
        super().__init__()
        self.template = python_template
        self.dockerfile_content = python_dockerfile

    def inject_code_to_test_script(self, solution_code:str, tests_code_list:list[str]) -> str:
        """
        Inject solution and tests code to test script
        :param solution_code: solution code
        :param tests_code_list: list of tests code
        :return: injected test script
        """
        tests = "\n\r    ".join(tests_code_list)
        test_script = self.template.substitute(solution=solution_code, tests=tests)
        return test_script