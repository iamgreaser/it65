
! WARNING ! THIS DRIVER DOESN'T ACTUALLY WORK YET !
! From what I gather, it plays through the patterns fine, but the notes themselves aren't playing properly.
! 

Notes:
- Sample mode, *LINEAR* slides (this isn't it2vgm!), No old-fart effects, No compat Gxx.
  - Yes, at least one of the two functions that calculate linear slides appears to actually work.
- No effects have been implemented yet.
- Voleffects should be on their way once those are sorted to some extent.
- It is likely that parameters will be handles S3M-style:
  - that is, only Gxx/Hxx/Oxx/(not sure what else)/derivatives will have their own special memory.

SAP:
- DO NOT GO PAST CHANNEL 16.
- S01 and S02 will eventually have meanings!
  - For 1,3,5,7: S01 = use slow clock, S02 = use fast clock.
  - For 2,4,6,8: S01 = use 8-bit oscillators, S02 = use combined 16-bit oscillator.
