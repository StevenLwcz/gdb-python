.text

.globl _start
_start:
        //     1C98765*32*B987654321A9876543210
    mov x1, #0b00000000000000000000000000000000 // round to neariest tie zero
    mov x2, #0b00000000010000000000000000000000 // + inf (ceil)
    mov x3, #0b00000000100000000000000000000000 // - inf (floor)
    mov x4, #0b00000000110000000000000000000000 // truncate

    msr fpcr, x1
    msr fpcr, x2
    msr fpcr, x3
    msr fpcr, x4

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          

.data
