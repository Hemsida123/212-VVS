import re,json,hashlib,base64,subprocess,tempfile,zipfile,runpy,posixpath,sys
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
def check():
 build=runpy.run_path(str(R/'qa/build.py'));html=(Path(sys.argv[1]) if len(sys.argv)>1 else R/'index.html').read_text();s=BeautifulSoup(html,'html.parser')
 assert s.html['lang']=='sv' and s.select_one('meta[name=viewport]') and s.select_one('main#main')
 assert len(s.select('main h1'))==1
 assert not s.select('script[src],link[rel=stylesheet],iframe')
 assert not build['REF'].search(html)
 assert all(i['src'].startswith('data:') for i in s.select('img[src]'))
 assert s.select_one('a[href="https://ekom.se"]').get_text(strip=True)=='Designed by Ekom'
 assert not re.search(r'localStorage|sessionStorage|XMLHttpRequest|sendBeacon|\bfetch\s*\(',html)
 assert not re.search(r'url\(\s*[\'"]?https?://',html)
 js='\n'.join(x.string or '' for x in s.select('script'))
 with tempfile.NamedTemporaryFile('w',suffix='.js') as f:
  f.write(js);f.flush();p=subprocess.run(['node','--check',f.name],capture_output=True,text=True);assert p.returncode==0,p.stderr
 inv=build['inventory']();routes={p['route'] for p in inv['pages']};assert len(routes)==23 and len(routes)==len(inv['pages']);valid=routes|set(inv['aliases']);alltext=[]
 for p in inv['pages']:
  q=BeautifulSoup(p['html'],'html.parser');assert len(q.select('h1'))==1,p['route'];ids=[e['id'] for e in q.select('[id]')];assert len(ids)==len(set(ids)),p['route']
  for a in q.select('a[href]'):
   if a['href'].startswith('#/'):assert a['href'][1:].split('?')[0] in valid,(p['route'],a['href'])
  for i in q.select('img[src]'):assert (R/i['src']).is_file(),i['src']
  alltext.append(q.get_text(' ',strip=True))
 c=json.loads((R/'qa/content.json').read_text())['company'];text=' '.join(alltext)
 for value in [c['name'],c['email'],c['street'],c['phone']]:assert value in text,value
 assert len(json.loads((R/'qa/media.json').read_text()))==6
 assert all('/galleri/'+x['id'] in routes for x in json.loads((R/'qa/media.json').read_text()))
 assert all('/omraden/'+x in routes for x in ['emmaboda','nybro','lessebo'])
 assert all('/'+x.stem in inv['aliases'] for x in (R/'research').glob('*.html') if x.stem not in ['home','integritetspolicy'])
 assert all('/tjanster/'+x['id'] in routes for x in json.loads((R/'qa/content.json').read_text())['services'])
 for e in json.loads((R/'qa/assets.json').read_text())+json.loads((R/'qa/fonts.json').read_text()):assert hashlib.sha256((R/e['file']).read_bytes()).hexdigest()==e['sha256'],e['file']
 hashes={hashlib.sha256(base64.b64decode(v,validate=True)).hexdigest() for v in set(re.findall(r'data:[^\s"\'<>;,]+(?:;[^\s"\'<>;,]+)*;base64,([A-Za-z0-9+/=]+)',html))}
 for e in json.loads((R/'qa/assets.json').read_text())+json.loads((R/'qa/fonts.json').read_text()):assert e['sha256'] in hashes,e['file']
 package=json.loads((R/'qa/package.json').read_text());a=Path(package['archive']);assert hashlib.sha256(a.read_bytes()).hexdigest()==package['sha256']
 with zipfile.ZipFile(a) as z:
  assert z.testzip() is None
  assert z.read('index.html')==(R/'index.html').read_bytes();assert z.read('redigerbar.html')==(R/'redigerbar.html').read_bytes()
  for n in z.namelist():
   if (R/n).is_file():assert z.read(n)==(R/n).read_bytes(),n
   if n.endswith('/index.html'):
    href=BeautifulSoup(z.read(n),'html.parser').select_one('a')['href'];target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('#')[0]));assert target in z.namelist(),n
 assert (R/'LAS-MIG.md').is_file();print('SITE_VERIFIED')
if __name__=='__main__':check()
