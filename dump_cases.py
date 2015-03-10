"""dump_cases.py Feb 25, 2015
  reads a file formatted like hwcmp_wil_yat.txt.
  For each case in this file,  extract the corresponding records from
   each dictionary and print

   Usage: python dump_cases.py input.txt output.txt firstdict.txt seconddict.txt

   E.g., python dump_cases.py input.txt output.txt wil.txt yat.txt

 python dump_cases.py near_semicolon.txt near_semicolon_dump.txt data/wil.txt data/yat.txt data/wilhw2.txt data/yathw2.txt

 

"""


import re
import sys
import codecs
import datetime

class Hwcmp(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  (self.data1,self.reason,self.data2) = re.split(r' ',line)
  m = re.search(r'^(.*?):',self.data1)
  self.key1=m.group(1)
  m = re.search(r'^(.*?):',self.data2)
  self.key2=m.group(1)

 def __repr__(self):
  out = "%s %s %s" %(self.data1,self.reason,self.data2)
  return out

def gather_lines(data,vrecs):
 """ data is one of data1 or data2 from Hwcmp record
 Assume it has format of one or more pieces separated by ';'
 Assume each piece has form hw:l1,l2
 """
 outarr = []
 parts = re.split(r';',data)
 for part in parts:
  (hw,l1,l2) = re.split(r'[:,]',part)
  i1 = int(l1) - 1
  i2 = int(l2) 
  for i in xrange(i1,i2):
   outarr.append((i+1,vrecs[i])) # a pair (i+1 is line #, starting at 1)
 return outarr

def get_headwords(filein):
 d={}
 f = codecs.open(filein,"r","utf-8")
 for line in f:
  line=line.rstrip('\r\n')
  (page,key,line12) = re.split(r':',line)
  dkey = "%s:%s" %(key,line12)
  d[dkey] = (page,key,line12)
 f.close()
 return d 
 # d is a dict on key1,line12
def main(filein,fileout,file1,file2,file3,file4):
 # slurp first dictionary into array of lines
 with codecs.open(file1,'r','utf-8') as f:
  vrecs1=[line.rstrip('\r\n') for line in f]
 # slurp second dictionary into array of lines
 with codecs.open(file2,'r','utf-8') as f:
  vrecs2=[line.rstrip('\r\n') for line in f]
 # get dictionaries for the headword files
 hwdict1 = get_headwords(file3)
 hwdict2 = get_headwords(file4)
 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 n = 0
 nout = 0
 curdate = datetime.date.today().strftime("%m/%d/%Y")
 for line in f:
  n = n + 1
  rec = Hwcmp(line)
  outar1 = gather_lines(rec.data1,vrecs1)
  outar2 = gather_lines(rec.data2,vrecs2)
  (page1,key1,line112) = hwdict1[rec.data1]
  (page2,key2,line212) = hwdict2[rec.data2]
  #print "dbg:",key1,key2
  out = "case %03d: %s\n" % (n,rec)
  fout.write(out)
  fout.write("%s (page %s)\n" %(file1,page1))
  fout.write('; %s %s -> %s ()\n' %(curdate,key1,key2))
  for i1,out in enumerate(outar1):
   outa='%06d old %s\n'%out
   fout.write(outa)
   if i1 == 0:
    outa='%06d new %s\n'%out
    outa = re.sub(key1,key2,outa)
    fout.write(outa)
  fout.write('\n')
  fout.write("%s (page %s)\n" %(file2,page2))
  fout.write('; %s %s -> %s (print error)\n' %(curdate,key2,key1))
  for i2,out in enumerate(outar2):
   outa='%06d old %s\n'%out
   fout.write(outa)
   if i2 == 0:
    outa='%06d new %s\n'%out
    outa = re.sub(key2,key1,outa)
    fout.write(outa)
  fout.write('\n')
  sep = '-'*72
  fout.write("%s\n\n" %sep)
 f.close()
 fout.close()
 print n,"lines read from",filein

#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1]  #
 fileout=sys.argv[2] #
 file1 = sys.argv[3]
 file2 = sys.argv[4]
 file1 = sys.argv[3]
 file2 = sys.argv[4]
 file3 = sys.argv[5]
 file4 = sys.argv[6]

 main(filein,fileout,file1,file2,file3,file4)
