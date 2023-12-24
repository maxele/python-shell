# Simple Python Shell

This is a simple python shell with a few bash-like keybindings useful if you
need to create your own shell for something.

Not the cleanest code, but should be usable as a refrence or even to use as is.

## Usage

Put the commands you want to use in the `get_commands` function in the
`commands/__init__.py` file.

the commands dictionary has to have the following layout:
```Python
def test(args):
    print("TEST:", args)

commands = {
    'test': {
        'func': test,
        'params': ['completion1', 'command2'],
        'desc': 'Function used for testing',
    },
}
```
- 'func' is the function which is called with the arguments.
- 'params' are the possible values which can come after `test`.
- 'desc' is a small description for the `help` command.
