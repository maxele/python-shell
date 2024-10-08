def test(args):
    print("TEST:", args)

commands = {
    'desc': 'Some commands with the purpose of testing',
    'cmds': {
        'test': {
            'func': test,
            'params': ['completion1', 'command2'],
            'desc': 'Function used for testing',
        },
        'technotest': {
            'func': test,
            'params': ['test'],
            'desc': 'A second test function',
        }
    }
}

def get_commands():
    return commands
