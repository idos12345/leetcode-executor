import unittest
from leetcode_execution_api.bl.log_parser.unitest_log_parser import UTestLogParser
from unittest.mock import patch


class TestUTestLogParser(unittest.TestCase):

    def _set_mock_settings(self, mock_settings):
        """Apply default mock values to settings."""
        mock_settings.DATABASE_URL = "sqlite:///:memory:"
        mock_settings.K8S_JOB_YAML_PATH = "/fake/path/job.yaml"
        mock_settings.REGISTRY_URL = "localhost:5000"

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_java_logs_successful(self):
        parser = UTestLogParser("java")
        logs = " 5 tests found\n 5 tests successful"
        self.assertTrue(parser.infer_solution_result_from_logs(logs))

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_java_logs_failed(self):
        parser = UTestLogParser("java")
        logs = " 5 tests found\n 3 tests successful"
        self.assertFalse(parser.infer_solution_result_from_logs(logs))

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_python_logs_successful(self):
        parser = UTestLogParser("python")
        logs = "Some logs...\nOK"
        self.assertTrue(parser.infer_solution_result_from_logs(logs))

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_python_logs_failed(self):
        parser = UTestLogParser("python")
        logs = "Some logs...\nFAILED"
        self.assertFalse(parser.infer_solution_result_from_logs(logs))

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_unsupported_language(self):
        parser = UTestLogParser("cpp")
        with self.assertRaises(Exception) as context:
            parser.infer_solution_result_from_logs("Some logs...")
        self.assertEqual(str(context.exception), "Language not supported")

    @patch(
        "leetcode_execution_api.bl.log_parser.unitest_log_parser.UTestLogParser.settings"
    )
    def test_java_logs_missing_info(self):
        parser = UTestLogParser("java")
        logs = " 5 tests found"
        with self.assertRaises(Exception) as context:
            parser.infer_solution_result_from_logs(logs)
        self.assertEqual(str(context.exception), "Could not infer solution from logs")


if __name__ == "__main__":
    unittest.main()
