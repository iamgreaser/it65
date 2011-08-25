
all: drv_sap.xex sappack.it saptest.sap

sappack.it: sappackgen.py
	python2 sappackgen.py

drv_sap.xex: drv_sap.a65 useful_stuff.a65 tab_sap.a65 player_it.a65 inc_a800.a65
	64tass -b -D STEREO=0 -o drv_sap.xex drv_sap.a65

drv_sapx2.xex: drv_sap.a65 useful_stuff.a65 tab_sap.a65 player_it.a65 inc_a800.a65
	64tass -b -D STEREO=1 -o drv_sapx2.xex drv_sap.a65

saptest.sap: drv_sap.xex drv_sapx2.xex it65.py saptest.it
	python2 it65.py -sap -stereo -a "Ben Russell (GreaseMonkey)" saptest.it saptest.sap
