#!/usr/bin/env python2
#
# IT65, the generic 6502 .it driver
# by Ben "GreaseMonkey" Russell, 2011. Public domain.
# .it applier thing

import struct, sys, time

dmp_author = "<?>"
t = time.gmtime()
dmp_date = "%04i/%02i/%02i" % (t.tm_year,t.tm_mon,t.tm_mday)

drvtype = None
stereo = False

args = sys.argv[1:]
while len(args) > 0 and args[0].startswith("-"):
	a = args.pop(0).lower()
	
	if a in ["-sap", "-xex"]:
		if drvtype != None:
			raise Exception("cannot have more than one driver specified")
		
		drvtype = a
	elif a == "-stereo":
		stereo = True
	elif a == "-a":
		dmp_author = args.pop(0)
	else:
		raise Exception("invalid argument: %s" % repr(drvtype))

if len(args) < 2:
	print """usage:
	./it65.py [options] -type [options] infile.it outfile.xxx

where -type is one of the following:
	-sap - output as an Atari 800 .sap file
	-xex - output as an Atari 800 .xex file

planned -type things:
	-nsf - output as a Nintendo Entertainment System .nsf file
	-hes - output as a Turbografx-16/PC-Engine .hes file
	-sid - output as a Commodore 64 .sid file
	-vic - output as a VIC-20 .prg file

options:
	-a author - give author name
	
sap options:
	-stereo - produce a stereo .sap

planned options:
	nsf options:
		-fds - add Famicom Disk System audio
		-n163 - add Namco 163 audio
		-mmc5 - add Nintendo MMC5 audio
		-vrc6 - add Konami VRC6 audio (VRC7 not planned)
		-fme07 - add Sunsoft FME-07 audio
"""
	exit(99)

if drvtype == None:
	raise Exception("no driver given")

# load .it file
fp = open(args[0],"rb")

if fp.read(4) != "IMPM":
	if fp.read(4) == "ONia": # did they decide to MMCMP-compress it?
		raise Exception("don't be a dick")
	else:
		raise Exception("not a valid IMPM module")

dmp_name = fp.read(26)
while dmp_name.endswith("\x00") or dmp_name.endswith(" "):
	dmp_name = dmp_name[:-1]

fp.read(2) # skip pathighlight
ordnum, insnum, smpnum, patnum, cwt, cmwt, flags, special = struct.unpack("<HHHHHHHH",fp.read(16))
gvol, mvol, tpr, bpm, sep, pwd = struct.unpack("<BBBBBB",fp.read(6))
fp.read(10) # skip other crap
fp.read(64) # skip channel pans
fp.read(64) # skip channel volumes <-- TODO? actually load these into the driver ?

ordlist = [ord(fp.read(1)) for i in xrange(ordnum)]
insplist = [struct.unpack("<I",fp.read(4))[0] for i in xrange(insnum)]
smpplist = [struct.unpack("<I",fp.read(4))[0] for i in xrange(smpnum)]
patplist = [struct.unpack("<I",fp.read(4))[0] for i in xrange(patnum)]

inslist = [] # right now i don't care
smplist = [] # TODO: load samples for formats that actually need them
patlist = []

# load patterns
for ptr in patplist:
	fp.seek(ptr)
	pl, rows, _ = struct.unpack("<HHI", fp.read(8))
	patlist.append((rows,fp.read(pl)))

# loaded!
fp.close()

print "Name: %s" % repr(dmp_name)
print "Author: %s" % repr(dmp_author)
print "Date: %s" % repr(dmp_date)

if drvtype in ["-sap", "-xex"]:
	driver = "drv_sapx2.xex" if stereo else "drv_sap.xex"
	sap = (drvtype == "-sap")
	
	# open target .sap
	fp = open(args[1],"wb")
	
	# write header
	if sap:
		fp.write("SAP\r\n")
		fp.write("AUTHOR \"%s\"\r\n" % dmp_author.replace('"',"'"))
		fp.write("NAME \"%s\"\r\n" % dmp_name.replace('"',"'"))
		fp.write("DATE \"%s\"\r\n" % dmp_date)
		fp.write("TYPE B\r\n")
		if stereo:
			fp.write("STEREO\r\n")
		else:
			print "You might be missing some of the benefits that stereo can provide."
		fp.write("INIT 2003\r\n")
		fp.write("PLAYER 2006\r\n")
	
	# write driver in
	rdfp = open(driver, "rb")
	fp.write(rdfp.read())
	rdfp.close()
	
	# start writing data.
	fp.write("\xFF\xFF\x00\x40\xFF\xFF")
	dataptr = fp.tell()
	
	# pad orderlist
	while len(ordlist) < 128:
		ordlist.append(255)
	assert len(ordlist) == 128
	
	# write space for orderlist
	fp.write("\x00"*256)
	
	# write TPR/BPM
	fp.write(struct.pack("<BB",tpr,bpm))
	
	# write patterns
	pptrs = []
	for rows,data in patlist:
		pptrs.append(fp.tell())
		fp.write(chr(rows&255))
		fp.write(data)
	
	dataend = fp.tell()
	
	# fix up orderlist
	fp.seek(dataptr)
	for v in ordlist:
		if v == 255:
			fp.write("\x01\x01")
		elif v == 254:
			fp.write("\x01\x00")
		else:
			fp.write(struct.pack("<H", pptrs[v]-dataptr+0x4000))
	
	# fix up data chunk
	fp.seek(dataptr-2)
	fp.write(struct.pack("<H",dataend+(0x4000-dataptr)-1))
	
	# that's all folks
	fp.close()
	
else:
	raise Exception("EDOOFUS this should never happen")
