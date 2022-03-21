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
    """Add vector registers to the TUI Window vector.
vector /OPT vector-register-list
Adds vector registers to the vector window. If a register already exists it gets updated with any new specifiers.
/OPT: x = display registers values in hex.
      c = clears vector window
      d = deletes registers from window: vector-register-list without.width or type spec.
Register format: {reg}[.width][.type]
reg:   v, b, h, s, d, q
width: b, h, s, d, q     - Width only allowed with v.
type:  f, s, u           - Type f not allowed with width b or q, or reg b or q.
vector v0.b.u v1.s.f b2.u h3.f q4.u v5 b6 s7 q8 v9.h"""

    def __init__(self):
       super(VectorCmd, self).__init__("vector", gdb.COMMAND_DATA)
       self.window = None
       self.hex = False
       self.clear = False
       self.delete = False

    def set_window(self, window):
        self.window = window

    def invoke(self, arguments, from_tty):
        if self.window:
            if len(arguments) == 0:
                print("vector /OPT vector-register-list")
                return

            try:
                self.hex = False
                self.clear = False
                self.delete = False
                offset = 0
                if arguments[0:1] == "/":
                    offset = self.parse_arguments(arguments)

                if self.clear:
                    self.window.clear_vector()
                elif self.delete:
                    argv = gdb.string_to_argv(arguments)
                    self.window.delete_vector(argv[1:])
                else:
                    self.parse_registers(arguments[offset:], self.hex)

            except SyntaxError as err:
                print(err)
                return

        else:
            print("vector: Tui Window not active yet")
            return

    def parse_arguments(self, line):
       i = 1
       if line[i] == "x":
           self.hex = True
       elif line[i] == 'd':
           self.delete = True
       elif line[i] == 'c':
           self.clear = True
           return
       else:
           raise SyntaxError(f'vector /OPT vector-register-list: Invalid option: {line[i:i + 1]}')

       # check there are registers and move ahead to 1st non space character

       ln = len(line)
       i += 1
       while i < ln:
           if line[i] == ' ': i += 1 
           else: break
        
       if i == ln:
           raise SyntaxError(f'vector /OPT vector-register-list')

       return i

    def parse_registers(self, line, hex):
        i = 0
        l = len(line)
        line += " " # make peep ahead easier
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
                        if c == 'v': 
                            i += 1
                            if line[i + 1] in width_spec:
                                i += 1
                                width = line[i:i + 1]
                            else:
                                raise SyntaxError(f"vector: invalid register {line[start:i + 2]} width specifier expected {width_spec}.")
                      
                        if line[i + 1] == ".":
                            i += 1
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
                        self.window.add_vector(reg, width, type, hex)
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

    def add_vector(self, name, width, type, hex):
        self.vector[name] = {'width': width, 'type': type, 'val': None, 'hex': hex}

    def clear_vector(self):
        self.vector.clear()

    def delete_vector(self, argv):
        for name in argv:
            try:
                del self.vector[name]
            except:
                print(f"vector /d: {name} not found.")

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
            hint = BLUE if attr['val'] != val  else WHITE
            self.vector[name]['val'] = val

            width = attr['width']
            type = attr['type']

            if attr['hex']:
                type = 'u' if type == 'f' else type
                if width:
                    st = val[width][type].format_string(format='z', repeat_threshold=0) if type else val[width].format_string(format='z')
                else:
                    st = val[type].format_string(format='z') if type else val.format_string(format='z')
            else:
                if width:
                    st = val[width][type].format_string(repeat_threshold=0) if type else val[width]
                else:
                    st = val[type] if type else val

            self.list.append(f'{GREEN}{name:<5}{hint}{st}{RESET}{NL}')

        self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.create_vector)
        VectorWindow.save_vector = self.vector

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()
        for l in self.list[self.start:]:
            self.tui.write(l)

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            self.render()

gdb.register_window_type("vector", VectorWinFactory)
