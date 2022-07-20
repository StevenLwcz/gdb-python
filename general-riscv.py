#--------------------------
# Colours

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;15m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n"

#--------------------------
# Register list

reg_rv64 = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8,
       "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16,
       "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24,
       "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, 
       "ra": 32, "sp": 33, "gp": 34, "tp": 35, "t0": 36, "t1": 37, "t2": 38, "t3": 39, "t4": 40,
       "t5": 41, "t6": 42, "fp": 43, "s0": 44, "s1": 45, "s2": 46, "s3": 47, "s4": 48, "s5": 49,
       "s6": 50, "s7": 51, "s8": 52, "s9": 53, "s10": 54, "s11": 55, 
       "a0": 56, "a1": 57, "a2": 58, "a3": 59, "a4": 60, "a5": 61, "a6": 62, "a7": 63,
       "pc": 255}

registers = reg_rv64

#--------------------------
# class view of registers for formatting

class Register(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.val = None
        self.fmt = 'd'
        self.colour = WHITE

    @classmethod
    def Factory(self, name):
        try:
            if name[1:2].isdigit():
                return reg_class[name[0:1]](name)
            else:
                return reg_special[name](name)
        except:
            raise BasicException("Invalid Register")

    def __format__(self, format_spec):
        return self.colour + format(str(self), format_spec)
         
    def __str__(self):
        return self.val.format_string(format=self.fmt)

    def value(self):
        val = Register.frame.read_register(self.name)
        self.colour = BLUE if self.val != val else WHITE
        self.val = val
        return self.val

class XReg(Register):
    pass

class LRReg(Register):

    def __str__(self):
        return self.val.format_string()

class PCReg(Register):

    def __str__(self):
        return self.val.format_string()

class SPReg(Register):

    def __str__(self):
        return self.val.format_string()

reg_class = {'x': XReg, 'a': XReg, 't': XReg, 's': XReg}
reg_special = {'ra': LRReg, 'pc': PCReg, 'sp': SPReg, 'gp': LRReg, 'fp': LRReg, "tp": LRReg}

#--------------------------
# Register command and Register Window

class RegisterCmd(gdb.Command):
    """Add registers to the custom TUI Window register.
register OPT|/FMT register-list
/FMT: x: hex, z: zero pad hex, s: signed, u: unsigned, f: float, c: char, a: address
OPT: del register-list
     clear - clear all registers from the window
     save filename - save register-list to file (use so filename to read back)
Ranges can be specified with -"""

    def __init__(self):
        self.__doc__ += "\nregister x0 - x31 a0 - a7 t0 - t6 s0 - s11\nSpecial registers: ra, pc, sp, fp, gp, tp"
 
        super(RegisterCmd, self).__init__("register", gdb.COMMAND_DATA)
        self.win = None

    def set_win(self, win):
        self.win = win

    def invoke(self, arguments, from_tty):
        if self.win == None:
            print("register: Tui Window not active.")
            return
     
        reg_list = []
        prev = None
        expand = False
        delete = False
        format = None

        args = gdb.string_to_argv(arguments)
        argc = len(args)
        if argc == 0:
            print("register register-list")
            return
        elif args[0][0:1] == '/':
            if argc > 1:
                f = args[0][1:2]
                if f in ['x', 'z', 's', 'u', 'f', 'c', 'a']:
                    format = 'd' if f == 's' else f
                else:
                    print(f'register /FMT: x, z, s, u, f, c or a expected: {f}')
                    return
                del args[0]
            else:
                print(f'register /FMT register-list')
                return
        elif args[0] == "clear":
            self.win.clear_registers()
            return
        elif args[0] == "del":
            if argc > 1:
                delete = True
                del args[0]
            else:
                print("register del register-list")
                return
        elif args[0] == 'save':
            if argc == 2:
                self.win.save_registers(args[1])
                return
            else:
                print("register save filename")
                return
            
        for reg in args:
            if reg == "-":
                expand = True
                continue
            elif not reg in registers:
                print("register: invalid register %s" % reg)
                return

            if expand:
                if prev == None:
                    print("register: no start to range")
                    return
                start = registers[prev] 
                finish = registers[reg]
                reg_list.extend([k for k, v in registers.items() if v > start and v <= finish])
                expand = False
            else: 
                prev = reg
                reg_list.append(reg)

        if delete:
            self.win.del_registers(reg_list)
        elif format is not None:
            self.win.format_registers(reg_list, format)
        else:
            self.win.add_registers(reg_list)

regWinCmd = RegisterCmd()

def RegisterFactory(tui):
    win = RegisterWindow(tui)
    gdb.events.before_prompt.connect(win.create_register)
    regWinCmd.set_win(win)
    return win

class RegisterWindow(object):

    regs_save = {}

    def __init__(self, tui):
        self.tui = tui
        tui.title = "Registers"
        self.regs = RegisterWindow.regs_save
        self.start = 0
        self.tui_list = []

    def add_registers(self, list):
        for name in list:
            if not name in self.regs:
                try:
                    self.regs[name] = Register.Factory(name)
                except:
                    print(f'register: invalid register {name}.')
            
    def del_registers(self, list):
        for name in list:
            try:
                del self.regs[name]
            except:
               print(f'register del {name} not found')

    def format_registers(self, args, format):
        for name in args:
            if not name in self.regs:
                self.add_registers([name])

            self.regs[name].fmt = format

    def clear_registers(self):
        self.regs.clear()

    def save_registers(self, filename):
        try:
            with open(filename, "w") as f:
                for name in self.regs:
                    f.write(f'reg {name}\n')
                    print(f'reg {name}')
        except IOError:
            print(f'reg: could not write to {filename}')

    def close(self):
        RegisterWindow.regs_save = self.regs
        gdb.events.before_prompt.disconnect(self.create_register)

    def render(self):
        if not self.tui.is_valid():
            return

        self.tui.erase()

        for l in self.tui_list[self.start:]:
            self.tui.write(l)

    def create_register(self):
        self.tui_list = []

        if not self.tui.is_valid():
            return
        
        try:
            Register.frame = gdb.selected_frame()
        except gdb.error:
            self.start = 0
            self.title = "No Frame"
            self.tui_list.append("No frame currently selected" + NL)
            self.render()
            return
        
        width = self.tui.width
        line = ""

        for name, reg in self.regs.items():
            reg.value()

            if width < 29:
                line += NL
                self.tui_list.append(line)
                line = ""
                width = self.tui.width

            line += f'{GREEN}{name:<5}{reg:<24}{RESET}'
            width -= 29

        if line != "":
            line += NL
            self.tui_list.append(line)

        self.render()

    def vscroll(self, num):
        if num > 0 and num + self.start < len(self.tui_list) or \
           num < 0 and num + self.start >= 0:
            self.start += num
            self.render()

gdb.register_window_type("register", RegisterFactory)
