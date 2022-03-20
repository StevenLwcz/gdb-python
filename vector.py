GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n\n"

reg_spec = ['v', 'b', 'h', 's', 'd', 'q']
width_spec = ['d', 's', 'b', 'q', 'h']
type_spec = ['f', 's', 'u']

class VectorCmd(gdb.Command):
    """Add vector registers to the TUI Window vector."""

    def __init__(self):
       super(VectorCmd, self).__init__("vector", gdb.COMMAND_DATA)
       self.window = None

    def set_window(self, window):
        self.window = window

    def invoke(self, arguments, from_tty):
        if self.window:
            if len(arguments) == 0:
                print("vector vector-register-list")
                return

            arguments += " "
            try:
                ret = self.parse_arguments(arguments)
            except SyntaxError as err:
                print(err)
                return

        else:
            print("vector: Tui Window not active yet")
            return

    # to do del, clear
    def parse_arguments(self, line):
        i = 0
        l = len(line) - 1
        while i < l:
            start = i
            c = line[i]
 
            if c in reg_spec:
                reg = None
                width = None
                type  = None

                if line[i + 1].isdigit():
                    i += 1
                    while line[i + 1].isdigit():
                        i += 1
 
                    if int(line[start + 1:i + 1]) > 31:
                        raise SyntaxError(f"vector: invalid register {line[start:i + 1]} > 31")
                  
                    reg = line[start:i + 1]

                    if line[i + 1] == ".":
                        i += 1
                        if c == 'v': 
                            if line[i + 1] in width_spec:
                                i += 1
                                width = line[i:i + 1]
                                if line[i + 1] == ".":
                                    i += 1
                                else:
                                    raise SyntaxError(f"vector: invalid register {line[start:i + 1]} . expected.")
                            else:
                                raise SyntaxError(f"vector: invalid register {line[start:i + 2]} width specifier expected {width_spec}.")
                      
                        if line[i + 1] in type_spec: 
                            i += 1
                            type = line[i:i + 1]
                            if (c == 'q' or c == 'b') and type == 'f':
                                raise SyntaxError(f"vector: {line[start:i + 1]} type specifier 'f' not valid with {c}.")
                            if (c == 'v' and (width == 'q' or width == 'b')) and type == 'f':
                                raise SyntaxError(f"vector: {line[start:i + 1]} type specifier 'f' not valid with {width}.")
                        else:
                            raise SyntaxError(f"vector: invalid register {line[start:i + 2]} type specifier expected {type_spec}.")

                    if line[i + 1] == ' ':
                        i += 1
                        self.window.add_vector(reg, width, type)
                    else:
                        raise SyntaxError(f"vector: invalid register {line[start:i + 2]} space excepted.")
                else:
                    raise SyntaxError(f"vector: invalid register {line[start:i + 1]} number expected.")
            elif c == ' ':
                i += 1
            else: 
                raise SyntaxError(f"vector: invalid register {line[start:]} register letter expected {reg_spec}.")

            i += 1
            

vectorCmd = VectorCmd()

def VectorWinFactory(tui):
    win = VectorWindow(tui)
    vectorCmd.set_window(win)
    gdb.events.before_prompt.connect(win.create_vector)
    return win

class VectorWindow(object):

    save_vector = {}

    def __init__(self, tui):
        self.tui = tui
        self.vector = VectorWindow.save_vector
        self.tui.title = "Vector Registers"
        self.start = 0
        self.list = []

    def add_vector(self, name, width, type):
        self.vector[name] = {'width': width, 'type': type, 'val': None, 'hex': False}

    def create_vector(self):
        self.list = []

        try:
            frame = gdb.selected_frame()
        except gdb.error:
            self.title = "No Frame"
            self.list.append("No frame currently selected" + NL)
            self.render()
            return

        for name, attr in self.vector.items():
            val = frame.read_register(name)

            width = attr['width']
            type = attr['type']
            if width:
                self.list.append(f'{GREEN}{name}  {WHITE}{val[width][type]}{RESET}{NL}')
            elif type:
                self.list.append(f'{GREEN}{name}  {WHITE}{val[type]}{RESET}{NL}')
            else:
                self.list.append(f'{GREEN}{name}  {WHITE}{val}{RESET}{NL}')

        self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.create_vector)
        VectorWindow.save_watch = self.watch

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()
        for l in self.list[self.start:]:
            self.tui.write(l)

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start > 0:
            self.start += num
            self.render()

gdb.register_window_type("vector", VectorWinFactory)
