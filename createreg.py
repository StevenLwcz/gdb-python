print("registers = {", end='')
first=True
index = 0
for r in ['x', 'b', 'h', 's', 'd', 'q', 'v', 'r']:
    for num in range(0,32):
        if r == 'x' and num == 31:
            continue
        if r == 'r' and num > 12:
            continue

        if first:
            print(f'       "{r}{num}": {index}', end='')
            first=False
        else:
            print(f', "{r}{num}": {index}', end='')

        if num == 8 or num == 16 or num == 24:
            print(",")
            first = True

        index += 1

    print(",")
    first = True

for r in ['lr', 'pc', 'sp', 'cpsr', 'fpsr', 'fpcr', 'fpscr']:
   if first:
       print(f'       "{r}": {index}', end='')
       first=False
   else:
       print(f', "{r}": {index}', end='')
   index += 1

print("}")

