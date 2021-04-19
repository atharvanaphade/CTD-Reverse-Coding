from django.shortcuts import render
from .imports import *
import os
import subprocess

# Create your views here.

class Code():
    def __init__(self, username, ques_id, lang, testcase, code):
        self.code = code
        self.lang = lang
        self.testcase = testcase
        self.username = username
        self.ques_id = ques_id
        os.chdir(user_codes_dir.format(self.username, self.ques_id, self.lang))
        code_file = open("main.{}".format(self.lang), "w+")
        code_file.write(self.code)
        code_file.close()
        input_file = open("input", "w+")
        input_file.write(self.testcase)
        input_file.close()

class Result():
    def __init__(self, ques_id, testcase_id, username, status, error):
        self.ques_id = ques_id
        self.testcase_td = testcase_id
        self.username = username
        self.status = status
        self.error = error
    
    def getError(self):
        return self.error

    def getStatus(self):
        return self.status

class Checker:
    def Check(output, exp_output, testcase_id, username, ques_id, attempt):
        escapes = '\n\r\t\b'
        for s in escapes:
            output = output.replace(s, '')
            exp_output = exp_output.replace(s, '')
        if(str(output) == str(exp_output)):
            status = "AC"
            error = "Compiled Successfully"
            result = Result(ques_id, testcase_id, username, status, error)
            return result
        status = "WA"
        error = "Compiled Succesfully"
        result = Result(ques_id, testcase_id, username, status, error)
        return result

class Runner():
    def __init__(self, username, lang, testcase_id, testcase, testcase_output, ques_id, code, attempt):
        self.username = username
        self.lang = lang
        self.testcase_id = testcase_id
        self.testcase = testcase
        self.testcase_output = testcase_output
        self.ques_id = ques_id
        self.code = code
        self.attempt = attempt
    
    def RunCode(self):
        code_obj = Code(self.username, self.ques_id, self.lang, self.testcase, self.code)
        os.chdir(user_codes_dir.format(self.username, self.ques_id, self.lang))
        build_image_commmand = ['sudo', 'docker', 'image', 'build', '.', '-t', '{}-{}-image'.format(self.username, self.lang)]
        execute_container_command = ['sudo', 'docker', 'run', '--rm', '--security-opt', 'seccomp={}'.format(seccomp_profile_dir + "/seccomp.json"), '{}-{}-image'.format(self.username, self.lang)]
        build_stat = None
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
                    output = execute_proc_out.decode("utf-8")
                    out_file = open("output", "w+")
                    out_file.write(output)
                    out_file.close()
                    result = Checker.Check(output, self.testcase_output, self.testcase_id, self.username, self.ques_id, self.attempt)
                    return result
                elif(execute_proc_stat_code == 124):
                    status = "TLE"
                    error = execute_proc_err.decode("utf-8")
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return result
                elif(execute_proc_stat_code == 139):
                    status = "Memory Limit Exceeded"
                    error = execute_proc_err.decode("utf-8")
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return result
                elif(execute_proc_stat_code == 1):
                    status = "RTE"
                    error = execute_proc_err.decode("utf-8")
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return result
                elif(execute_proc_stat_code == 2):
                    status = "CTE"
                    error = execute_proc_err.decode("utf-8")
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return result
                else:
                    status = "Unknown Error"
                    error = execute_proc_err.decode("utf-8")
                    result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                    return Result
            except:
                print("Exception Occurred while running code!")
                status = "Server Error"
                error = "Server Error while running code"
                result = Result(self.ques_id, self.testcase_id, self.username, status, error)
                return result
        else:
            status = "Server Error while Building Image"
            error = "Server Error"
            result = Result(self.ques_id, self.testcase_id, self.username, status, error)
            return result

