# import boto3
# import pytest
import os
from os import path

DEV = "us-west-2"
PROD = "us-east-1"


class InvocationTestCase:
    def __init__(self, function_name, json_file_path):
        self.boilerplate = {
            "_testing": True,
            "State_Config": {"Name": "test", "Parameters": {}},
        }
        self.parameters = {}
        self.expected_result = {}
        self.actual_result = {}
        self.did_test_pass = False
        self.test_name = ""
        self.function_name = function_name
        self.json_file_path = json_file_path
        self._parse_file(json_file_path)

    def __repr__(self):
        return self.function_name + str(self.parameters)

    def _parse_file(self, json_file_path):
        pass

    def run_test(self, blocking=False):
        pass


# read testing variables from file


# get test cases
FUNCTIONS_LOCATION = "./functions"
for lambda_name in os.listdir(FUNCTIONS_LOCATION):
    full_path = path.join(FUNCTIONS_LOCATION, lambda_name)
    if path.isdir(full_path):
        for file_name in os.listdir(full_path):
            file_path = path.join(full_path, file_name)
            if path.isfile(file_path) and path.splitext(file_path)[1] == ".json":
                test_case = InvocationTestCase(lambda_name, file_path)
                print(test_case)

# print(dirs)
# os.path.isdir()
