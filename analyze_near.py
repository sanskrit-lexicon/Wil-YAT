"""analyze_near.py Feb 25, 2015
  hwcmp_near.txt is created by

  Read hwcmp.txt and analyze the ~= cases, write out all the records,
  with some new reasons
  Usage: python analyze_near.py hwcmp_near.txt hwcmp_near_analyze.txt
  Mar 7, 2015:  Merged some reason codes

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
  m = re.search(r'^(.*?):',self.data1)
  self.key1=m.group(1)
  m = re.search(r'^(.*?):',self.data2)
  self.key2=m.group(1)

 def __repr__(self):
  out = "%s %s %s" %(self.data1,self.reason,self.data2)
  return out

def notes():
 """
 """
def analysis1(rec):
 """
 """
 verb_equal_key1 = [
  'akza:491,495',
  'aca:2072,2076',
  'aja:2188,2193',  
  'awa:2593,2596',
  'aWa:2677,2679',
  'aqa:2680,2682',
  'aRa:2689,2691',

  'ata:2787,2789',
  'ada:3636,3641',
  'ana:4746,4748',
  'aSa:17427,17431',
  'iKa:25871,25872',
  'ila:26616,26621',
  'iza:26681,26686',
  'Iza:27087,27092',
  'ucCa:27552,27560',
  'fja:33808,33816',
  'eja:34721,34723',
  'kaka:35715,35719',
  'kawa:36244,36252',
  'kaWa:36585,36589',
  'kaqa:36680,36687',
  'kaRa:36728,36733',
  'kada:37261,37267',
  'kala:40016,40025',
  'kasa:41073,41080',
  'Rada:71252,71255'
 ]
 if rec.data1 in verb_equal_key1:
  rec.reason = '=V'
  return True
 return False

def analysis2(rec):
 if rec.key1 == re.sub(r'r(.)\1',r'r\1',rec.key2):
  rec.reason = '=rxx' #'=rxx2'
  return True
 if re.sub(r'r(.)\1',r'r\1',rec.key1) == rec.key2:
  rec.reason = '=rxx' #'=rxx1'
  return True
 return False

def analysis3(rec,wilsonrootP):
 if ';' in rec.data2:
  return False
 if rec.key1 == ("%s%s" % (rec.key2,'a')):
  if rec.key1 in wilsonrootP:
   rec.reason = '=V' # "=a1V"
  else:
   rec.reason = '=a' #'=a1'
  return True
 if rec.key2 == ("%s%s" % (rec.key1,'a')):
  rec.reason = '=a' #'=a2'
  return True 
 return False

def analysis4(rec):
 if rec.key1 == re.sub(r'b','v',rec.key2):
  rec.reason = '=vb' #'=vb2'
  return True
 if re.sub(r'b','v',rec.key1) == rec.key2:
  rec.reason = '=vb' #'=vb1'
  return True
 return False

def analysis5(rec):
 if rec.key1 == re.sub(r'a$','A',rec.key2):
  rec.reason = '=aA' #'=aA2'
  return True
 if re.sub(r'a$','A',rec.key1) == rec.key2:
  rec.reason = '=aA' #'=aA1'
  return True
 return False

def analysis6(rec):
 if rec.key1 == re.sub(r'cC','C',rec.key2):
  rec.reason = '=cC' #'=cC2'
  return True
 if re.sub(r'cC','C',rec.key1) == rec.key2:
  rec.reason = '=cC' #'=cC1'
  return True
 if rec.key1 == re.sub(r'tt','t',rec.key2):
  rec.reason = '=tt' #'=tt2'
  return True
 if re.sub(r'tt','t',rec.key1) == rec.key2:
  rec.reason = '=tt' #''=tt1'
  return True
 return False

slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}
def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)

def analysis7(rec):
 key1 = re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,rec.key1)
 key2 = re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,rec.key2)
 if key1 == key2:
  rec.reason = '=nasal'
  return True
 return False

def analysis8(rec):
 m1 = re.search(r'^(.*?)([mM])$',rec.key1)
 m2 = re.search(r'^(.*?)([mM])$',rec.key2)
 if m1 and m2 and (m1.group(1) == m2.group(1)):
  rec.reason = '=mM$'
  return True
 m1 = re.search(r'^(.*?)([sH])$',rec.key1)
 m2 = re.search(r'^(.*?)([sH])$',rec.key2)
 if m1 and m2 and (m1.group(1) == m2.group(1)):
  rec.reason = '=sH$'
  return True
 return False

def analyze(rec,wilsonrootP):
 # The order of application is probably significant
 if analysis1(rec):
  return
 if analysis2(rec):
  return
 if analysis3(rec,wilsonrootP):
  return
 if analysis4(rec):
  return
 if analysis5(rec):
  return
 if analysis6(rec):
  return
 if analysis7(rec):
  return
 if analysis8(rec):
  return

def wil_mw_roots_init(filein):
 d={}
 f = codecs.open(filein,"r","utf-8")
 n = 0
 for line in f:
  n = n + 1
  m = re.search(r'<wil>(.*?)</wil>',line)
  d[m.group(1)] = True
 print n,"roots read from",filein
 return d 
 
def main(filein,fileout,filein1):
 wilsonrootP = wil_mw_roots_init(filein1)

 f = codecs.open(filein,"r","utf-8")
 fout = codecs.open(fileout,"w","utf-8")
 n = 0
 nout = 0
 reason_counter=Counter()
 for line in f:
  n = n + 1
  rec = Hwcmp(line)
  analyze(rec,wilsonrootP) # modifies 'reason'
  out = "%s\n" % rec
  fout.write(out)
  reason_counter.update([rec.reason])
 f.close()
 fout.close()
 print n,"lines read from",filein
 
 for reason in reason_counter.d.keys():
  print reason,reason_counter.d[reason]

#-----------------------------------------------------
if __name__=="__main__":
 filein=sys.argv[1]  #hwcmp_near.txt
 fileout=sys.argv[2] #hwcmp_near_analyze.txt
 filein1 = sys.argv[3] # wil_mw.txt
 main(filein,fileout,filein1)
