all: infocpsr infofpcr  infofpsr2  infofpsr  testqv

%.o:%.s
	as -mcpu=cortex-a72 -g -o $@ $<

infocpsr: infocpsr.o
	ld -o $@ $<

infofpcr: infofpcr.o
	ld -o $@ $<

infofpsr: infofpsr.o
	ld -o $@ $<

infofpsr2: infofpsr2.o
	ld -o $@ $<

testqv: testqv.o
	ld -o $@ $<

clean:
	rm -f infocpsr infofpcr infofpsr2 infofpsr testqv
	rm -f infocpsr.o infofpcr.o infofpsr2.o infofpsr.o testqv.o
