"""hwcmp.py Feb 28, 2015
  In this version, the forcefile is empty, so the logic pertaining to
  it in hw_cmp7 function is not relevant.
  Feb 27, 2015.  Change hw_cmp7 so all the 'force' records are applied before
   anything else is done
"""


import re
import sys
import codecs
import string
from levenshtein import levenshtein1,levenshtein

class Hwrec(object):
 def __init__(self,line,n):
  line = line.rstrip()
  self.line = line
  (pagecol,hw,line12) = re.split(':',line)
  self.hw = hw
  (line1,line2) = re.split(r',',line12)
  lnum1=int(line1)
  lnum2=int(line2)
  self.ids = "%s:%s" %(hw,line12)
  self.used = False
  self.matchtype = None
  self.match = None

def extract2_recs(filein):
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs=[]
 n = 0
 ndup = 0
 recprev = None
 for line in f:
  rec = Hwrec(line,n)
  recs.append(rec)
  #print "extract2_recs",n,rec,line.rstrip('\r\n')
  n = n + 1
  #if n == 20:
  # print "extract2_recs dbg stop when n=",20
  # break
 f.close()
 print "%s consecutive duplicate headwords found in %s" % (ndup,filein)
 recmap = {}
 for rec in recs:
  if rec.ids in recmap:
   print "DUPLICATE rec.ids=",rec.ids
  recmap[rec.ids] = rec 
 return (recs,recmap)

def levenshtein1b(s1,s2,dmax):
 """ like levenshtein1, except return dmax if s1 and s2 have different
   first letters
 """
 #if (len(s1)>0) and (len(s2)>0) and (s1[0] != s2[0]):
 #return dmax
 if abs(len(set(s1)) - len(set(s2))) >= dmax: #additional optimization
  return dmax
 return levenshtein1(s1,s2,max)


def match_headwords(hw1,hw2,dmax,exact=False):
 if hw1 == hw2:
  return '=='
 if exact:
  return False
 d = levenshtein1b(hw1,hw2,dmax)
 if (d < dmax):
  return '~='
 return None

def apply_force(rec1map,rec2map,forcefile):
 f = codecs.open(fileforce,encoding='utf-8',mode='r')
 for line in f:
  line = line.rstrip()
  if line == '': # allow blank lines
   continue
  if line.startswith(';'): # allow comment starting with ';'
   continue
  (forceidstr1,forcetype,forceidstr2) = re.split(r' +',line)
  # Apply
  forceids1 = re.split(r';',forceidstr1)
  forceids2 = re.split(r';',forceidstr2)
  if (len(forceids1)>1) and (len(forceids2)>1):
   print "force problem dual duplicates",line
   continue
  if (len(forceids1) == 1) and (forceids1 != ['MISSING']):
   # modify rec1
   #print "force check:",line
   forceid1 = forceids1[0]
   if forceid1 in rec1map:
    rec1 = rec1map[forceid1]
    rec1.matchtype = forcetype
    rec1.match = forceidstr2
    rec1.ids2 = forceids2
    #rec1.used = True
   elif forceid1 == 'MISSING':
    pass
   else:
    print forceid1,"not in rec1map; forceline=",line
  elif (len(forceids2) == 1) and (forceids2 != ['MISSING']):
   # modify rec2
   forceid2 = forceids2[0]
   if forceid2 in rec2map:
    rec2 = rec2map[forceid2]
    rec2.matchtype = forcetype
    rec2.match = forceidstr1
    rec2.ids1 = forceids1
    #rec2.used = True
   elif forceid2 == 'MISSING':
    pass
   else:
    print forceid2,"not in rec2map; forceline=",line
  else:
   print "force problem:",line
 f.close()

def hw_cmp7(filein1,filein2,fileforce,fileout):
 wilFlag1 = (filein1 == 'wilhw2.txt') 
 wilFlag2 = (filein2 == 'wilhw2.txt') 
 (recs1,rec1map) = extract2_recs(filein1)
 (recs2,rec2map) = extract2_recs(filein2)
 apply_force(rec1map,rec2map,fileforce) 
 #apply_force(rec1map,rec2map,force1map,force2map)
 i1 = 0
 i2 = 0
 recs = [] # matches
 nrecs1 = len(recs1)
 nrecs2 = len(recs2)
 nprob = 0
 dmax = 2
 while (i1<nrecs1) and (i2<nrecs2):
  #if (i1>100):
  # print "DEBUG QUIT"
  # break
  rec1 = recs1[i1]
  rec2 = recs2[i2]
  #print "CHK:",i1,rec1.ids,rec1.used," ... ",i2,rec2.ids,rec2.used
  if rec1.used:
   i1 = i1 + 1
   continue
  if rec2.used:
   i2 = i2 + 1
   continue
  """
  if duplicate_headwords(rec2.hw,recs2[i2-1].hw,wilFlag2):
   (rec1ids,eqtype,rec2ids) = recs[-1]
   rec2ids = "%s;%s" % (rec2ids,rec2.ids)
   recs[-1] = (rec1ids,eqtype,rec2ids)
   i2 = i2 + 1
   continue
  if duplicate_headwords(rec1.hw,recs2[i1-1].hw,wilFlag1):
   (rec1ids,eqtype,rec2ids) = recs[-1]
   rec1ids = "%s;%s" % (rec1ids,rec1.ids)
   recs[-1] = (rec1ids,eqtype,rec2ids)
   i1 = i1 + 1
   continue
  """
  if rec1.matchtype:
   #print "Check a:",rec1.ids,rec1.matchtype,rec1.match
   recs.append((rec1.ids,rec1.matchtype,rec1.match))
   rec1.used=True
   for ids in rec1.ids2:
    if ids in rec2map:
     rec2map[ids].used=True
   continue
  if rec2.matchtype:
   recs.append((rec2.match,rec2.matchtype,rec2.ids))
   #print "Check b:",rec2.match,"(",rec2.ids1,")",rec2.matchtype,rec2.ids
   rec2.used=True
   for ids in rec2.ids1:
    if ids in rec1map:
     rec1map[ids].used=True
   continue
  # try exact match
  matchtype = match_headwords(rec1.hw,rec2.hw,dmax,exact=True)
  if matchtype:
   recs.append((rec1.ids,matchtype,rec2.ids))
   rec1.used=True
   rec2.used=True
   i1 = i1 + 1
   i2 = i2 + 1
   continue
  found = False
  mlook = 20  # a tunable parameter
  exact=True  # tunable
  for inc in xrange(1,mlook):
   if nrecs1<=i1+inc: 
    matchtype=False
   else:
    matchtype = match_headwords(recs1[i1+inc].hw,rec2.hw,dmax,exact=exact)
   if matchtype:
   #if rec2.hw == recs1[i1+inc].hw:
    recs.append((rec1.ids,'NONE','MISSING'))
    rec1.used=True
    i1 = i1 + 1
    found=True
    break # for loop
   if nrecs2<=i2+inc: 
    matchtype=False
   else:
    matchtype = match_headwords(rec1.hw,recs2[i2+inc].hw,dmax,exact=exact)
   if matchtype:
   #if rec1.hw == recs2[i2+inc].hw:
    recs.append(('MISSING','NONE',rec2.ids))
    rec2.used=True
    i2 = i2 + 1
    found=True
    break # for loop
  if found:
   continue
  # try approximate match
  matchtype = match_headwords(rec1.hw,rec2.hw,dmax,exact=False)
  if matchtype:
   recs.append((rec1.ids,matchtype,rec2.ids))
   rec1.used=True
   rec2.used=True
   i1 = i1 + 1
   i2 = i2 + 1
   continue
  if True:   # always do this.  
   #Assume neither rec1.hw is missing in recs2, and
   # that rec2.hw is missing in recs1
   recs.append((rec1.ids,'NONE','MISSING'))
   rec1.used=True
   i1 = i1 + 1
   recs.append(('MISSING','NONE',rec2.ids))
   rec2.used=True
   i2 = i2 + 1
   continue
  nprob = nprob + 1
  recs.append((rec1.ids,'??',rec2.ids))
  i1 = i1 + 1
  i2 = i2 + 1
  if nprob >= 1:  # examine EVERY problem
   print "Breaking after %s problems" % nprob
   break
 # some further adjustments
 fout = codecs.open(fileout,'w','utf-8')
 # write these 'near matches'
 dtypes = {}
 for (rec1ids,mtype,rec2ids) in recs:
  out = "%s %s %s" % (rec1ids,mtype,rec2ids)
  fout.write("%s\n" % out)
  if mtype in dtypes:
   dtypes[mtype] = dtypes[mtype] + 1
  else:
   dtypes[mtype] = 1
 # print summaries
 print "%s records read from file#1 = %s" %(len(recs1),filein1)
 print "%s records read from file#2 = %s" %(len(recs2),filein2)
 print "%s records written to %s" %(len(recs),fileout)
 for (mtype,ntype) in dtypes.iteritems():
  print "%5d matches of type %s" % (ntype,mtype)
 fout.close()
 if nprob>0:  # print last 15 records
  nrecs = len(recs)
  nrecs0 = max(nrecs-15,0)
  for i in xrange(nrecs0,nrecs):
   (rec1ids,mtype,rec2ids) = recs[i]
   out = "%s %s %s" % (rec1ids,mtype,rec2ids)
   print out
 else:
  print "NO OPEN PROBLEMS!"
 return

#-----------------------------------------------------
if __name__=="__main__":
 filein1=sys.argv[1]  #vcpte headwords+linenums
 filein2 =sys.argv[2]  # vcp headwords+linenums
 fileforce = sys.argv[3]  #forced correspondences
 fileout =sys.argv[4]
 hw_cmp7(filein1,filein2,fileforce,fileout)
