import logging
import os
import time
import argparse

#import GPT.machine_id
#import GPT.tune as tune

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')

class GPTService():
    def __init__(self, args):
        logging.info('Initializing ChatGPT Service...')
        self.chatVer = args.chatVer

        if self.chatVer == 1:
            from revChatGPT.V1 import Chatbot
            config = {}
            if args.accessToken:
                logging.info('Try to login with access token.')
                config['access_token'] = args.accessToken

            else:
                logging.info('Try to login with email and password.')
                config['email'] = args.email
                config['password'] = args.password
            config['paid'] = args.paid
            config['model'] = args.model
            if type(args.proxy) == str:
                config['proxy'] = args.proxy

            self.chatbot = Chatbot(config=config)
            logging.info('WEB Chatbot initialized.')


        elif self.chatVer == 3:
            mach_id = GPT.machine_id.get_machine_unique_identifier()
            from revChatGPT.V3 import Chatbot
            if args.APIKey:
                logging.info('you have your own api key. Great.')
                api_key = args.APIKey
            else:
                logging.info('using custom API proxy, with rate limit.')
                os.environ['API_URL'] = "https://api.geekerwan.net/chatgpt2"
                api_key = mach_id

            self.chatbot = Chatbot(api_key=api_key, proxy=args.proxy, system_prompt=self.tune)
            logging.info('API Chatbot initialized.')

    def ask(self, text):
        stime = time.time()
        if self.chatVer == 3:
            prev_text = self.chatbot.ask(text)

        # V1
        elif self.chatVer == 1:
            for data in self.chatbot.ask(
                    text
            ):
                prev_text = data["message"]

        logging.info('ChatGPT Response: %s, time used %.2f' % (prev_text, time.time() - stime))
        return prev_text

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chatVer", type=int, nargs='?', required=False)
    parser.add_argument("--APIKey", type=str, nargs='?', required=False)
    parser.add_argument("--email", type=str, nargs='?', required=False)
    parser.add_argument("--password", type=str, nargs='?', required=False)
    parser.add_argument("--accessToken", type=str, nargs='?', required=False)
    parser.add_argument("--proxy", type=str, nargs='?', required=False)
    parser.add_argument("--paid", type=str2bool, nargs='?', required=False)
    parser.add_argument("--model", type=str, nargs='?', required=False)
    parser.add_argument("--stream", type=str2bool, nargs='?', required=False)
    parser.add_argument("--character", type=str, nargs='?', required=False)
    parser.add_argument("--ip", type=str, nargs='?', required=False)
    parser.add_argument("--brainwash", type=str2bool, nargs='?', required=False)
    return parser.parse_args()

args = parse_args()

args.accessToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJndWtlZGV1dHNjaEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1ZRjJDUEVQZFFJblJqVksweHNoOXg3SjMifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExOTY2MTE4NTI5ODMwMzE4NzEyIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5NTQzNTk1MCwiZXhwIjoxNjk2NjQ1NTUwLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.DEhPB7eq6m_2avgJ_FTmynYW1vggnPkdoTJviAPU65IU9Zx_61LHg7thO7D3k2F-pz0WBx4prwoD390p_JIDpHkQQ6A5z0QituKCpvQs3sY416EnGV3hVNthVKcml2aiLt5FngEVk2DeK-IOvE5NHoacJocBzt5XGy6GrTHdIlNo6Bbpj3ZM27Rpw5xshUqKTYX3-CNgfvXhzPwF2JrLTWbJPi7vm9Qv1nA1fniXc4McLR0EW6PXLKdUD-zlsvP-UP7F7Q21S7PdY0syj7IPpNaLMPOmH93spfPUz9Ax6TzQDj57zSIWDigf7xYD20Z0mCK06etFKDpkvcitAitxqA"
args.chatVer = 1

ask_text = "hello world, I love you forever!"

GPT_Client = GPTService(args)

for sentence in GPT_Client.ask(ask_text):
    print(sentence)