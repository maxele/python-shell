def get_commands():
    cmds = {}
    import example
    # TODO: Check if command is alaready defined
    cmds.update(example.get_commands())
    return cmds
