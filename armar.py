# Genera grabar.html: los guiones uno por uno, para leer mientras se graba, con el video de referencia al lado.
# Sale de guiones.js (la misma fuente que el tablero): el arranque que se muestra es el propuesto del guion.
# Uso: py armar.py   (escribe grabar.html al lado de este archivo)
import html, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
e = lambda s: html.escape(str(s), quote=True)

src = open(os.path.join(AQUI, 'guiones.js'), encoding='utf-8').read()
D = json.loads(re.search(r'window\.GUIONES = (\{.*\});\s*$', src, re.S).group(1))

def fecha_orden(g):
    m = re.search(r'(\d\d)-(\d\d)', g['tipo'])
    return (int(m.group(2)), int(m.group(1))) if m else (99, 99)

G = []
for r in D['refs']:
    for g in r['guiones']:
        G.append((r, g))
G.sort(key=lambda x: fecha_orden(x[1]))

def campo(k, q, txt, sec, nota=''):
    h = (f'<div class="l"><p class="q">{e(q)}</p>'
         f'<p class="d" contenteditable="true" spellcheck="false" data-k="{e(k)}" data-o="{e(txt)}" data-sec="{e(sec)}" data-q="{e(q)}">{e(txt)}</p>'
         f'<p class="ed" data-for="{e(k)}" hidden>Editado · <button type="button" data-volver="{e(k)}">volver al original</button></p>')
    if nota: h += f'<p class="n">{e(nota)}</p>'
    return h + '</div>'

secs, grilla = [], []
for i, (r, g) in enumerate(G, 1):
    k = f"{r['n']}{g['v']}"
    fecha = g['tipo'].split(' · ')[0]
    sec = f"{fecha} · {g['titulo']}"
    cuerpo = campo(f'{k}|h', g['hook']['quien'].upper() + ' · ARRANQUE', g['hook']['dice'], sec, 'Los otros arranques para elegir están en el tablero.')
    for j, b in enumerate(g['beats']):
        quien = b[3].upper()
        nota = ('⚠️ ' + b[4]) if len(b) > 4 and b[4] else ''
        cuerpo += campo(f'{k}|{j}', quien, b[2], sec, nota)
    vid = r['id']
    secs.append(f'''<section class="g" id="g{k.lower()}">
  <div class="txt">
    <p class="meta"><span class="num">{i:02d}</span> {e(g['tipo'])} · {e(g['dur'])}</p>
    <h2>{e(g['titulo'])}</h2>
    <p class="n">{e(g.get('plano', ''))}</p>
    {cuerpo}
    <div class="extra"><p class="n"><b>La idea:</b> {e(g['angulo'])}</p><p class="n"><b>Ojo:</b> {e(g.get('ojo', ''))}</p></div>
  </div>
  <div class="vid"><p class="n">Video de referencia · {e(r['formato'])} · {e(r['cuenta'])} · <a href="https://www.instagram.com/reel/{vid}/" target="_blank" rel="noopener">abrir en Instagram</a></p>
    <iframe src="https://www.instagram.com/reel/{vid}/embed" loading="lazy" allowfullscreen scrolling="no" title="Video de referencia"></iframe></div>
</section>''')
    grilla.append(f'<li><a href="#g{k.lower()}"><b>{e(fecha)}</b> · {e(g["titulo"])}</a> <span class="n">· {e(g["dur"].split(" · ")[-1])}</span></li>')

pagina = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Para grabar · Sergio Rosa y Asociados</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap" rel="stylesheet">
<style>
/* Sistema de Seery Studio (el del portfolio): negro, hueso y un solo acento naranja. Campo claro para leer mientras se graba. */
:root{{color-scheme:light;--negro:#0E0E0E;--tinta:#141414;--naranja:#FF4D00;--gris:#5F5F5F;--linea:#D9D9D9;--hueso:#F5F4F2}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--tinta);font:19px/1.6 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:var(--tinta)}}
header{{background:var(--negro);color:#fff}}
header .in{{max-width:1100px;margin:0 auto;padding:36px 16px 30px}}
.marca{{font:600 12px/1.4 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--naranja);margin:0 0 10px}}
h1{{font-weight:900;font-size:40px;line-height:1.08;letter-spacing:-.03em;margin:0 0 10px}}
header p{{margin:4px 0;color:#CFCFCF;font-size:16px}} header a{{color:var(--naranja)}}
main{{max-width:1100px;margin:0 auto;padding:8px 16px 80px}}
h2{{font-weight:800;font-size:26px;line-height:1.25;letter-spacing:-.02em;margin:4px 0 8px}}
.parte{{font:600 13px/1.4 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;border-top:2px solid var(--negro);padding-top:12px;margin:48px 0 0}}
.grilla{{list-style:none;padding:0;margin:14px 0 0}} .grilla li{{margin:6px 0;font-size:17px}} .grilla a{{text-decoration:none}} .grilla a:hover b{{text-decoration:underline}}
.g{{display:grid;grid-template-columns:1fr 340px;gap:40px;padding:40px 0;border-bottom:1px solid var(--linea)}}
.meta,.q{{font:600 12px/1.4 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin:0;color:var(--gris)}}
.num{{display:inline-block;background:var(--negro);color:var(--naranja);padding:2px 7px;border-radius:3px;margin-right:6px;letter-spacing:.04em}}
.l{{margin:20px 0}} .d{{font-size:23px;line-height:1.5;margin:6px 0;font-weight:500;color:var(--negro)}}
.n{{font:14px/1.5 Inter,sans-serif;color:var(--gris);margin:4px 0}}
.extra{{margin-top:26px;padding:14px 16px;background:var(--hueso);border-left:3px solid var(--naranja)}}
.vid{{position:sticky;top:16px;align-self:start}}
.vid iframe{{display:block;width:100%;height:620px;border:1px solid var(--linea);margin-top:6px;background:var(--hueso);border-radius:6px}}
.d[contenteditable]{{border-radius:4px;padding:4px 8px;margin-left:-8px;outline:none;cursor:text}}
.d[contenteditable]:hover{{background:var(--hueso)}}
.d[contenteditable]:focus{{background:#fff;box-shadow:0 0 0 1.5px var(--negro)}}
.d.mod{{border-left:3px solid var(--naranja);border-radius:0 4px 4px 0}}
.ed{{font:13px Inter,sans-serif;color:var(--gris);margin:2px 0 0}}
.ed button{{font:inherit;color:var(--tinta);background:none;border:0;padding:0;text-decoration:underline;cursor:pointer}}
.aviso{{font:15px/1.5 Inter,sans-serif;border:1px solid var(--negro);padding:12px 14px;margin:24px 0 0}}
#toast{{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);font:14px Inter,sans-serif;background:var(--negro);color:#fff;padding:9px 14px;border-radius:6px;opacity:0;transition:opacity .2s;pointer-events:none}}
#toast.on{{opacity:1}}
@media (max-width:900px){{.g{{grid-template-columns:1fr 260px;gap:20px}} .vid iframe{{height:520px}} .d{{font-size:21px}}}}
@media (max-width:640px){{.g{{grid-template-columns:1fr}} .vid{{position:static;order:-1}} .vid iframe{{height:560px}} h1{{font-size:32px}}}}
@media print{{header{{background:none;color:#000}} .vid,.ed,.aviso{{display:none}} .g{{grid-template-columns:1fr;break-inside:avoid-page}}}}
</style></head><body>
<header><div class="in">
<p class="marca">Sergio Rosa y Asociados · guiones de octubre</p>
<h1>Para grabar</h1>
<p>{len(G)} reels de una sola jornada de grabación, en el orden en que se publican.</p>
<p><a href="./">Volver al tablero de guiones</a></p>
</div></header>
<main>
<p class="aviso">Podés agregar o borrar palabras: tocá cualquier texto y escribí. Se guarda solo y se ve igual desde cualquier aparato. Si te arrepentís, cada texto cambiado tiene «volver al original». Lo marcado ⚠️ es lo que Sergio tiene que confirmar antes de publicar.</p>
<p class="parte">El orden</p>
<ol class="grilla">{''.join(grilla)}</ol>
<p class="parte">Los guiones</p>
{''.join(secs)}
</main>
<div id="toast" role="status"></div>
<script>
/* Ediciones: en este navegador y en la planilla de Google (tablero propio). Gana lo más nuevo. */
const NUBE = 'https://script.google.com/macros/s/AKfycbxgjYt2q3iZXebWQTGmeCoIkdg6bAyGNUPSIwTy47F43D51ED09QDCZU1WNqTMlQp31qw/exec', TABLERO = 'sergio-grabar-2026-10';
const leer = (k, d) => {{ try {{ const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); }} catch {{ return d; }} }};
const anotar = (k, v) => {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch {{}} }};
let ed = leer('sr-gr-ed', {{}}), fecha = leer('sr-gr-fecha', 0), tSub, tToast;
/* lo que se cambió en el tablero (sergio-rosa-guiones) es la base: acá se edita encima */
let tab = leer('sr-ed', {{}});
const idTab = k => {{ const [g, x] = k.split('|'); return x === 'h' ? g + ':say' : g + ':b' + x; }};
const base = p => tab[idTab(p.dataset.k)] ?? p.dataset.o;
const campos = [...document.querySelectorAll('.d[data-k]')];
const hora = () => new Date().toTimeString().slice(0, 5);
function toast(t, ms = 1800){{ const el = document.getElementById('toast'); el.textContent = t; el.classList.add('on'); clearTimeout(tToast); tToast = setTimeout(() => el.classList.remove('on'), ms); }}
function marcar(p){{
  const mod = p.dataset.k in ed;
  p.classList.toggle('mod', mod);
  document.querySelector(`.ed[data-for="${{CSS.escape(p.dataset.k)}}"]`).hidden = !mod;
}}
function pintar(){{ campos.forEach(p => {{ if (document.activeElement !== p) p.textContent = ed[p.dataset.k] ?? base(p); marcar(p); }}); }}
function filas(){{ return campos.map(p => [p.dataset.sec, p.dataset.q, p.textContent.trim(), p.dataset.k in ed ? 'editado' : 'original']); }}
async function subir(){{
  try {{
    const o = await (await fetch(NUBE, {{method: 'POST', body: JSON.stringify({{t: TABLERO, fecha, estado: {{ed}}, filas: filas()}})}})).json();
    if (!o.ok) throw 0;
    toast('Guardado · ' + hora());
  }} catch {{ toast('Sin conexión: quedó guardado en este aparato', 3000); }}
}}
function cambio(){{
  fecha = Math.max(Date.now(), fecha + 1);
  anotar('sr-gr-ed', ed); anotar('sr-gr-fecha', fecha);
  clearTimeout(tSub); tSub = setTimeout(subir, 1200);
}}
document.addEventListener('input', ev => {{
  const p = ev.target.closest('.d[data-k]'); if (!p) return;
  const t = p.textContent.replace(/\\s+/g, ' ').trim();
  if (t === base(p).replace(/\\s+/g, ' ').trim()) delete ed[p.dataset.k]; else ed[p.dataset.k] = p.textContent;
  marcar(p); cambio();
}});
document.addEventListener('paste', ev => {{
  if (!ev.target.closest('.d[data-k]')) return;
  ev.preventDefault(); document.execCommand('insertText', false, (ev.clipboardData || window.clipboardData).getData('text/plain'));
}});
document.addEventListener('keydown', ev => {{ if (ev.key === 'Enter' && ev.target.closest('.d[data-k]')) {{ ev.preventDefault(); ev.target.blur(); }} }});
document.addEventListener('click', ev => {{
  const b = ev.target.closest('[data-volver]'); if (!b) return;
  const p = document.querySelector(`.d[data-k="${{CSS.escape(b.dataset.volver)}}"]`);
  delete ed[b.dataset.volver]; p.textContent = base(p); marcar(p); cambio();
}});
pintar();
(async () => {{
  try {{
    const t = await (await fetch(NUBE + '?t=sergio-rosa-guiones')).json();
    if (t.ok && t.estado && t.estado['sr-ed']) {{ tab = t.estado['sr-ed']; pintar(); }}
  }} catch {{}}
}})();
(async () => {{
  try {{
    const o = await (await fetch(NUBE + '?t=' + TABLERO)).json();
    if (o.ok && o.estado && o.fecha > fecha && !document.activeElement.matches('.d[data-k]')) {{
      ed = o.estado.ed || {{}}; fecha = o.fecha; anotar('sr-gr-ed', ed); anotar('sr-gr-fecha', fecha); pintar();
    }}
  }} catch {{}}
}})();
</script>
</body></html>
'''
open(os.path.join(AQUI, 'grabar.html'), 'w', encoding='utf-8').write(pagina)
print('ok', len(G), 'guiones')
