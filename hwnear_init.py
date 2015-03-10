"""hwnear_init.py Feb 25, 2015
  Read hwcmp.txt and dump records whose 'relation' is ~=
  python hwnear_init.py hwcmp_wil_yat.txt hwcmp_near.txt

"""


import re
import sys
import codecs

def near(filein,fileout):
 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 n = 0
 nout = 0
 for line in f:
  n = n + 1
  if re.search(' ~= ',line):
   nout = nout + 1
   fout.write(line)
 f.close()
 fout.close()
 print n,"lines read from",filein
 print nout,"lines written to",fileout

#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1]  #hwcmp.txt
 fileout =sys.argv[2] #hwcmp_near.txt
 near(filein,fileout)
