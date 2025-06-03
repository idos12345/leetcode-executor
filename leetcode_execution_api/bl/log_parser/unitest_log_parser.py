import re


class UTestLogParser:

    def __init__(self, language: str):
        self.language = language

    def infer_solution_result_from_logs(self, logs: str) -> [bool, str]:
        if self.language == "java":
            return self.__infer_solution_result_from_logs_for_java(logs)
        elif self.language == "python":
            return self.__infer_solution_result_from_logs_for_python(logs)
        else:
            raise Exception("Language not supported")

    @staticmethod
    def __infer_solution_result_from_logs_for_java(logs: str) -> bool:
        tests_found = re.search(r" ([0-9]+) tests found", logs)
        tests_successful = re.search(r" ([0-9]+) tests successful", logs)

        if not tests_found or not tests_successful:
            raise Exception("Could not infer solution from logs")

        return tests_successful.group(1) == tests_found.group(1)

    @staticmethod
    def __infer_solution_result_from_logs_for_python(logs: str) -> [bool, str]:

        last_log = logs.splitlines()[-1]
        return "OK" in last_log
