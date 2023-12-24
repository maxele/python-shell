def get_commands():
    cmds = {}
    import commands.example
    # TODO: Check if command is alaready defined
    cmds.update(commands.example.get_commands())
    return cmds
