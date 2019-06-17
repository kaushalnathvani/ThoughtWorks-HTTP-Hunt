import requests
import json


class RequestHandler:

    def __init__(self, api_config):
        self.api_config = api_config

        self.headers = {
            'content-type': 'application/json',
            'userId': self.api_config['userid']
        }

    def get_stage(self):
        response = requests.get(self.api_config['uri'], headers=self.headers)
        data = response.text

        response = json.loads(data)
        if 'stage' in response:
            stage = response['stage'][:1]
            statement = response['statement']
        else:
            stage = 0
            statement = response['message']
        return stage, statement

    def get_stage_instructions(self):
        stage_input_url = self.api_config['uri'] + '/' + self.api_config['input']
        response = requests.get(stage_input_url, headers=self.headers)

        data = json.loads(response.text)

        return data

    def post_output(self, body):
        stage_output_url = self.api_config['uri'] + '/' + self.api_config['output']

        body = json.dumps(body)
        response = requests.post(stage_output_url, body, headers=self.headers)

        data = json.loads(response.text)

        return data
