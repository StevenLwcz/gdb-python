  .cpu cortex-a76

.text

.globl _start

_start:

    // integer vector

    ldr x0, =num1
    ldr q0, [x0]
    ldr x0, =num2
    ldr q1, [x0]

    add v2.16b, v1.16b, v0.16b   // 8 bit
    add v2.8b,  v1.8b,  v0.8b    // 8 bit

    ldr x0, =num3
    ldr q3, [x0]
    ldr x0, =num4
    ldr q4, [x0]

    add v5.8h, v3.8h, v4.8h    // 16 bit
    add v5.4h, v3.4h, v4.4h    // 16 bit

    ldr x0, =num5
    ldr q6, [x0]
    ldr x0, =num6
    ldr q7, [x0]

    add v8.4s, v6.4s, v7.4s    // 32 bit
    add v8.2s, v6.2s, v7.2s    // 32 bit

    ldr x0, =num7
    ldr q9, [x0]
    ldr x0, =num8
    ldr q10, [x0]

    add v11.2d, v9.2d, v10.2d    // 64 bit

    // single element moves - uses ins
    // only replaces the element leaving the rest of the vector untouched

    mov v2.b[1], v0.b[15]
    mov v5.h[2], v3.h[7]
    mov v8.s[3], v6.s[3]
    mov v11.d[1], v9.d[0]

    // single element moves - uses dup
    // will set the rest of the vector register to zero

    mov b2, v0.b[0]
    mov h5, v3.h[3]
    mov s8, v6.s[2]
    mov d11, v9.d[0]

    // general register moves

    mov x0, 1234          // movz
    mov v8.s[1], w0       // ins
    mov v11.d[1], x0      // ins
    umov w0, v6.s[1]      // has mov alias
    umov x0, v9.d[1]      // has mov alias

    // dup fills all vector elements with source (no mov alias)

    dup v2.16b, v0.b[4]
    dup v5.8h, v3.h[3]
    dup v8.4s, v6.s[2]
    dup v11.2d, v9.d[1]

    mov x0, 5678            
    dup v8.4s, w0
    dup v11.2d, x0

    // vector register to vector register

    mov v2.16b, v0.16b
    mov v2.8b,  v1.8b

    // from immediates - fills vector - no mov alias

    movi v0.16b, 100
    movi v3.8h,  127
    movi v6.4s,  255
    movi v9.2d,  0

    // floatng point vector

    // from immediates

    fmov v12.8h, 1.0
    fmov v13.4h, 2.0
    fmov v15.4s, 1.0
    fmov v16.2s, 2.0
    fmov v18.2d, 1.0

    // from memory

    ldr x0, =num9 
    ld1 {v12.8h, v13.8h}, [x0]

    fadd v14.8h, v13.8h, v12.8h
    fadd v14.4h, v13.4h, v12.4h

    ldr x0, =num11
    ld1 {v15.4s, v16.4s}, [x0]

    fadd v17.4s, v15.4s, v16.4s
    fadd v17.2s, v15.2s, v16.2s

    ldr x0, =num13
    ld1 {v18.2d, v19.2d}, [x0]

    fadd v20.2d, v19.2d, v18.2d

    // single element moves - uses ins

    mov v14.h[1], v16.h[6]
    mov v17.s[1], v16.s[2]
    mov v20.d[1], v19.d[1]

end:
    mov     x0, #0      /* status */
    mov     x8, #93     /* exit is syscall 93 */
    svc     #0          


.data
    .balign 32

num1:
    .byte 1
    .byte 2
    .byte 3
    .byte 4
    .byte 5
    .byte 6
    .byte 7
    .byte 8
    .byte 9
    .byte 10
    .byte 11
    .byte 12
    .byte 13
    .byte 14
    .byte 15
    .byte 16
num2:
    .byte 120
    .byte 121
    .byte 122
    .byte 123
    .byte 124
    .byte 125
    .byte 126
    .byte 127
    .byte 128
    .byte 129
    .byte 130
    .byte 131
    .byte 132
    .byte 133
    .byte 134
    .byte 135
num3:
    .hword 22000
    .hword 33000
    .hword 44000
    .hword 55000
    .hword 11000
    .hword 2200
    .hword 1100
    .hword 3300
num4:
    .hword 10000
    .hword 20000
    .hword 30000
    .hword 40000
    .hword 50000
    .hword 10000
    .hword 5000
    .hword 5000
num5:
    .word 100001
    .word 200002
    .word 300003
    .word 400004
num6:
    .word 900090
    .word 800080
    .word 700070
    .word 600060
num7:
    .quad 1000100
    .quad 2000200
num8:
    .quad 3001000
    .quad 4004000
num9:
    .float16 23.45
    .float16 67.89
    .float16 23.45
    .float16 67.89
    .float16 23.45
    .float16 67.89
    .float16 23.45
    .float16 67.89
num10:
    .float16 100.1
    .float16 200.2
    .float16 100.3
    .float16 200.4
    .float16 100.5
    .float16 200.6
    .float16 100.7
    .float16 200.8
num11:
    .single 1000.1
    .single 2000.1
    .single 3000.1
    .single 4000.1
num12:
    .single 5000.1
    .single 6000.1
    .single 7000.1
    .single 8000.1
num13:
    .double 1e100
    .double 2e100
num14:
    .double 3e100
    .double 4e100
