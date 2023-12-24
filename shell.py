import keyboard
import sys, tty, termios

def get_commands():
    cmds = {}
    import commands.example
    # TODO: Check if command is alaready defined
    cmds.update(commands.example.getcommands())
    return cmds

conv = { 1: 'Ctrl-A', 2: 'Ctrl-B', 3: 'Ctrl-C', 4: 'Ctrl-D', 5: 'Ctrl-E', 6:
        'Ctrl-F', 7: 'Ctrl-G', 8: 'Ctrl-H', 9: 'Ctrl-I', 10: 'Ctrl-J', 11:
        'Ctrl-K', 12: 'Ctrl-L', 13: 'Return', 14: 'Ctrl-N', 15: 'Ctrl-O', 16:
        'Ctrl-P', 17: 'Ctrl-Q', 18: 'Ctrl-R', 19: 'Ctrl-S', 20: 'Ctrl-T', 21:
        'Ctrl-U', 22: 'Ctrl-V', 23: 'Ctrl-W', 24: 'Ctrl-X', 25: 'Ctrl-Y', 26:
        'Ctrl-Z', 27: 'Escape', 127: 'Backspace' }
reverse_conv = {v: k for k, v in conv.items()}

def isvalidchar(c):
    return type(c) == int and c >= 32 and c <= 122

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def eline(l, cmds):
    cmd = l.strip().split(' ')
    if cmd[0] == 'help':
        print()
        for cmd in cmds:
            print(f"{cmd:16s} {cmds[cmd]['desc']}")
    elif cmd[0] in cmds:
        print()
        cmds[cmd[0]]['func'](cmd[1:])
    else:
        print('\nUNKNOWN INPUT:', l)
    #print('\nBAZAAR_SCRIPT:', bazaar_script(l))

def get_escaped_sequence():
    c = getch()
    if c == '[':
        return c + getch()
    elif ord(c) in conv:
        return 'Alt-' + conv[ord(c)]
    elif isvalidchar(ord(c)):
        return 'Alt-' + c
    else:
        return c + getch()

def delchar(s, pos):
    if pos == 0: return s
    return s[:pos-1] + s[pos:]

def inschar(s, pos, c):
    return s[:pos] + c + s[pos:]

def overlap(a, b):
    r = ''
    for c in range(min(len(a), len(b))):
        if a[c] != b[c]: return r
        r += a[c]
    return r
def complete(s, cmds, cmd):
    if cmd != None:
        cmds = cmds[cmd]['params']

    ls = None
    similarcount = 0
    for i in cmds:
        if i.startswith(s):
            if ls == None: ls = i
            else:
                ls = overlap(ls, i)
                similarcount += 1
    if ls == None: return s
    elif ls == s and similarcount >= 1:
        print()
        for cmd in cmds:
            if cmd.startswith(s):
                print(cmd)
    return ls

def shell(v = False):
    cmds = {
        'help': {
            'func': None,
            'complete': None,
            'desc': 'Print help for all commands',
        }
    }
    cmds.update(get_commands())

    keybinds = {
            reverse_conv['Return']: 'Submit',
            reverse_conv['Backspace']: 'Delete',
            reverse_conv['Ctrl-C']: 'Exit',
            reverse_conv['Ctrl-D']: 'Exit',

            reverse_conv['Ctrl-I']: 'Complete',
            reverse_conv['Ctrl-L']: 'Clear',

            reverse_conv['Ctrl-A']: 'Home',
            reverse_conv['Ctrl-E']: 'End',
            reverse_conv['Ctrl-B']: 'BackChar',
            'Alt-f': 'ForwardWord',
            'Alt-b': 'BackWord',
            reverse_conv['Ctrl-K']: 'KillLine',
            reverse_conv['Ctrl-F']: 'ForwardChar',
            reverse_conv['Ctrl-P']: 'HistoryUp',
            reverse_conv['Ctrl-N']: 'HistoryDown',
            '[H': 'Home',
            '[F': 'End',
            '[C': 'ForwardChar',
            '[D': 'BackChar',
            '[A': 'HistoryUp',


            '[B': 'HistoryDown',
    }

    buf = ''
    cursor = 0

    history = ['']
    hindex = 0

    print(end='> ', flush=True)
    while c := ord(getch()):
        if c == reverse_conv['Escape']:
            c = get_escaped_sequence()

        if c in keybinds:
            #print(keybinds[c])
            match keybinds[c]:
                case 'Exit':
                    print()
                    print("BYE!")
                    break
                case 'Submit':
                    if buf.strip() != '':
                        eline(buf, cmds)
                        history[-1] = buf
                        history.append('')
                        hindex = len(history)-1
                    buf = ''
                    cursor = 0
                case 'Delete':
                    buf = delchar(buf, cursor)
                    if cursor > 0: cursor -= 1
                case 'Complete':
                    i = cursor
                    while i > 0 and buf[i-1] != ' ': i -= 1
                    cmd = None
                    if buf[:i].strip() != '':
                        cmd = buf.strip().split(' ')[0].strip()
                    compl = complete(buf[i:cursor], cmds, cmd)
                    #print(buf[i:cursor], compl)
                    cursor += len(compl) - (cursor-i)
                    buf = buf[:i] + compl + buf[cursor:]
                case 'Clear':
                    print(end='\033[2J\033[1;0H')
                case 'Home':
                    cursor = 0
                case 'End':
                    cursor = len(buf)
                case 'BackChar':
                    if cursor > 0: cursor -= 1
                case 'KillLine':
                    buf = buf[:cursor]
                case 'ForwardChar':
                    if cursor < len(buf): cursor += 1
                case 'BackWord':
                    if cursor == len(buf): cursor -= 1
                    if buf[cursor] != ' ': cursor -= 1
                    while cursor > 0 and buf[cursor] == ' ':
                        cursor -= 1
                    while cursor > 0 and buf[cursor] != ' ':
                        cursor -= 1
                    if cursor > 1 and cursor < len(buf): cursor += 1
                case 'ForwardWord':
                    if cursor == len(buf): cursor -= 1
                    if buf[cursor] != ' ': cursor -= 1
                    while cursor < len(buf) and buf[cursor] == ' ':
                        cursor += 1
                    while cursor < len(buf) and buf[cursor] != ' ':
                        cursor += 1
                    if cursor > 1 and cursor < len(buf): cursor += 1
                case 'HistoryUp':
                    if hindex > 0: hindex -= 1
                    buf = history[hindex]
                    cursor = len(buf)
                case 'HistoryDown':
                    if hindex < len(history)-1: hindex += 1
                    buf = history[hindex]
                    cursor = len(buf)
                case _:
                    if v: print('Unimplemented:', keybinds[c])
        elif c in conv:
            if v: print('\nUnbound:', conv[c], reverse_conv[conv[c]])

        elif isvalidchar(c):
            buf = inschar(buf, cursor, chr(c))
            cursor += 1
        else:
            if v: print('\nUnknown:', c)
        print('\r> ' + buf + '\033[K' + '\033[D' * (len(buf)-cursor), end='', flush=True)

if __name__ == '__main__':
    shell(v=False)
