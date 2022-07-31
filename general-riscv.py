#--------------------------
# Colours

GREEN = "\x1b[38;5;47m"
BLUE  = "\x1b[38;5;14m"
WHITE = "\x1b[38;5;255m"
GREY  = "\x1b[38;5;246m"
RESET = "\x1b[0m"
NL = "\n"

#--------------------------
# Register list


reg_rv64 = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, 
"x8": 8, "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, 
"x16": 16, "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, 
"x24": 24, "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, 
"a0": 32, "a1": 33, "a2": 34, "a3": 35, "a4": 36, "a5": 37, "a6": 38, "a7": 39, 
"s0": 40, "s1": 41, "s2": 42, "s3": 43, "s4": 44, "s5": 45, "s6": 46, "s7": 47, 
"s8": 48, "s9": 49, "s10": 50, "s11": 51, "t0": 52, "t1": 53, "t2": 54, "t3": 55, 
"t4": 56, "t5": 57, "t6": 58, "t7": 59, "t8": 60, "t9": 61, "t10": 62, "t11": 63, 
"f0": 64, "f1": 65, "f2": 66, "f3": 67, "f4": 68, "f5": 69, "f6": 70, "f7": 71, 
"f8": 72, "f9": 73, "f10": 74, "f11": 75, "f12": 76, "f13": 77, "f14": 78, "f15": 79, 
"f16": 80, "f17": 81, "f18": 82, "f19": 83, "f20": 84, "f21": 85, "f22": 86, "f23": 87, 
"f24": 88, "f25": 89, "f26": 90, "f27": 91, "f28": 92, "f29": 93, "f30": 94, "f31": 95, 
"fa0": 96, "fa1": 97, "fa2": 98, "fa3": 99, "fa4": 100, "fa5": 101, "fa6": 102, "fa7": 103, 
"fs0": 104, "fs1": 105, "fs2": 106, "fs3": 107, "fs4": 108, "fs5": 109, "fs6": 110, "fs7": 111, 
"fs8": 112, "fs9": 113, "fs10": 114, "fs11": 115, "ft0": 116, "ft1": 117, "ft2": 118, "ft3": 119, 
"ft4": 120, "ft5": 121, "ft6": 122, "ft7": 123, "ft8": 124, "ft9": 125, "ft10": 126, "ft11": 127, 
"f0.s": 128, "f1.s": 129, "f2.s": 130, "f3.s": 131, "f4.s": 132, "f5.s": 133, "f6.s": 134, "f7.s": 135, 
"f8.s": 136, "f9.s": 137, "f10.s": 138, "f11.s": 139, "f12.s": 140, "f13.s": 141, "f14.s": 142, "f15.s": 143, 
"f16.s": 144, "f17.s": 145, "f18.s": 146, "f19.s": 147, "f20.s": 148, "f21.s": 149, "f22.s": 150, "f23.s": 151, 
"f24.s": 152, "f25.s": 153, "f26.s": 154, "f27.s": 155, "f28.s": 156, "f29.s": 157, "f30.s": 158, "f31.s": 159, 
"fa0.s": 160, "fa1.s": 161, "fa2.s": 162, "fa3.s": 163, "fa4.s": 164, "fa5.s": 165, "fa6.s": 166, "fa7.s": 167, 
"fs0.s": 168, "fs1.s": 169, "fs2.s": 170, "fs3.s": 171, "fs4.s": 172, "fs5.s": 173, "fs6.s": 174, "fs7.s": 175, 
"fs8.s": 176, "fs9.s": 177, "fs10.s": 178, "fs11.s": 179, "ft0.s": 180, "ft1.s": 181, "ft2.s": 182, "ft3.s": 183, 
"ft4.s": 184, "ft5.s": 185, "ft6.s": 186, "ft7.s": 187, "ft8.s": 188, "ft9.s": 189, "ft10.s": 190, "ft11.s": 191, 
"ra": 192, "sp": 193, "gp": 194, "fp": 195, "pc": 255}

registers = reg_rv64

#--------------------------
# class view of registers for formatting

class Register(object):

    frame = None

    def __init__(self, name):
        self.name = name
        self.val = None
        self.fmt = None
        self.colour = WHITE

    @classmethod
    def Factory(self, name):
        try:
            return reg_rv64_class[name](name)
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

class XReg(Register):

    def __init__(self, name):
        super().__init__(name)
        self.fmt = 'd'

class AdReg(Register):

    def __init__(self, name):
        super().__init__(name)
        self.fmt = 'a'

class FSReg(Register):

    def __init__(self, name):
        f = name.find('.')
        name = name[0:f]
        print(name)
        super().__init__(name)
        self.fmt = 'f'

    def __str__(self):
        return self.val['float'].format_string(format=self.fmt)

class FDReg(Register):

    def __init__(self, name):
        super().__init__(name)
        self.fmt = 'f'

    def __str__(self):
        return self.val['double'].format_string(format=self.fmt)

reg_rv64_class = {"x0": XReg, "x1": XReg, "x2": XReg, "x3": XReg, "x4": XReg, "x5": XReg, "x6": XReg, "x7": XReg, 
"x8": XReg, "x9": XReg, "x10": XReg, "x11": XReg, "x12": XReg, "x13": XReg, "x14": XReg, "x15": XReg, 
"x16": XReg, "x17": XReg, "x18": XReg, "x19": XReg, "x20": XReg, "x21": XReg, "x22": XReg, "x23": XReg, 
"x24": XReg, "x25": XReg, "x26": XReg, "x27": XReg, "x28": XReg, "x29": XReg, "x30": XReg, "x31": XReg, 
"a0": XReg, "a1": XReg, "a2": XReg, "a3": XReg, "a4": XReg, "a5": XReg, "a6": XReg, "a7": XReg, 
"s0": XReg, "s1": XReg, "s2": XReg, "s3": XReg, "s4": XReg, "s5": XReg, "s6": XReg, "s7": XReg, 
"s8": XReg, "s9": XReg, "s10": XReg, "s11": XReg, "t0": XReg, "t1": XReg, "t2": XReg, "t3": XReg, 
"t4": XReg, "t5": XReg, "t6": XReg, "t7": XReg, "t8": XReg, "t9": XReg, "t10": XReg, "t11": XReg, 
"f0": FDReg, "f1": FDReg, "f2": FDReg, "f3": FDReg, "f4": FDReg, "f5": FDReg, "f6": FDReg, "f7": FDReg, 
"f8": FDReg, "f9": FDReg, "f10": FDReg, "f11": FDReg, "f12": FDReg, "f13": FDReg, "f14": FDReg, "f15": FDReg, 
"f16": FDReg, "f17": FDReg, "f18": FDReg, "f19": FDReg, "f20": FDReg, "f21": FDReg, "f22": FDReg, "f23": FDReg, 
"f24": FDReg, "f25": FDReg, "f26": FDReg, "f27": FDReg, "f28": FDReg, "f29": FDReg, "f30": FDReg, "f31": FDReg, 
"fa0": FDReg, "fa1": FDReg, "fa2": FDReg, "fa3": FDReg, "fa4": FDReg, "fa5": FDReg, "fa6": FDReg, "fa7": FDReg, 
"fs0": FDReg, "fs1": FDReg, "fs2": FDReg, "fs3": FDReg, "fs4": FDReg, "fs5": FDReg, "fs6": FDReg, "fs7": FDReg, 
"fs8": FDReg, "fs9": FDReg, "fs10": FDReg, "fs11": FDReg, "ft0": FDReg, "ft1": FDReg, "ft2": FDReg, "ft3": FDReg, 
"ft4": FDReg, "ft5": FDReg, "ft6": FDReg, "ft7": FDReg, "ft8": FDReg, "ft9": FDReg, "ft10": FDReg, "ft11": FDReg, 
"f0.s": FSReg, "f1.s": FSReg, "f2.s": FSReg, "f3.s": FSReg, "f4.s": FSReg, "f5.s": FSReg, "f6.s": FSReg, "f7.s": FSReg, 
"f8.s": FSReg, "f9.s": FSReg, "f10.s": FSReg, "f11.s": FSReg, "f12.s": FSReg, "f13.s": FSReg, "f14.s": FSReg, "f15.s": FSReg, 
"f16.s": FSReg, "f17.s": FSReg, "f18.s": FSReg, "f19.s": FSReg, "f20.s": FSReg, "f21.s": FSReg, "f22.s": FSReg, "f23.s": FSReg, 
"f24.s": FSReg, "f25.s": FSReg, "f26.s": FSReg, "f27.s": FSReg, "f28.s": FSReg, "f29.s": FSReg, "f30.s": FSReg, "f31.s": FSReg, 
"fa0.s": FSReg, "fa1.s": FSReg, "fa2.s": FSReg, "fa3.s": FSReg, "fa4.s": FSReg, "fa5.s": FSReg, "fa6.s": FSReg, "fa7.s": FSReg, 
"fs0.s": FSReg, "fs1.s": FSReg, "fs2.s": FSReg, "fs3.s": FSReg, "fs4.s": FSReg, "fs5.s": FSReg, "fs6.s": FSReg, "fs7.s": FSReg, 
"fs8.s": FSReg, "fs9.s": FSReg, "fs10.s": FSReg, "fs11.s": FSReg, "ft0.s": FSReg, "ft1.s": FSReg, "ft2.s": FSReg, "ft3.s": FSReg, 
"ft4.s": FSReg, "ft5.s": FSReg, "ft6.s": FSReg, "ft7.s": FSReg, "ft8.s": FSReg, "ft9.s": FSReg, "ft10.s": FSReg, "ft11.s": FSReg, 
"ra": AdReg, "sp": AdReg, "gp": AdReg, "fp": AdReg, "pc": AdReg}

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
                if f in ['x', 'z', 's', 'u', 'f', 'c', 'a', 't']:
                    format = 'd' if f == 's' else f
                else:
                    print(f'register /FMT: x, z, s, u, f, c, a or t expected: {f}')
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

            line += f'{GREEN}{name:<5}{reg:<24}'
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
