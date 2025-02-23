java_dockerfile = """
FROM openjdk:17-slim

RUN apt-get update && apt-get install -y wget

WORKDIR /app

COPY . /app

RUN wget -q https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.9.3/junit-platform-console-standalone-1.9.3.jar

RUN javac -cp .:junit-platform-console-standalone-1.9.3.jar TestSolution.java

CMD sh -c 'java -cp .:junit-platform-console-standalone-1.9.3.jar org.junit.platform.console.ConsoleLauncher --select-class TestSolution; [ $? -eq 1 ] && exit 0 || exit $?'

"""