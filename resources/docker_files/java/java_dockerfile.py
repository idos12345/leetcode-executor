java_dockerfile = """
FROM swr.tr-west-1.myhuaweicloud.com/ido/java-junit-base:latest

WORKDIR /app

COPY . /app

RUN javac -cp .:/jars/junit-platform-console-standalone-1.10.0.jar TestSolution.java

CMD sh -c 'java -cp .:/jars/junit-platform-console-standalone-1.10.0.jar org.junit.platform.console.ConsoleLauncher --select-class TestSolution; exit 0'


"""