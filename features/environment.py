import configparser

def before_all(context):
    config = configparser.ConfigParser()
    config.read('behave.ini')

    context.api_url = config['api']['url']
    context.auth = dict(config['auth'])
