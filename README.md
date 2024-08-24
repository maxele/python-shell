# Simple Python Shell

This is a simple python shell with a few bash-like keybindings useful if you
need to create your own shell for something.

Not the cleanest code, but should be usable as a refrence or even to use as is.

## Usage

Put the modules you want to use in the `commands` directory.
Each module should implement a `get_commands()` function which should return a dict of the form:
```Python
commands = {
    'desc': <description>,
    'cmds': {
        'test': {
            'func': <function>,
            'params': <list_with_completions>,
            'desc': <description>,
        },
    }
}
```
- `<desctiption>` is a string which describes the module/command
- `<list_with_completions>` a list with word suggestions
- `<function>` a funtion which takes an single argument which contains the list of arguments
