import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
user_codes_dir = cur_dir + "../SandboxData/Users/{}/{}/{}"
seccomp_profile_dir = os.path.abspath(os.path.dirname(__name__)) + "/SandboxData/"

Dockerfile = [
    "FROM openjdk:11.0.6-jdk-slim\n" + "WORKDIR /app\n" + "USER root\n" + "ADD . .\n" + "RUN chmod a+x ./main.java\n" + "RUN chmod a+x ./entrypoint.sh\n" + "ENTRYPOINT ./entrypoint.sh\n",
    "FROM python:3.7\n" + "WORKDIR /app\n" + "USER root\n" + "ADD . .\n" + "RUN chmod a+x ./main.py\n" + "RUN chmod a+x ./entrypoint.sh\n" + "ENTRYPOINT ./entrypoint.sh\n",
    "FROM gcc\n" + "WORKDIR /app\n" + "USER root\n" + "ADD . .\n" + "RUN chmod a+x ./main.c\n" + "RUN chmod a+x ./entrypoint.sh\n" + "ENTRYPOINT ./entrypoint.sh\n",
    "FROM gcc\n" + "WORKDIR /app\n" + "USER root\n" + "ADD . .\n" + "RUN chmod a+x ./main.cpp\n" + "RUN chmod a+x ./entrypoint.sh\n" + "ENTRYPOINT ./entrypoint.sh\n"
]

EntryPointScript = [
    "#!/usr/bin/env bash\n" + "javac main.java\n" + "ret=$?\n" + "if [ $ret -ne 0 ]\n" + "then\n" + "  exit 2\n" + "fi\n" + "ulimit -s 100\n" + "timeout --signal=SIGTERM 1 java main < input\n" + "exit $?\n",
    "#!/usr/bin/env bash\n" + "ulimit -s " + "100\n" + "timeout --signal=SIGTERM " + "2" + " python3 main.py < input\n" + "exit $?\n",
    "#!/usr/bin/env bash\n" + "gcc main.c" + " -o exec" + "\n" + "ret=$?\n" + "if [ $ret -ne 0 ]\n" + "then\n" + "  exit 2\n" + "fi\n" + "ulimit -s " + "100" + "\n" + "timeout --signal=SIGTERM " + "2" + " ./exec " + " < " + "input" + "\n" + "exit $?\n",
    "#!/usr/bin/env bash\n" + "g++ main.cpp" + " -o exec" + "\n" + "ret=$?\n" + "if [ $ret -ne 0 ]\n" + "then\n" + "  exit 2\n" + "fi\n" + "ulimit -s " + "100" + "\n" + "timeout --signal=SIGTERM " + "2" + " ./exec " + " < " + "input" + "\n" + "exit $?\n"
]