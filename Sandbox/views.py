from django.shortcuts import render
from .imports import *
import os
import subprocess

# Create your views here.

class Code():
    def __init__(self, username, ques_id, lang, testcase, status):
        self.lang = lang
        self.testcase = testcase
        self.status = status
        self.username = username
        self.ques_id = ques_id

    def PutCodeAndTestcases(self, code):
        os.chdir(user_codes_dir.format(self.username, self.lang, ""))
        code_file = open("main." + self.lang, "w+")
        code_file.write(code)
        code_file.close()
        input_file = open("input", "w+")
        input_file.write(self.testcase)

class Result():
    def __init__(self, ques_id, testcase_id, username, status, error):
        self.ques_id = ques_id
        self.testcase_td = testcase_id
        self.username = username
        self.status = status
        self.error = error

class Runner():
    def __init__(self, username, lang, testcase_id, testcase, ques_id, code, attempt):
        self.username = username
        self.lang = lang
        self.testcase_id = testcase_id
        self.testcase = testcase
        self.ques_id = ques_id
        self.code = code
        self.attempt = attempt
    
    def RunCode(self):
        os.chdir(user_codes_dir.format(self.username, self.ques_id, self.lang))
        build_image_commmand = ['sudo', 'docker', 'image', 'build', '.', '-t', '{}-{}-image-{}'.format(self.username, self.lang, self.attempt)]
        execute_container_command = ['sudo', 'docker', 'run', '--rm', '--security-opt', 'seccomp={}'.format(seccomp_profile_dir + "/seccomp.json"), '{}-{}-image-{}'.format(self.username, self.lang, self.attempt)]
        build_stat = 0
        try:
            build_proc = subprocess.Popen(build_image_commmand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Building Image for thr container")
            [build_proc_out, build_proc_err] = build_proc.communicate()
            build_stat = build_proc.wait()
        except:
            print("Could not build image, exception occurred")
            status = "Server Error Occurred!"
            error = "Server Error"
            result = Result(self.ques_id, self.testcase_id, self.username, status, error)
            return result
        if(build_stat == 0):
            try:
                execute_proc = subprocess.Popen(execute_container_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Executing the code")
                [execute_proc_out, execute_proc_err] = execute_proc.communicate()
                execute_proc_stat_code = execute_proc.wait()
                if(execute_proc_stat_code == 0):
                    output_file = open("output", "w+")
                    output_file.write(execute_proc_out.decode("utf-8"))
                    status = "Compiled Successfully"
                    error = None
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return result
            except:
                print("Exception Occurred while running code!")
                status = "Server Error"
                error = "Server Error while running code"
                result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                return result
        else:
            return("Server Error Occurred while Building image")


        
