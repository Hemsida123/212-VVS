import json,re,subprocess,base64,mimetypes,hashlib,zipfile,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REF=re.compile(r'(?<![A-Za-z0-9_./:\-])(?:assets|fonts)/[A-Za-z0-9_./\-]+\.(?:png|webp|jpg|jpeg|avif|woff2|ttf)(?![A-Za-z0-9_.\-])')
def read(p):return (ROOT/p).read_text()
def jsjson(v):return json.dumps(v,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def prefix():
 media=json.loads(read('qa/media.json'));assets=json.loads(read('qa/assets.json'));logo=next(x for x in assets if x['file']=='assets/logo.png');media.append(dict(id='logo',file=logo['file'],width=logo['width'],height=logo['height'],alt='212 VVS AB'))
 return 'const CONTENT='+jsjson(json.loads(read('qa/content.json')))+';\nconst MEDIA='+jsjson({m['id']:m for m in media})+';\n'
def pure():return read('qa/site.js').split('//__BROWSER__')[0]
def node(code):
 r=subprocess.run(['node'],input=code,capture_output=True,text=True);assert r.returncode==0,r.stderr;return r.stdout

def inventory():return json.loads(node(prefix()+pure()+"\nprocess.stdout.write(JSON.stringify({pages:pageEntries().map(p=>({route:p.route,title:p.title,html:p.render()})),aliases:ALIASES}));"))
def build():
 logo='<img src="assets/logo.png" alt="212 VVS AB" width="137" height="143">'
 seed=node(prefix()+pure()+'\nprocess.stdout.write(home());')
 text=read('qa/template.html').replace('/*__CSS__*/',read('qa/site.css')).replace('/*__DATA__*/',prefix()).replace('/*__JS__*/',read('qa/site.js')).replace('<!--__LOGO__-->',logo).replace('<!--__HOME__-->',seed)
 assert '/*__' not in text and '<!--__' not in text
 (ROOT/'redigerbar.html').write_text(text)
 used=sorted(set(REF.findall(text)));data={f:'data:'+(mimetypes.guess_type(f)[0] or 'application/octet-stream')+';base64,'+base64.b64encode((ROOT/f).read_bytes()).decode() for f in used}
 portable=REF.sub(lambda m:data[m[0]],text);assert not REF.search(portable);(ROOT/'index.html').write_text(portable)
 inv=inventory();(ROOT/'qa/routes.json').write_text(json.dumps([p['route'] for p in inv['pages']],indent=2));(ROOT/'qa/pages.json').write_text(json.dumps(inv,ensure_ascii=False))
 files=['index.html','redigerbar.html','LAS-MIG.md','qa/build.py','qa/check.py','qa/site.css','qa/site.js','qa/template.html','qa/content.json','qa/facts.json','qa/assets.json','qa/media.json','qa/fonts.json','qa/routes.json','qa/DESIGN.md','research/SOURCES.md']+used+[str(p.relative_to(ROOT)) for p in (ROOT/'fonts').glob('*LICENSE*')]
 redirects={p['route']:p['route'] for p in inv['pages'] if p['route']!='/'}|{k:v for k,v in inv['aliases'].items() if k!=v}
 archive=ROOT/'package.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for f in files:z.write(ROOT/f,f)
  for old,target in redirects.items():
   path=old.strip('/');url='../'*len(path.split('/'))+'redigerbar.html#'+target
   z.writestr(path+'/index.html',f'<!doctype html><html lang="sv"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={html.escape(url,quote=True)}"><title>212 VVS AB</title><a href="{html.escape(url,quote=True)}">Fortsätt till sidan</a></html>')
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for f in files:assert z.read(f)==(ROOT/f).read_bytes(),f
  count=len(z.namelist())
 result={'archive':str(archive),'archive_bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':count,'routes':len(inv['pages']),'redirects':len(redirects),'resources':len(used),'standalone_bytes':(ROOT/'index.html').stat().st_size,'editable_bytes':(ROOT/'redigerbar.html').stat().st_size,'crc':'pass','files_match':'pass'}
 (ROOT/'qa/package.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':build()
