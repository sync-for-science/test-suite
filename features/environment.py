import configparser

def before_all(context):
    config = configparser.ConfigParser()
    config.read('behave.ini')

    context.api_url = config['api']['url']
    context.patient = config['api']['patient']

    context.auth = dict(config['auth'])
