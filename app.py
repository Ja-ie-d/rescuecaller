"""RescueCall AI: local, simulated 911 report triage demo. NOT for real dispatch."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from collections import Counter
import json, re, threading

ROOT = Path(__file__).parent
LOCK = threading.Lock()
BASE = datetime(2026, 10, 7, 18, 0)
SEED = [
 ('Car crash with injured passengers at 5th Avenue and 34th Street','Manhattan, 5th Ave & 34th St','crash',0),
 ('Two cars collided near 34th and Fifth, people hurt','Manhattan, 5th Ave & 34th St','crash',1),
 ('Serious vehicle accident at Fifth Avenue 34th, three injured','Manhattan, 5th Ave & 34th St','crash',2),
 ('Crash at 34th street and 5th avenue, ambulance needed','Manhattan, 5th Ave & 34th St','crash',3),
 ('Someone is unconscious after a car collision at 5th and 34th','Manhattan, 5th Ave & 34th St','crash',4),
 ('Traffic collision with injuries Fifth and 34th','Manhattan, 5th Ave & 34th St','crash',5),
 ('Vehicle crash at 5th Ave and 34th Street','Manhattan, 5th Ave & 34th St','crash',6),
 ('Smoke coming from apartment building, possible fire','Brooklyn, Atlantic Ave & 4th Ave','fire',2),
 ('Building on Atlantic and Fourth is on fire, smoke visible','Brooklyn, Atlantic Ave & 4th Ave','fire',3),
 ('Fire at Atlantic Avenue and 4th, residents evacuating','Brooklyn, Atlantic Ave & 4th Ave','fire',4),
 ('Loud music complaint from a nearby apartment','Queens, Jackson Ave & 21st St','noise',3),
 ('Noise from loud party at Jackson and 21st','Queens, Jackson Ave & 21st St','noise',4),
 ('Person collapsed and is not breathing at Union Square','Manhattan, Union Square','medical',5),
 ('Unresponsive person near Union Square subway entrance','Manhattan, Union Square','medical',6),
 ('Water leaking from broken hydrant','Bronx, Grand Concourse & 170th St','utility',7),
 ('Power lines down and sparking near intersection','Staten Island, Victory Blvd & Jewett Ave','hazard',8),
 ('Tree blocking the roadway, no injuries reported','Queens, Northern Blvd & 82nd St','obstruction',9),
 ('Suspicious unattended bag near bus stop','Brooklyn, Flatbush Ave & Church Ave','suspicious',10),
]
REPORTS=[]; REVIEWS={}
for i,(desc,loc,kind,minutes) in enumerate(SEED,1):
 REPORTS.append({'id':i,'description':desc,'location':loc,'kind':kind,'time':(BASE+timedelta(minutes=minutes)).isoformat(timespec='minutes')})
NEXT_ID=len(REPORTS)+1

CRITICAL = ('not breathing','unconscious','unresponsive','severe bleeding','cardiac arrest','trapped')
HIGH = ('injured','injuries','hurt','fire','smoke','sparking','power lines','ambulance','collision','crash','accident')
MEDIUM = ('suspicious','blocked','blocking','leak','hydrant')

def urgency(desc):
 d=desc.lower()
 if any(k in d for k in CRITICAL): return 'Critical'
 if any(k in d for k in HIGH): return 'High'
 if any(k in d for k in MEDIUM): return 'Medium'
 return 'Low'

def norm(s):
 s=s.lower().replace('fifth','5th').replace('fourth','4th').replace('avenue','ave').replace('street','st')
 return set(re.findall(r'[a-z0-9]+',s)) - {'at','the','a','an','and','near','from','on','with','is','of','to'}

def similar(a,b):
 # Candidate reports must share the same normalized location and incident category,
 # and arrive within 20 minutes. This avoids merging unrelated emergencies.
 if a['kind']!=b['kind'] or norm(a['location'])!=norm(b['location']): return False
 t1=datetime.fromisoformat(a['time']); t2=datetime.fromisoformat(b['time'])
 if abs((t1-t2).total_seconds())>1200: return False
 x,y=norm(a['description']),norm(b['description'])
 return len(x&y)/max(1,len(x|y))>=.08 or SequenceMatcher(None,a['description'].lower(),b['description'].lower()).ratio()>=.38

def incidents():
 groups=[]
 for report in REPORTS:
  matches=[g for g in groups if any(similar(report,member) for member in g)]
  if not matches: groups.append([report]); continue
  primary=matches[0]; primary.append(report)
  for other in matches[1:]:
   primary.extend(other); groups.remove(other)
 rank={'Critical':0,'High':1,'Medium':2,'Low':3}
 result=[]
 for group in groups:
  group.sort(key=lambda x:x['id']); level=min((urgency(r['description']) for r in group),key=lambda x:rank[x]); ident=group[0]['id']
  result.append({'id':ident,'location':group[0]['location'],'kind':group[0]['kind'].title(),'priority':level,'count':len(group),'duplicates':len(group)-1,'status':REVIEWS.get(ident,'Pending review'),'reports':group,'summary':group[0]['description']})
 result.sort(key=lambda x:(rank[x['priority']],-x['count'],x['id']))
 return result

class Handler(BaseHTTPRequestHandler):
 def send(self,data,status=200,content_type='application/json'):
  body=json.dumps(data).encode() if content_type=='application/json' else data
  self.send_response(status);self.send_header('Content-Type',content_type+'; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_GET(self):
  if self.path=='/': return self.send((ROOT/'index.html').read_bytes(),content_type='text/html')
  if self.path=='/api/incidents':
   with LOCK:
    items=incidents(); count=len(REPORTS)
   return self.send({'incidents':items,'reports':count,'unique':len(items),'duplicates':count-len(items),'disclaimer':'Simulation only. Human review required.'})
  self.send({'error':'Not found'},404)
 def do_POST(self):
  global NEXT_ID
  length=int(self.headers.get('Content-Length','0'))
  if length>10000:return self.send({'error':'Request too large'},413)
  try: data=json.loads(self.rfile.read(length) or b'{}')
  except ValueError:return self.send({'error':'Invalid JSON'},400)
  with LOCK:
   if self.path=='/api/reports':
    desc=str(data.get('description','')).strip()[:500]; loc=str(data.get('location','')).strip()[:150];kind=str(data.get('kind','')).lower()
    if not desc or not loc or kind not in ('crash','fire','noise','medical','utility','hazard','obstruction','suspicious'):
     return self.send({'error':'Provide description, location, and valid incident type'},400)
    report={'id':NEXT_ID,'description':desc,'location':loc,'kind':kind,'time':BASE.isoformat(timespec='minutes')};NEXT_ID+=1;REPORTS.append(report)
    return self.send({'report':report},201)
   if self.path=='/api/review':
    try: ident=int(data.get('id'))
    except (TypeError,ValueError):return self.send({'error':'Invalid ID'},400)
    status=data.get('status')
    if status not in ('Acknowledged','Dispatched (demo)','Needs verification','Pending review') or ident not in [g['id'] for g in incidents()]:return self.send({'error':'Invalid incident or status'},400)
    REVIEWS[ident]=status;return self.send({'ok':True})
   if self.path=='/api/reset':
    REPORTS[:]=[{'id':i,'description':d,'location':l,'kind':k,'time':(BASE+timedelta(minutes=m)).isoformat(timespec='minutes')} for i,(d,l,k,m) in enumerate(SEED,1)];NEXT_ID=len(REPORTS)+1;REVIEWS.clear();return self.send({'ok':True})
  return self.send({'error':'Not found'},404)

if __name__=='__main__':
 print('RescueCall AI demo: http://localhost:8000')
 ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
