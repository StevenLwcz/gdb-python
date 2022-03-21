set style enabled off
b _start
r
so ../vector.py
tui new-layout debug1 vector 1 src 1 status 0 cmd 1
layout debug1

vector v0.b.u v1.b.u v2.b.u
vector v3.h.u v4.h.u v5.h.u
vector v6.s.u v7.s.u v8.s.u
vector v9.d.u v10.d.u v11.d.u
vector b2.u h5.u s8.u d11.u
vector v12.h.f v13.h.f v14.h.f
vector v15.s.f v16.s.f v17.s.f
vector v18.d.f v19.d.f v20.d.f
vector h14.f s17.f d20.f

focus vector
