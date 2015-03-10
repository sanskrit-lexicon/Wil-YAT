"""hwnear_adj.py Mar 7, 2015
  Adjust hwcmp based upon hwcmp_near_analyze
  
python hwcmp_adj.py hwcmp.txt hwcmp_near_analyze.txt hwcmp_adj.txt


"""


import re
import sys
import codecs

class Counter(dict):
 def __init__(self):
  self.d = {}
 def update(self,l):
  for x in l:
   if not (x in self.d):
    self.d[x]=0
   self.d[x] = self.d[x] + 1

class Hwcmp(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  (self.data1,self.reason,self.data2) = re.split(r' ',line)
  try:
   m = re.search(r'^(.*?):(.*?)$',self.data1)
   self.key1=m.group(1)
   self.pos1 =m.group(2)
  except:
   self.key1 = None
   self.key2 = None
  try:
   m = re.search(r'^(.*?):(.*?)$',self.data2)
   self.key2=m.group(1)
   self.pos2 =m.group(2)
  except:
   self.pos1 = None
   self.pos2 = None

 def __repr__(self):
  out = "%s %s %s" %(self.data1,self.reason,self.data2)
  return out

def verb_patch1(recs):
 """  Search for triplets of records
      MISSING NONE X:y1
      Xa:w1 == Xa:y2
      Xa:w2 NONE MISSING
and replace with
     MISSING NONE MISSING  (this record skipped on output)
     Xa:w1 =V* X:y1
     XA:w2 == Xa:y2
Example: BEFORE
MISSING NONE lAj:48823,48824
lAja:141031,141034 == lAja:48825,48827
lAja:141035,141038 NONE MISSING

AFTER
MISSING NONE MISSING
lAja:141031,141034 =V* lAj:48823,48824
lAja:141035,141038 == lAja:48825,48827

 """
 for i in xrange(0,len(recs)-2):
  r1 = recs[i]
  r2 = recs[i+1]
  r3 = recs[i+2]
  dbg = (i == 34683)
  dbg = False
  if dbg:
   print "DBG CHECK BEFORE"
   print recs[i]
   print recs[i+1]
   print recs[i+2]
   print
  if r1.data1 != 'MISSING':
   if dbg: print "Exit 1"
   continue
  if r2.reason != '==':
   if dbg: print "Exit 2"
   continue
  if r2.key1 != r2.key2:
   if dbg: print "Exit 3"
   continue
  if r2.key1 != ("%sa" % r1.key2):
   if dbg: print "Exit 4"
   continue
  if r3.reason != 'NONE':
   if dbg: print "Exit 5"
   continue
  if r3.key1 != r2.key1:
   if dbg: print "Exit 6"
   continue
  #  All the conditions are fulfilled. Reconstruct data1,data2 for
  # each record.  Note - This does not adjust key1,key2,pos1,pos2
  r3.data2 = r2.data2
  r3.reason = '=='
  r2.reason = '=V*'
  r2.data2 = r1.data2
  # Now r1 will be an 'empty' record.
  r1.data2 = 'MISSING'
  if dbg:
   print "CHECK patch:"
   print recs[i]
   print recs[i+1]
   print recs[i+2]
   print
 return

def combine(filein,filein1,fileout):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Hwcmp(line) for line in f if not line.startswith(';')]
 d = {}
 for rec in recs:
  d[rec.data1]=rec
 
 f = codecs.open(filein1,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 n = 0
 nout = 0
 for line in f:
  n = n + 1
  recadj = Hwcmp(line)
  try:
   rec = d[recadj.data1]
  except:
   print "Not found",line.encode('utf-8')
   continue
  rec.reason = recadj.reason
 f.close()
 # There are about 300 cases of verbs still not properly
 # matched.  Try to improve this situation
 # modify attributes of recs[i]
 verb_patch1(recs)
 c = Counter()
 for rec in recs:
  if (rec.data1 == 'MISSING') and (rec.data2 == 'MISSING'):
   continue
  fout.write("%s\n" % rec)
  c.update([rec.reason])
 fout.close()
 # print counter
 sorted_c_keys = sorted(c.d,key=c.d.get,reverse=True)
 for reason in sorted_c_keys:
  print reason,c.d[reason]

#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1]  #hwcmp.txt
 filein1 =sys.argv[2] # hwcmp_near_analyze.txt
 fileout = sys.argv[3] # hwcmp_adj.txt
 combine(filein,filein1,fileout)
