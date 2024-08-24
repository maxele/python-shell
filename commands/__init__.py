# def get_commands():
#     cmds = {}
#     import commands.example
#     # TODO: Check if command is alaready defined
#     cmds.update({'example': commands.example.get_commands()})
#     return cmds
#
import os
import importlib

def get_commands():
    potential_modules = os.listdir('./commands')
    if '__init__.py' in potential_modules:
        potential_modules.remove('__init__.py')
    if '__pycache__' in potential_modules:
        potential_modules.remove('__pycache__')

    modules = {}
    for pm in potential_modules:
        if pm.endswith('.py'):
            m = importlib.import_module('commands.'+pm[:-3])
            modules.update({pm[:-3]: m.get_commands()})
        elif os.path.isdir('./commands/'+pm):
            m = importlib.import_module('commands.'+pm)
            modules.update({pm: m.get_commands()})
    return modules
