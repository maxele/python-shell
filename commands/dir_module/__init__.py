def shell_module(args):
    print("SHELL_MODULE:", args)

commands = {
    'desc': 'An example module in the form of a directory',
    'cmds': {
        'shell_module': {
            'func': shell_module,
            'params': ['test'],
            'desc': 'A module testing function',
        }
    }
}

def get_commands():
    return commands
