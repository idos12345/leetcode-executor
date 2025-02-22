import tempfile
import os
from abc import abstractmethod



@abstractmethod
class BaseImageGenerator:

    def __init__(self):
        # self.client = docker.from_env()
        self.template = None
        self.dockerfile_content = None

    def build_image(self, image_tag, question, tests):
        script_content = self.inject_code_to_test_script(question, tests)
        with tempfile.TemporaryDirectory() as tmpdir:
            dockerfile_path = os.path.join(tmpdir, "Dockerfile")
            app_py_path = os.path.join(tmpdir, "test.py")

            with open(dockerfile_path, "w") as f:
                f.write(self.dockerfile_content)

            with open(app_py_path, "w") as f:
                f.write(script_content)

            # Build the Docker image
            # image, _ = self.client.images.build(path=tmpdir, tag=image_tag)

    @abstractmethod
    def inject_code_to_test_script(self, question, tests):
        pass
