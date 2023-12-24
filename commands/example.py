def test(args):
    print("TEST:", args)

commands = {
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

def getcommands():
    return commands
