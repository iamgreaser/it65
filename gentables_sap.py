def gentab(p,b,bn,m,ms,c,cn):
	print ".align $%04X" % (0x80*b/8)
	print "pertab_%s%i_%i" % (cn,b,p)
	xl = []
	for i in xrange(128):
		v = int(c/(440.0*(2.0**((i+3-48)/12.0)*p/2.0)))
		v = min(m+1,max(1,v))-1
		xl.append(v)
		if len(xl) == 16:
			s = "\t." + bn + " "
			s += ','.join(ms % x for x in xl)
			print s
			xl = []
	print

for p in [2,15,31]:
	for b,bn,m,ms in [(8,"byte",0xFF,"$%02X"),(16,"word",0xFFFF,"$%04X")]:
		for c,cn in [(64000,"s"),(1790000,"f")]:
			gentab(p,b,bn,m,ms,c,cn)
