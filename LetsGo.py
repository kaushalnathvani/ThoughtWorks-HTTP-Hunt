import RequestHandler
import time
from datetime import datetime
from collections import defaultdict
import ConfigReader


class LetsGo:

    def __init__(self):
        self.stage = 1
        config_reader = ConfigReader.ReadConfig()
        config = config_reader.read()

        if config.has_section('api_config'):
            api_config = dict(config.items('api_config', {}))
            self.request_handler = RequestHandler.RequestHandler(api_config)
            self.play_game()
        else:
            print 'API config not available. Cannot start the game ...'

    def play_game(self):
        ans = raw_input('Start game (y/n)? ---> ')

        if ans.lower() in ['y', 'yes']:
            while self.stage != 0:
                stage, statement = self.request_handler.get_stage()

                self.stage = stage

                print '==================================================='
                print 'Stage:',stage
                print 'Statement:', statement
                print '==================================================='

                if stage == '1':
                    print '\nSolving stage one ...'
                    self.stage_one()
                elif stage == '2':
                    print '\nSolving stage two ...'
                    self.stage_two()
                elif stage == '3':
                    print '\nSolving stage three ...'
                    self.stage_three()
                elif stage == '4':
                    print '\nSolving stage four ...'
                    self.stage_four()
                else:
                    print '\nCongrats. You have reached the finished line ...'
                    break
        else:
            print 'Please start the game again and enter valid input.'

    def stage_one(self):
        data = self.request_handler.get_stage_instructions()
        start = time.time()

        encrypted_message = data['encryptedMessage']
        key = data['key']

        print '\nEncrypted Message:', encrypted_message
        print 'Encryption Key:', key

        ascii_list = [ord(letter) for letter in encrypted_message]

        message = []
        for ascii_char in ascii_list:
            output_identifier = ascii_char - key
            if not 64 < ascii_char < 91:
                message.append(chr(ascii_char))
            elif output_identifier > 64:
                message.append(chr(ascii_char - key))
            else:
                message.append(chr(ascii_char - key + 26))

        print '\nDecryption Successful ...'
        print 'Decrypted Message:\n', ''.join(message)

        output = {'message': ''.join(message)}

        end = time.time()
        print 'Execution time:', end - start
        print 'Sending output ...'
        resp = self.request_handler.post_output(output)

        if 'Wrong Answer' in resp:
            print 'Wrong Answer ...'
        else:
            print 'Stage one solved ...'

    def stage_two(self):
        start = time.time()
        data = self.request_handler.get_stage_instructions()

        tools_found = []
        tools = data['tools']
        print 'Tools to search:', tools
        hidden_tools = data['hiddenTools']

        for search_tool in tools:
            found = 1
            for char in search_tool:
                if char not in hidden_tools:
                    found = 0

            if found and search_tool not in tools_found:
                tools_found.append(search_tool)

        print 'Tools found:', tools_found
        end = time.time()
        print 'Execution time:', end - start

        print 'Sending output ...'
        output = {'toolsFound': tools_found}
        resp = self.request_handler.post_output(output)

        if 'Wrong Answer' in resp:
            print 'Wrong Answer ...'
        else:
            print 'Stage two solved ...'

    def stage_three(self):
        start = time.time()
        data = self.request_handler.get_stage_instructions()

        tool_usage = data['toolUsage']
        tool_usage_list = []
        tool_usage_dict = defaultdict()
        for each_tool in tool_usage:
            if each_tool['name'] in tool_usage_dict:
                tool_usage_dict[each_tool['name']] += (datetime.strptime(each_tool['useEndTime'],
                                                              '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    each_tool['useStartTime'], '%Y-%m-%d %H:%M:%S')).total_seconds() / 60.0
            else:
                tool_usage_dict[each_tool['name']] = (datetime.strptime(each_tool['useEndTime'],
                                                                         '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    each_tool['useStartTime'], '%Y-%m-%d %H:%M:%S')).total_seconds() / 60.0

        for tools in sorted(tool_usage_dict.items(), key=lambda x: x[1], reverse=True):
            row = defaultdict(dict)

            row['name'] = tools[0]
            row['timeUsedInMinutes'] = tools[1]

            tool_usage_list.append(dict(row))

        end = time.time()
        print 'Execution time:', end - start

        print 'Sending output ...'
        output = {'toolsSortedOnUsage': tool_usage_list}
        resp = self.request_handler.post_output(output)

        if 'Wrong Answer' in resp:
            print 'Wrong Answer ...'
        else:
            print 'Stage three solved ...'

    def stage_four(self):
        data = self.request_handler.get_stage_instructions()
        start = time.time()

        tools = data['tools']

        current_weight = 0
        maximum_weight = data['maximumWeight']
        tools_to_take = []
        for each_tool in sorted(tools, key=lambda x: x['value'], reverse=True):
            if current_weight + each_tool['weight'] <= maximum_weight:
                tools_to_take.append(each_tool['name'])
                current_weight += each_tool['weight']

        end = time.time()
        print 'Execution time:', end - start

        output = {'toolsToTakeSorted': tools_to_take}
        print 'Sending output ...'
        resp = self.request_handler.post_output(output)

        if 'Wrong Answer' in resp:
            print 'Wrong Answer ...'
        else:
            print 'Stage four solved ...'


if __name__ == '__main__':
    start = LetsGo()
