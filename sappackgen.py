#!/usr/bin/env python2
#
# IT65, the generic 6502 .it driver
# by Ben "GreaseMonkey" Russell, 2011. Public domain.
# SAP pack generator

import struct

# generate samples
#
# from "Mapping The Atari":
#     7    6    5
#     0    0    0  five bit, then 17 bit, polys
#     0    0    1  five bit poly only
#     0    1    0  five bit, then four bit, polys
#     0    1    1  five bit poly only
#     1    0    0  l7 bit poly only
#     1    0    1  no poly counters (pure tone)
#     1    1    0  four bit poly only
#     1    1    1  no poly counters (pure tone)

sdata = []

def mixpoly(l1,l2):
	p1 = 0
	p2 = 0
	l = []
	while True:
		if l1[p1] > 0 and l2[p2] > 0:
			l.append(80)
		else:
			l.append(-80)
		p1 += 1
		p2 += 1
		p1 %= len(l1)
		p2 %= len(l2)
		if p1 == 0 and p2 == 0:
			break
	return l

def genpoly(taps):
	l = []
	
	v = taps
	
	# modplug is a piece of shit modplug is a piece of shit modplug is a piece of shit modplug is a piece of shit modplug is a piece of shit
	# hence we have to ensure every sample is at least 4 bytes
	# HENCE we need to spit each byte out twice
	while True:
		if v&1:
			l.append(80)
			l.append(80)
			v = (v>>1)^taps
		else:
			l.append(-80)
			l.append(-80)
			v >>= 1
		if v == taps:
			break
	
	return l

# TODO work this damn thing out
# FIXME: the really noisy one is complete bullshit; currently doing a 15-bit thing
# wf0
sdata.append(mixpoly(genpoly(0b11000),genpoly(0b110000000000000)))
# wf1
sdata.append(genpoly(0b11000))
# wf2
sdata.append(mixpoly(genpoly(0b11000),genpoly(0b1100)))
# wf3
sdata.append(genpoly(0b11000))
# wf4
sdata.append(genpoly(0b110000000000000))
# wf5
sdata.append(genpoly(0b10))
# wf6
sdata.append(genpoly(0b1100))
# wf7
sdata.append(genpoly(0b10))

sscaler = [31,31,31,31,31,2,15,2]

# write it up
fp = open("sappack.it","wb") # crapsack
fp.write("IMPM")
fp.write("it65 sap pack" + " "*(25-13) + "\x00\x04\x10")
fp.write(struct.pack("<HHHHHHHH"
	,1
	,0
	,8
	,0
	,0x0200
	,0x0216
	,0b00001001
	,0x0000
		))
fp.write(struct.pack("<BBBBBB"
	,128
	,48
	,6
	,125
	,64
	,0
		))
fp.write("it65, bro.")
fp.write("\x00"*4 + "\x40"*4 + "\x20"*56)
fp.write("\x40"*64)
fp.write("\xFF")
slptr = fp.tell()
splist = []
fp.write("\x00"*4*8)
fp.write("\x00"*6) # XXX: how many does this have to be? DOCUMENT YOUR STUFF BETTER, DAMMIT also only modplug chokes here AFAIK
for i in xrange(8):
	splist.append(fp.tell())
	fp.write("IMPS :D it65 :D \x00\x40\x11\x40")
	fp.write("wf%i" % i + " "*(25-3) + "\x00")
	fp.write("\x01\x20")
	fp.write(struct.pack("<IIIIIIIBBBB"
		,len(sdata[i])
		,0
		,len(sdata[i])
		,int(440.0*(2.0**(3.0/12.0))*2*sscaler[i])
		,0
		,0
		,fp.tell()+32
		,0,0,0,0
			))
	fp.write(''.join(chr(c&255) for c in sdata[i]))

fp.seek(slptr)
fp.write(struct.pack("<" + "I"*len(splist), *splist))

fp.close()