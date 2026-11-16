"""Arma guiones.js del tablero de Sergio Rosa (noviembre-diciembre 2026) con el molde de solmi-guiones.

    py armar-tablero.py

Fuente: vault-obsidian-git/clientes/sergio-rosa/REELS-2026-11.md. Trece temas, tres versiones cada uno (A/B/C),
cada versión con su reel de referencia. Los ya guionados (C-17, C-16, R-01) y los cuatro publicados salen de
guiones-octubre.js. Códigos de quién habla: V a cámara · E pregunta en off · P en pantalla · C chat ·
S «sin abogado» · K «con abogado». Nada de cifras ni artículos de ley; «A validar» = lo confirma Sergio.
"""
import json, subprocess

OCT = json.loads(subprocess.run(['node', '-e', '''
global.window={};require('./guiones-octubre.js');const D=window.GUIONES;const o={};
D.refs.forEach(r=>r.guiones.forEach(g=>{o[r.n+g.v]={titulo:g.titulo,dur:g.dur,hook:g.hook,hooks:g.hooks,beats:g.beats,id:r.id}}));
process.stdout.write(JSON.stringify(o))'''], capture_output=True, text=True, encoding='utf8').stdout)


def de_octubre(k):
    g = OCT[k]
    quien = lambda q: 'E' if 'off' in (q or '').lower() else 'V'
    hk = g['hook']
    lin = [['0:00', quien(hk.get('quien')), hk['dice'], 'Arranque']]
    lin += [[b[0], quien(b[3]), b[2], ('A validar · ' + b[4]) if len(b) > 4 and b[4] else ''] for b in g['beats']]
    hooks = [h[1] for h in (g.get('hooks') or []) if not str(h[2] if len(h) > 2 else '').startswith('✗')][:8]
    return lin, hooks


F = {  # formato: (mecánica, reel de referencia, de quién, cómo se graba)
 'pyr': ('pregunta y respuesta', 'Dd2bqaeRFmN', '«¿Esto se denuncia o no?» · @clemente.jimenez_', 'Sergio de frente en el escritorio; Emanuel pregunta desde atrás de la cámara. Respuestas cortas, se corta seco entre pregunta y respuesta.'),
 'jamas': ('jamás', 'DeHHucjoZG8', '«Jamás te vayas de una empresa sin reclamar esto» · @juanmalorente_laboralista', 'De pie al lado de la ventana, plano medio. Corte con zoom y placa en cada número.'),
 'sipodes': ('sí, podés', 'Dd1KV0LIqb4', '«Sí, podés irte con indemnización» · @juanmalorente_laboralista', 'De pie al lado de la ventana, plano medio. Corte con zoom y placa en cada número.'),
 'pov': ('POV', 'Dbo8iYZR1M7', 'POV: la consulta', 'Cámara a la altura de quien se sienta enfrente; Emanuel pregunta en off y el abogado contesta a cámara.'),
 'coment': ('contestando un comentario', 'DaTxtkvuAlz', 'Contestando un comentario · @nahuelaltieri', 'El comentario en pantalla al principio; el abogado lo lee y contesta de frente.'),
 'pizarron': ('pizarrón', 'DdSDh_hD9SU', 'El pizarrón · @laboralista.ok', 'Plano entero; escribe en el pizarrón mientras explica. Pizarrón limpio y fibrón que se lea.'),
 'placa': ('pregunta en placa', 'De7zcEUIAs5', '«¿Quién cobra la indemnización cuando fallece el trabajador?» · @derechosart (128 mil, 13 veces su normal)', 'La pregunta escrita grande desde el primer cuadro; el abogado contesta de frente, plano cerrado.'),
 '60s': ('60 segundos', 'DexDbW7JAl7', '«6 objections in 60 seconds» · @wolfofwallst', 'Escritorio con la notebook adelante y un reloj de 60 segundos corriendo que se ve todo el video. Se graba de corrido. La palabra clave de cada respuesta, grande en dorado.'),
 'solovs': ('solo vs con abogado', 'DfDWqalkdn_', '«Arreglar con el seguro: solo vs con abogado» · @dc.legalstudio', 'Dos personas del estudio de pie frente a la biblioteca, «SIN ABOGADO» y «CON ABOGADO» fijos arriba de cada una. Charlan entre ellas; al final una habla a cámara.'),
 'cadena': ('cadena de repreguntas', 'Dez56Kxx_Rf', '«¿Lo puedo sancionar?» · @ani.petratti.abogada', 'Sentado, plano medio. La primera pregunta en una caja arriba; las repreguntas en off, cortas. Respuestas de una o dos frases.'),
 'esverdad': ('¿es verdad?', 'DfDWRLStGwO', '«¿Ya no hay multas con la Ley Bases?» · @ani.petratti.abogada', 'Sentado a una mesa con el celular en la mano, como si leyera la pregunta. La pregunta en una caja en el primer cuadro; papeles de b-roll a la mitad.'),
 'animado': ('cuatro casos animado', 'DfM2TRWIZWI', '«¿Siempre es culpa del de atrás?» · @futuroseguro.ok', 'Todo en motion graphics (la receta del R-17, ónix y dorado): cada caso con su etiqueta y el veredicto abajo. Sergio recortado entra al costado al principio y al final; la voz se graba aparte.'),
 'papel': ('papel en la mesa', 'DeHp3Qyucg7', '«Esta cláusula» · @reyessulbaran.juridico', 'Cenital del escritorio: el papel sobre la mesa y la mano que marca cada parte. Voz del abogado. Ninguna cifra legible.'),
 'chat': ('chat en pantalla', 'DU5r_mnDkj5', 'Consultas por WhatsApp · @estudiojuridicoarancibia', 'El chat en pantalla, armado en edición con nombres inventados; el abogado lo lee y explica.'),
}
L = lambda t, q, x, n='': [t, q, x, n]
AV = 'A validar'


def ver(v, f, titulo, lineas, cierre, hooks, cierres, meta='Duración ≈35 s'):
    mec, ej, ejde, nota = F[f]
    return {'v': v, 'f': f, 'titulo': titulo, 'mecanica': mec, 'meta': meta, 'ej': ej, 'ejde': ejde, 'nota': nota,
            'lineas': lineas, 'cierre': cierre, 'hooks': hooks, 'cierres': cierres, 'hookIdx': 0}


def tema(r, tema_txt, persona, palabra, rec, porque, versiones, aviso=''):
    a, *otras = versiones
    it = {'r': r, 'tipo': F[a['f']][0].capitalize() + ' · ' + persona + ' · ' + palabra, 'titulo': tema_txt,
          'meta': a['meta'] + ' · ' + persona + ' · cierra en ' + palabra, 'ej': a['ej'], 'ejde': a['ejde'], 'nota': a['nota'],
          'lineas': a['lineas'], 'cierre': a['cierre'], 'hooks': a['hooks'], 'cierres': a['cierres'], 'hookIdx': 0,
          'recomendacion': 'grabar ' + rec + ' — ' + porque + (' ' + aviso if aviso else ''),
          'versiones': [{k: x[k] for k in x if k != 'f'} for x in otras]}
    return it


T = []

# 01 · aguinaldo en el despido de diciembre
T.append(tema('T01', 'Me echaron en diciembre: ¿y el aguinaldo?', 'Diego', 'DESPIDO', 'A',
  'despido es el tema que más rinde en la cuenta, y la pregunta y respuesta sacó el mejor reel (2.772 vistas).', [
  ver('A', 'pyr', 'Me echaron en diciembre: ¿y el aguinaldo?', [
    L('0:00', 'E', 'Me echaron en diciembre. ¿Me tienen que pagar el aguinaldo?', 'Arranque · En pantalla: DESPIDO EN DICIEMBRE'),
    L('0:03', 'V', 'Sí. Aunque te echen antes de cobrarlo, la parte que ya trabajaste te la tienen que pagar.', AV),
    L('0:09', 'E', '¿Y si renuncié yo?'),
    L('0:10', 'V', 'También. Renuncies o te echen, esa parte va en la liquidación final.', AV),
    L('0:15', 'E', '¿Y las vacaciones que no me tomé?'),
    L('0:17', 'V', 'También entran. Y los días que trabajaste del mes.', AV),
    L('0:21', 'E', '¿Y si me dicen que ya está todo pago?'),
    L('0:23', 'V', 'Pedí la liquidación por escrito y no firmes nada hasta que alguien la revise.')],
    'Si te echaron este mes, comentá DESPIDO o mandanos un mensaje y la revisamos con vos.',
    ['Me echaron en diciembre. ¿Me tienen que pagar el aguinaldo?', 'Si te echan en diciembre, esto te lo tienen que pagar igual.',
     '¿Te despidieron justo antes de fin de año? Escuchá esto antes de firmar.', 'El aguinaldo no se pierde porque te echen. Te explico.'],
    ['Si te echaron este mes, comentá DESPIDO o mandanos un mensaje y la revisamos con vos.',
     'Antes de firmar la liquidación, comentá DESPIDO o escribinos.', 'Mandáselo a alguien al que echaron este mes, y comentá DESPIDO si querés que la miremos.']),
  ver('B', 'jamas', 'Jamás firmes la liquidación de diciembre sin mirar esto', [
    L('0:00', 'V', 'Jamás firmes la liquidación de diciembre sin mirar esto.', 'Arranque · En pantalla: DICIEMBRE'),
    L('0:04', 'V', 'Renuncies o te echen, tu liquidación tiene que traer tres cosas.', AV),
    L('0:08', 'V', 'Uno: la parte del aguinaldo que ya trabajaste.', AV + ' · En pantalla: 1'),
    L('0:12', 'V', 'Dos: las vacaciones que no te tomaste.', AV + ' · En pantalla: 2'),
    L('0:16', 'V', 'Tres: los días que trabajaste del mes.', 'En pantalla: 3'),
    L('0:20', 'V', 'Si falta una, no firmes conforme.')],
    'Si te vas este mes, comentá DESPIDO o mandanos un mensaje y la miramos antes de que firmes.',
    ['Jamás firmes la liquidación de diciembre sin mirar esto.', 'Si te vas de un trabajo en diciembre, revisá estas tres cosas.',
     'Tres cosas que tiene que traer tu liquidación de fin de año.', 'Antes de firmar en diciembre, mirá esto.'],
    ['Si te vas este mes, comentá DESPIDO o mandanos un mensaje y la miramos antes de que firmes.',
     'Guardalo para cuando te toque, y comentá DESPIDO si querés que la revisemos.', '¿Te faltó alguna? Comentá DESPIDO o escribinos.']),
  ver('C', 'papel', 'Buscá esto en tu liquidación de diciembre', [
    L('0:00', 'V', 'Si te echan en diciembre, buscá esto en tu liquidación.', 'Arranque · la liquidación sobre la mesa, sin cifras legibles'),
    L('0:04', 'V', 'Acá: la parte del aguinaldo que ya trabajaste.', AV + ' · la mano marca la línea'),
    L('0:09', 'V', 'Acá: las vacaciones que no te tomaste.', AV),
    L('0:13', 'V', 'Y acá: los días que trabajaste del mes.'),
    L('0:17', 'V', 'Si alguno no está, no firmes conforme. Traela y la miramos.')],
    'Si tenés tu liquidación en la mano, comentá DESPIDO o mandanos un mensaje.',
    ['Si te echan en diciembre, buscá esto en tu liquidación.', 'Tu liquidación de fin de año tiene que tener estas tres líneas.',
     'Agarrá tu liquidación y fijate si dice esto.', 'Esto es lo primero que miramos cuando nos traen una liquidación.'],
    ['Si tenés tu liquidación en la mano, comentá DESPIDO o mandanos un mensaje.', 'Sacale una foto y escribinos: la miramos.',
     '¿No encontrás alguna? Comentá DESPIDO o escribinos.'])]))

# 02 · no me renuevan el contrato
T.append(tema('T02', 'No me renuevan el contrato para enero', 'Diego', 'DESPIDO', 'B',
  'el formato «¿es verdad?» todavía no se usó y la pregunta es la que se escucha en esta época.', [
  ver('A', 'pyr', 'No me renuevan el contrato para enero', [
    L('0:00', 'E', 'Me dijeron que no me renuevan el contrato para enero.', 'Arranque'),
    L('0:03', 'V', 'Primero fijate qué firmaste. Muchos contratos que dicen «a plazo» en realidad no lo son.', AV),
    L('0:09', 'E', '¿Y cómo me doy cuenta?'),
    L('0:10', 'V', 'Si hacés lo mismo que un empleado fijo y te renuevan una y otra vez, eso hay que mirarlo.', AV),
    L('0:16', 'E', '¿Y me corresponde algo?'),
    L('0:17', 'V', 'Como mínimo, la liquidación final. Y según el caso, puede haber más.', AV)],
    'Si te avisaron que no te renuevan, comentá DESPIDO o mandanos un mensaje y miramos tu contrato.',
    ['Me dijeron que no me renuevan el contrato para enero.', 'Si no te renuevan el contrato, escuchá esto antes de irte.',
     '«Se terminó el contrato» no siempre es tan simple.', '¿Te avisaron que en enero no seguís? Mirá esto.'],
    ['Si te avisaron que no te renuevan, comentá DESPIDO o mandanos un mensaje y miramos tu contrato.',
     'Traé el contrato y lo vemos: comentá DESPIDO o escribinos.', 'Mandáselo a alguien con contrato que vence en diciembre.']),
  ver('B', 'esverdad', '¿Es verdad que si tengo contrato a plazo no me pagan nada?', [
    L('0:00', 'E', 'Doctor, ¿es verdad que si tengo contrato a plazo no me tienen que pagar nada?', 'Arranque · la pregunta en una caja'),
    L('0:04', 'V', 'Te lo respondo porque me lo preguntan mucho en esta época. Sí y no.'),
    L('0:08', 'V', 'Que se termine el plazo no es lo mismo que te echen.', AV),
    L('0:12', 'V', 'Pero la liquidación final te la tienen que pagar igual.', AV),
    L('0:16', 'V', 'Y si te renovaron muchas veces haciendo lo mismo, puede que el contrato no sea a plazo.', AV),
    L('0:22', 'V', 'No alcanza con saber qué dice el contrato. Hay que saber cómo trabajaste.')],
    'Si te vence el contrato, comentá DESPIDO o mandanos un mensaje y lo vemos.',
    ['Doctor, ¿es verdad que si tengo contrato a plazo no me tienen que pagar nada?', '¿Es verdad que cuando se termina el contrato no te pagan nada?',
     'Te lo respondo porque me lo preguntan mucho en diciembre.', 'Sí y no. Te explico qué pasa cuando no te renuevan.'],
    ['Si te vence el contrato, comentá DESPIDO o mandanos un mensaje y lo vemos.', 'Comentá DESPIDO y te escribimos por privado.',
     '¿Te renovaron más de una vez? Contanos por mensaje.']),
  ver('C', 'chat', 'El mensaje de «para enero no te renovamos»', [
    L('0:00', 'C', 'Encargado: Hola, te aviso que para enero no te renovamos.', 'Arranque'),
    L('0:03', 'C', 'Vos: ¿Y qué me pagan?'),
    L('0:05', 'C', 'Encargado: Nada, se terminó el contrato.'),
    L('0:07', 'V', 'Esa última respuesta no es tan así.'),
    L('0:10', 'V', 'Aunque se termine el contrato, la liquidación final te la tienen que pagar.', AV),
    L('0:15', 'V', 'Y si te renovaron una y otra vez, hay que ver si de verdad era a plazo.', AV),
    L('0:20', 'V', 'Guardá ese chat.')],
    'Si te mandaron un mensaje así, comentá DESPIDO o mandanos una captura y lo vemos.',
    ['«Para enero no te renovamos.» ¿Te llegó este mensaje?', 'Si tu encargado te escribió esto, no le contestes todavía.',
     'Este chat se repite mucho en diciembre.', '«Nada, se terminó el contrato.» No es tan así.'],
    ['Si te mandaron un mensaje así, comentá DESPIDO o mandanos una captura y lo vemos.', 'Guardá el chat y escribinos.',
     'Comentá DESPIDO y te escribimos por privado.'])]))

# 03 · control médico
T.append(tema('T03', 'No fui al control médico de la empresa', 'Diego', 'DESPIDO', 'A',
  'es el formato de la referencia tal cual, del lado del trabajador.', [
  ver('A', 'cadena', '¿Me pueden echar por no ir al control médico?', [
    L('0:00', 'E', 'Doctor, no fui al control médico que me mandó la empresa. ¿Me pueden echar?', 'Arranque · la pregunta en una caja'),
    L('0:04', 'V', 'Cuidado. Primero fijate si te avisaron bien: cuándo, dónde y por qué medio.', AV),
    L('0:09', 'E', '¿Y si me avisaron bien y no fui?'),
    L('0:11', 'V', 'Justificá por qué no fuiste, por escrito, y pedí que te vuelvan a citar.', AV),
    L('0:16', 'E', '¿Y con una sola falta me pueden despedir?'),
    L('0:18', 'V', 'No debería ser automático.', AV),
    L('0:20', 'E', '¿Y si el médico de la empresa dice una cosa y el mío otra?'),
    L('0:23', 'V', 'Ahí no lo decide la empresa sola.', AV),
    L('0:26', 'V', 'No improvises: primero guardá todo por escrito, después decidís.')],
    'Si te pasó, comentá DESPIDO o mandanos un mensaje y lo vemos.',
    ['Doctor, no fui al control médico que me mandó la empresa. ¿Me pueden echar?', 'No fuiste al control médico. Cuidado con lo que hacés ahora.',
     '¿Te pueden despedir por faltar a un control médico?', 'Te mandaron un médico a tu casa y no estabas. ¿Y ahora?'],
    ['Si te pasó, comentá DESPIDO o mandanos un mensaje y lo vemos.', 'No improvises: comentá DESPIDO o escribinos.',
     'Mandáselo a alguien que está de licencia.'], 'Duración ≈32 s'),
  ver('B', 'placa', '¿Te pueden echar por no ir al control médico?', [
    L('0:00', 'P', '¿TE PUEDEN ECHAR POR NO IR AL CONTROL MÉDICO?', 'Arranque'),
    L('0:03', 'V', 'Depende. Y casi nunca es tan automático como te dicen.', AV),
    L('0:07', 'V', 'Si no te avisaron bien, no podés faltar a algo que no sabías.', AV),
    L('0:12', 'V', 'Si te avisaron y no fuiste, justificalo por escrito.', AV),
    L('0:16', 'V', 'Y si los médicos no coinciden, no lo decide la empresa sola.', AV)],
    'Si te pasó, comentá DESPIDO o mandanos un mensaje.',
    ['¿Te pueden echar por no ir al control médico?', 'Faltar al control médico no es lo mismo que faltar al trabajo.',
     'Lo que nadie te dice del control médico.', 'Si estás de licencia, esto te conviene saberlo.'],
    ['Si te pasó, comentá DESPIDO o mandanos un mensaje.', 'Guardalo por si te toca.', 'Comentá DESPIDO y te escribimos por privado.']),
  ver('C', 'animado', 'No fuiste al control médico: cuatro casos', [
    L('0:00', 'V', 'No fuiste al control médico. Mirá estos cuatro casos.', 'Arranque · Sergio entra al costado'),
    L('0:04', 'P', 'CASO 1 · Te avisaron mal → No te pueden sancionar por algo que no sabías.', AV),
    L('0:10', 'P', 'CASO 2 · Te avisaron bien y justificaste → Pedí otra fecha, por escrito.', AV),
    L('0:16', 'P', 'CASO 3 · Una sola falta sin justificar → No debería ser automático.', AV),
    L('0:22', 'P', 'CASO 4 · Faltás siempre → Ahí el riesgo es real.', AV)],
    '¿En cuál estás? Comentá DESPIDO o mandanos un mensaje.',
    ['No fuiste al control médico. Mirá estos cuatro casos.', 'Faltaste al control médico: en cuál de estos cuatro casos estás.',
     'Cuatro casos de control médico y qué pasa en cada uno.', '¿Te pueden echar por el control médico? Depende del caso.'],
    ['¿En cuál estás? Comentá DESPIDO o mandanos un mensaje.', 'Mandáselo a alguien que está de licencia.', 'Comentá DESPIDO y te escribimos.'])]))

# 04 · Ley Bases
T.append(tema('T04', 'Ley Bases y trabajo en negro', 'Diego', 'CONSULTA', 'A',
  'es el formato de la referencia tal cual.', [
  ver('A', 'esverdad', '¿Es verdad que con la Ley Bases ya no podés reclamar si trabajás en negro?', [
    L('0:00', 'E', 'Doctor, ¿es verdad que con la Ley Bases si trabajás en negro ya no podés reclamar nada?', 'Arranque · la pregunta en una caja'),
    L('0:05', 'V', 'Te lo respondo porque me lo preguntan mucho. Sí y no.'),
    L('0:08', 'V', 'Lo que cambió: (Sergio lo dice en una frase).', '🔒 Sergio explica la reforma'),
    L('0:14', 'V', 'Lo que sigue igual: (Sergio, en otra).', '🔒 Sergio explica la reforma'),
    L('0:20', 'V', 'Lo que se fue es la multa. El derecho a reclamar, no.', AV),
    L('0:25', 'V', 'No alcanza con saber que la ley cambió. Hay que saber en qué cambió y qué sigue igual.')],
    'Si trabajás o trabajaste en negro, comentá CONSULTA o mandanos un mensaje.',
    ['Doctor, ¿es verdad que con la Ley Bases si trabajás en negro ya no podés reclamar nada?', 'Te lo respondo porque me lo preguntan mucho: la Ley Bases y el trabajo en negro.',
     'Con la Ley Bases cambió algo. No lo que te dijeron.', 'Sí y no. Lo que cambió y lo que sigue igual.'],
    ['Si trabajás o trabajaste en negro, comentá CONSULTA o mandanos un mensaje.', 'Comentá CONSULTA y te escribimos por privado.',
     'Mandáselo a alguien que trabaja sin estar anotado.'], 'Duración ≈32 s'),
  ver('B', 'pizarron', 'Ley Bases: lo que cambió y lo que sigue igual', [
    L('0:00', 'V', 'Te dijeron que con la Ley Bases ya no podés reclamar si trabajabas en negro. Te muestro.', 'Arranque · pizarrón con dos columnas'),
    L('0:05', 'V', 'De este lado, lo que cambió.', '🔒 Sergio completa la columna'),
    L('0:12', 'V', 'De este, lo que sigue igual.', '🔒 Sergio completa la columna'),
    L('0:20', 'V', 'Lo que se fue es la multa. El derecho a reclamar, no.', AV)],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje.',
    ['Te dijeron que con la Ley Bases ya no podés reclamar. Te muestro.', 'Ley Bases: lo que cambió y lo que sigue igual, en un pizarrón.',
     'Dos columnas para entender la Ley Bases si trabajás en negro.', 'Esto es lo que cambió. Y esto, lo que no.'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje.', 'Guardalo y comentá CONSULTA si tenés dudas.', 'Comentá CONSULTA y te escribimos.']),
  ver('C', 'coment', '«Leí que con la Ley Bases ya no hay multas»', [
    L('0:00', 'P', 'Comentario: «Leí que con la Ley Bases ya no hay multas. ¿Entonces no puedo reclamar?»', 'Arranque'),
    L('0:04', 'V', 'Buena pregunta, porque es lo que más se escucha.'),
    L('0:07', 'V', 'Que no haya multa no quiere decir que no puedas reclamar.', '🔒 ' + AV),
    L('0:12', 'V', '(Sergio: qué se sigue pudiendo reclamar, en una frase.)', '🔒 Sergio explica la reforma'),
    L('0:18', 'V', 'Y si tenés otra pregunta, dejala abajo: la contestamos así.')],
    'Comentá CONSULTA o mandanos un mensaje con tu caso.',
    ['«Leí que con la Ley Bases ya no hay multas. ¿Entonces no puedo reclamar?»', 'Te contesto este comentario porque lo leo todos los días.',
     'Que no haya multa no quiere decir esto.', 'Respuesta a un comentario sobre la Ley Bases.'],
    ['Comentá CONSULTA o mandanos un mensaje con tu caso.', 'Dejá tu pregunta abajo y la contestamos así.', 'Comentá CONSULTA y te escribimos.'])],
  aviso='🔒 No se graba hasta que Sergio explique qué cambió con la reforma.'))

# 05 · volví de la ART
T.append(tema('T05', 'Volví de la ART y me quieren echar', 'Roberto', 'ART', 'A',
  'la pregunta y respuesta es el formato que mejor rindió; la referencia (#bajamedica de juanmalorente) sacó 369 mil.', [
  ver('A', 'pyr', 'Volví de la ART y me quieren echar', [
    L('0:00', 'E', 'Volví al trabajo después de la ART y me quieren echar.', 'Arranque'),
    L('0:03', 'V', 'Lo primero: que te hayan dado el alta no quiere decir que estés como antes.'),
    L('0:07', 'E', '¿Me pueden despedir?'),
    L('0:08', 'V', 'Pueden, pero no les sale gratis. Y si es por el accidente, eso se mira con lupa.', AV),
    L('0:14', 'E', '¿Y si me cambian de puesto?'),
    L('0:15', 'V', 'Si no podés hacer lo de antes, te tienen que dar tareas que puedas hacer.', AV),
    L('0:20', 'E', '¿Qué hago?'),
    L('0:21', 'V', 'No firmes nada y guardá todo: el alta, los estudios y los mensajes.')],
    'Si volviste de la ART y te pasa esto, comentá ART o mandanos un mensaje.',
    ['Volví al trabajo después de la ART y me quieren echar.', 'Te dieron el alta y te quieren despedir. Escuchá esto.',
     'Que te den el alta no quiere decir que estés como antes.', 'Volver de la ART y que te echen no es lo mismo que un despido cualquiera.'],
    ['Si volviste de la ART y te pasa esto, comentá ART o mandanos un mensaje.', 'Comentá ART y te escribimos por privado.',
     'Mandáselo a un compañero que volvió de la ART.']),
  ver('B', 'cadena', 'Volví de la ART y me cambiaron de puesto', [
    L('0:00', 'E', 'Doctor, volví de la ART y me cambiaron de puesto.', 'Arranque · la pregunta en una caja'),
    L('0:03', 'V', 'Cuidado. Si es porque no podés hacer lo de antes, puede corresponder.', AV),
    L('0:08', 'E', '¿Y si me pagan menos?'),
    L('0:09', 'V', 'Eso no. Que te muevan no es que te bajen el sueldo.', AV),
    L('0:13', 'E', '¿Y si me echan?'),
    L('0:14', 'V', 'Si es por el accidente, eso se mira con lupa.', AV),
    L('0:18', 'V', 'No improvises: guardá el alta y los mensajes, después decidís.')],
    'Si te pasó, comentá ART o mandanos un mensaje.',
    ['Doctor, volví de la ART y me cambiaron de puesto.', 'Te dieron el alta y te movieron de puesto. ¿Y el sueldo?',
     'Volviste de la ART. Tres preguntas que te vas a hacer.', 'Lo que te pueden cambiar y lo que no cuando volvés de la ART.'],
    ['Si te pasó, comentá ART o mandanos un mensaje.', 'No improvises: comentá ART o escribinos.', 'Mandáselo a un compañero que volvió de la ART.']),
  ver('C', 'coment', '«Me dieron el alta y a la semana me echaron»', [
    L('0:00', 'P', 'Comentario: «Me dieron el alta y a la semana me echaron. ¿Es legal?»', 'Arranque'),
    L('0:04', 'V', 'Te contesto porque esto pasa más de lo que creés.'),
    L('0:07', 'V', 'Que te den el alta no cierra lo que tenés que reclamarle a la ART.', AV),
    L('0:12', 'V', 'Y que te echen después no borra lo que te pasó trabajando.'),
    L('0:16', 'V', 'Son dos cosas distintas, y se pueden reclamar las dos.', AV)],
    'Si te pasó, comentá ART o mandanos un mensaje y lo vemos.',
    ['«Me dieron el alta y a la semana me echaron. ¿Es legal?»', 'Te contesto este comentario porque pasa más de lo que creés.',
     'El alta y el despido son dos cosas distintas.', 'Te echaron después de la ART. Esto no se borra.'],
    ['Si te pasó, comentá ART o mandanos un mensaje y lo vemos.', 'Dejá tu pregunta abajo y la contestamos así.', 'Comentá ART y te escribimos.'])],
  aviso='Antes de publicar: arreglar el ManyChat de ART (todavía manda la guía de in itinere).'))

# 06 · en negro y me lastimé (A = R-01 de octubre)
r01, r01h = de_octubre('5A')
T.append(tema('T06', 'Trabajo en negro y me lastimé', 'Roberto', 'CONSULTA', 'A',
  'ya está guionado (R-01 de octubre).', [
  ver('A', 'coment', '«Trabajo en negro y me lastimé laburando»', r01,
    'Si te pasó, comentá CONSULTA o mandanos un mensaje, y lo vemos.', r01h or ['Trabajo en negro y me lastimé laburando. ¿Puedo reclamar algo?'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje, y lo vemos.', 'Dejá tu pregunta abajo: la contestamos así.', 'Comentá CONSULTA y te escribimos por privado.']),
  ver('B', 'pov', 'Me caí en la obra y estoy en negro', [
    L('0:00', 'E', 'Trabajo en negro y me caí de una escalera en la obra.', 'Arranque'),
    L('0:03', 'V', '¿Te atendieron? ¿Tenés algo de la guardia?'),
    L('0:05', 'E', 'Sí, pero el patrón dice que no puedo reclamar porque no estoy anotado.'),
    L('0:09', 'V', 'Eso no es así. Que no te hayan registrado no juega a su favor.', AV),
    L('0:14', 'V', 'Juntá los mensajes, las fotos, los testigos y cómo te pagaban.', AV),
    L('0:19', 'V', 'Con eso se muestra que trabajabas ahí.')],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje.',
    ['Trabajo en negro y me caí de una escalera en la obra.', '«No podés reclamar porque no estás anotado.» No es así.',
     'Te lastimaste trabajando en negro. Lo primero que te preguntamos.', 'Vino a consultar porque el patrón le dijo que no podía reclamar.'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje.', 'Comentá CONSULTA y te escribimos por privado.', 'Mandáselo a alguien que trabaja en una obra.']),
  ver('C', 'sipodes', 'Sí: podés reclamar aunque trabajes en negro', [
    L('0:00', 'V', 'Sí: podés reclamar aunque trabajes en negro.', 'Arranque · En pantalla: AUNQUE ESTÉS EN NEGRO'),
    L('0:04', 'V', 'Lo que hay que mostrar es que trabajabas ahí. Tres formas.', AV),
    L('0:08', 'V', 'Uno: los mensajes con el patrón.', 'En pantalla: 1'),
    L('0:11', 'V', 'Dos: fotos y testigos.', 'En pantalla: 2'),
    L('0:14', 'V', 'Tres: cómo te pagaban.', 'En pantalla: 3')],
    'Si te lastimaste trabajando en negro, comentá CONSULTA o mandanos un mensaje.',
    ['Sí: podés reclamar aunque trabajes en negro.', 'Trabajar en negro no te deja sin derechos.',
     'Tres cosas que sirven para mostrar que trabajabas ahí.', 'Sí, podés. Aunque no estés anotado.'],
    ['Si te lastimaste trabajando en negro, comentá CONSULTA o mandanos un mensaje.', 'Guardalo y comentá CONSULTA si te pasó.',
     'Mandáselo a alguien que trabaja sin estar anotado.'])]))

# 07 · quién cobra si fallece
T.append(tema('T07', '¿Quién cobra si el trabajador fallece?', 'Mónica', 'CONSULTA', 'A',
  'es la mecánica del reel que más rindió en el rubro este mes (@derechosart, 128 mil, 13 veces su normal); el único para Mónica.', [
  ver('A', 'placa', 'Si un trabajador fallece, ¿quién cobra?', [
    L('0:00', 'P', 'SI UN TRABAJADOR FALLECE POR UN ACCIDENTE DE TRABAJO, ¿QUIÉN COBRA?', 'Arranque'),
    L('0:03', 'V', 'Es una pregunta que nadie se hace hasta que le toca.'),
    L('0:06', 'V', 'Su familia puede reclamar.', AV),
    L('0:09', 'V', '(Sergio: quiénes, en una frase.)', AV),
    L('0:14', 'V', 'Y no hace falta que haya sido en el lugar de trabajo: también cuenta el camino.', AV),
    L('0:19', 'V', 'Si te pasó con alguien de tu familia, no lo dejes pasar.')],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje. Te escribimos por privado.',
    ['Si un trabajador fallece por un accidente de trabajo, ¿quién cobra?', 'Es una pregunta que nadie se hace hasta que le toca.',
     'Si pasa lo peor, la familia también puede reclamar.', '¿Quién cobra cuando el trabajador ya no está?'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje. Te escribimos por privado.', 'Mandáselo a alguien que lo necesite.',
     'Escribinos por privado y lo vemos con tiempo.'], 'Duración ≈30 s'),
  ver('B', 'pyr', 'Mi papá falleció en un accidente de trabajo', [
    L('0:00', 'E', 'Mi papá falleció en un accidente de trabajo. ¿Podemos reclamar algo?', 'Arranque · tono sobrio, sin música arriba'),
    L('0:04', 'V', 'Lo siento mucho. Y sí: la familia puede reclamar.', AV),
    L('0:08', 'E', '¿Quiénes?'),
    L('0:09', 'V', '(Sergio, en una frase.)', AV),
    L('0:14', 'E', '¿Hay apuro?'),
    L('0:15', 'V', 'Los reclamos tienen plazo. Mejor consultarlo con tiempo.', AV)],
    'Si te pasó, mandanos un mensaje o comentá CONSULTA. Te escribimos por privado.',
    ['Mi papá falleció en un accidente de trabajo. ¿Podemos reclamar algo?', 'Si perdiste a alguien en un accidente de trabajo, esto te importa.',
     'La familia también puede reclamar.', 'Una pregunta difícil, con una respuesta corta.'],
    ['Si te pasó, mandanos un mensaje o comentá CONSULTA. Te escribimos por privado.', 'Escribinos por privado, sin apuro.',
     'Mandáselo a quien lo necesite.']),
  ver('C', 'esverdad', '¿Es verdad que la familia no puede reclamar?', [
    L('0:00', 'E', 'Doctor, ¿es verdad que si el trabajador fallece la familia no puede reclamar nada?', 'Arranque · la pregunta en una caja'),
    L('0:05', 'V', 'Te lo respondo porque me lo preguntan mucho. No.', AV),
    L('0:08', 'V', 'La familia puede reclamar. (Sergio: quiénes.)', AV),
    L('0:14', 'V', 'Y cuenta aunque haya sido en el camino al trabajo.', AV),
    L('0:18', 'V', 'Lo que no hay que hacer es dejarlo pasar: los reclamos tienen plazo.', AV)],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje.',
    ['Doctor, ¿es verdad que si el trabajador fallece la familia no puede reclamar nada?', '¿Es verdad que la familia se queda sin nada?',
     'Te lo respondo porque me lo preguntan mucho.', 'No. Y te explico por qué.'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje.', 'Escribinos por privado.', 'Mandáselo a quien lo necesite.'])]))

# 08 · choque de atrás
T.append(tema('T08', '¿Siempre es culpa del que choca de atrás?', 'Carlos', 'CHOQUE', 'A',
  'tránsito tuvo cero reels el ciclo pasado y el animado ya tiene receta (R-17).', [
  ver('A', 'animado', 'Me chocaste de atrás: cuatro casos', [
    L('0:00', 'E', 'Me chocaste de atrás, la culpa es tuya.', 'Arranque · otra voz, en off · dos autos animados'),
    L('0:03', 'V', 'Casi siempre, sí. Pero mirá estos cuatro casos.', 'Sergio entra al costado'),
    L('0:06', 'P', 'CASO 1 · El de adelante tira marcha atrás y te pega → responde él.', AV),
    L('0:11', 'P', 'CASO 2 · Te chocan de atrás y te empujan contra el de adelante → responde el que empezó la cadena.', AV),
    L('0:17', 'P', 'CASO 3 · El de adelante frena de golpe, sin motivo → la culpa puede ser compartida.', AV),
    L('0:22', 'P', 'CASO 4 · Frena por el semáforo, un peatón o un perro → la culpa es tuya: tenías que mantener la distancia.', AV)],
    'Si te chocaron y te dicen que la culpa es tuya, comentá CHOQUE o mandanos un mensaje. Y mandáselo a ese amigo que maneja pegado.',
    ['Me chocaste de atrás, la culpa es tuya.', '¿Siempre es culpa del que choca de atrás? Casi siempre. Pero mirá estos cuatro casos.',
     'Cuatro choques de atrás y quién paga en cada uno.', 'Si chocás de atrás, no siempre es tuya la culpa.'],
    ['Si te chocaron y te dicen que la culpa es tuya, comentá CHOQUE o mandanos un mensaje. Y mandáselo a ese amigo que maneja pegado.',
     'Mandáselo a ese amigo que maneja pegado.', '¿En cuál te pasó? Comentá CHOQUE o escribinos.'], 'Duración ≈32 s'),
  ver('B', 'pyr', 'Me chocaron de atrás y dicen que frené de golpe', [
    L('0:00', 'E', 'Me chocaron de atrás y el otro dice que frené de golpe.', 'Arranque'),
    L('0:03', 'V', 'Casi siempre, el que choca de atrás es el responsable.', AV),
    L('0:07', 'E', '¿Y si de verdad frené?'),
    L('0:08', 'V', 'Si frenaste por algo, el semáforo o alguien que cruzaba, sigue siendo de él: tenía que mantener la distancia.', AV),
    L('0:15', 'E', '¿Y si frené sin motivo?'),
    L('0:16', 'V', 'Ahí la culpa puede ser compartida.', AV),
    L('0:19', 'V', 'Por eso: sacá fotos de cómo quedaron los autos antes de moverlos.')],
    'Si te chocaron de atrás, comentá CHOQUE o mandanos un mensaje.',
    ['Me chocaron de atrás y el otro dice que frené de golpe.', '«Frenaste de golpe.» Lo que te dicen cuando te chocan de atrás.',
     'Te chocaron de atrás y te quieren pasar la culpa.', 'Frenar no te hace culpable. Depende de por qué.'],
    ['Si te chocaron de atrás, comentá CHOQUE o mandanos un mensaje.', 'Comentá CHOQUE y te escribimos por privado.',
     'Mandáselo a alguien que maneja todos los días.']),
  ver('C', 'placa', '¿Siempre es culpa del que choca de atrás?', [
    L('0:00', 'P', '¿SIEMPRE ES CULPA DEL QUE CHOCA DE ATRÁS?', 'Arranque'),
    L('0:03', 'V', 'Casi siempre, sí. Pero hay casos que conviene conocer.', AV),
    L('0:07', 'V', 'Si el de adelante tira marcha atrás, responde él.', AV),
    L('0:11', 'V', 'Si te empujan contra el de adelante, responde el que empezó.', AV),
    L('0:15', 'V', 'Y si frenó de golpe sin motivo, la culpa puede ser compartida.', AV)],
    'Si te pasó, comentá CHOQUE o mandanos un mensaje.',
    ['¿Siempre es culpa del que choca de atrás?', 'Casi siempre, sí. Pero no siempre.',
     'Tres casos en los que la culpa no es del de atrás.', 'Chocaste de atrás. ¿Seguro que es tuya la culpa?'],
    ['Si te pasó, comentá CHOQUE o mandanos un mensaje.', 'Mandáselo a ese amigo que maneja pegado.', 'Comentá CHOQUE y te escribimos.'])]))

# 09 · qué traer (A = C-17)
c17, c17h = de_octubre('1A')
T.append(tema('T09', 'Qué traer a la primera consulta después de un choque', 'Carlos', 'CHOQUE', 'A',
  'ya está guionado (C-17 de octubre); el POV todavía no se usó en la cuenta.', [
  ver('A', 'pov', '«Tuve un choque»', c17, 'Si te pasó un choque, comentá CHOQUE o mandanos un mensaje, y te decimos por dónde empezar.',
    c17h or ['Tuve un choque. Vengo a consultar qué se puede hacer.'],
    ['Si te pasó un choque, comentá CHOQUE o mandanos un mensaje, y te decimos por dónde empezar.', 'Guardalo para cuando te toque.',
     'Mandáselo a alguien que maneja todos los días.'], 'Duración ≈42 s'),
  ver('B', '60s', 'Lo que tenés que juntar después de un choque, contra reloj', [
    L('0:00', 'V', 'Lo que tenés que juntar después de un choque, antes de que se termine el reloj.', 'Arranque · reloj en 01:00'),
    L('0:04', 'V', 'Fotos de los dos autos y del lugar.', 'En pantalla: FOTOS'),
    L('0:08', 'V', 'Patente, nombre y seguro del otro.', 'En pantalla: EL OTRO'),
    L('0:12', 'V', 'La denuncia en tu seguro.', AV + ' · En pantalla: DENUNCIA'),
    L('0:16', 'V', 'La constancia de la guardia y los recibos de lo que gastaste.', 'En pantalla: GUARDIA'),
    L('0:21', 'V', 'Si alguien vio todo, su teléfono.', 'En pantalla: TESTIGOS'),
    L('0:25', 'V', 'Y si no pudiste trabajar, tu recibo de sueldo.', 'En pantalla: RECIBO')],
    'Si te pasó, comentá CHOQUE o mandanos un mensaje y te decimos por dónde empezar.',
    ['Lo que tenés que juntar después de un choque, antes de que se termine el reloj.', 'Seis cosas después de un choque, en sesenta segundos.',
     'Te chocaron. Tenés un minuto: juntá esto.', 'Contra reloj: lo que no podés no tener después de un choque.'],
    ['Si te pasó, comentá CHOQUE o mandanos un mensaje y te decimos por dónde empezar.', 'Guardalo para cuando te toque.',
     'Mandáselo a alguien que maneja todos los días.'], 'Duración ≈45 s'),
  ver('C', 'papel', 'Lo que hay que traer, uno por uno sobre la mesa', [
    L('0:00', 'V', 'Esto es lo que nos tenés que traer después de un choque.', 'Arranque · escritorio vacío'),
    L('0:03', 'V', 'Las fotos de los autos y del lugar.', 'La mano deja las fotos impresas'),
    L('0:07', 'V', 'Los datos del otro y de su seguro.', 'Un papel con datos tapados'),
    L('0:11', 'V', 'La denuncia que hiciste.', AV),
    L('0:15', 'V', 'La constancia de la guardia y los recibos.'),
    L('0:19', 'V', 'Y si no pudiste trabajar, tu recibo de sueldo.'),
    L('0:23', 'V', 'Si te falta algo, se consigue. Pero con esto no arrancamos de cero.')],
    'Si te pasó, comentá CHOQUE o mandanos un mensaje.',
    ['Esto es lo que nos tenés que traer después de un choque.', 'Lo que tiene que haber sobre esta mesa el primer día.',
     'Seis papeles que hacen que no arranquemos de cero.', 'Después de un choque, esto vale oro.'],
    ['Si te pasó, comentá CHOQUE o mandanos un mensaje.', 'Guardalo para cuando te toque.', 'Comentá CHOQUE y te escribimos por privado.'])]))

# 10 · lo que te ofrece el seguro (A = C-16)
c16, c16h = de_octubre('1B')
T.append(tema('T10', 'Lo que te ofrece el seguro', 'Carlos', 'CHOQUE', 'A', 'ya está guionado (C-16 de octubre).', [
  ver('A', 'pov', '«Me ofrecieron esto por el choque»', c16,
    'Si te ofrecieron algo y todavía no firmaste, comentá CHOQUE o mandanos un mensaje, y lo miramos antes de que firmes.',
    c16h or ['...estuve un mes sin poder laburar. Y me ofrecieron esto.'],
    ['Si te ofrecieron algo y todavía no firmaste, comentá CHOQUE o mandanos un mensaje, y lo miramos antes de que firmes.',
     'Comentá CHOQUE y te escribimos por privado.', 'Mandáselo a alguien al que le acaban de ofrecer algo.'], 'Duración ≈40 s'),
  ver('B', 'chat', 'El mensaje del seguro', [
    L('0:00', 'C', 'Seguro: Te ofrecemos cerrar hoy. (el monto, borroneado)', 'Arranque · sin cifra legible'),
    L('0:03', 'C', 'Vos: ¿Y eso por qué?'),
    L('0:05', 'C', 'Seguro: Es lo que corresponde por los daños.'),
    L('0:07', 'V', 'Ese número lo calcularon mirando el auto.', AV),
    L('0:11', 'V', '¿Y tu lesión? ¿Y los días que no fuiste a trabajar? Eso se mira aparte.', AV),
    L('0:17', 'V', 'Antes de contestar «dale», que alguien lo mire.')],
    'Si te llegó un mensaje así, comentá CHOQUE o mandanos una captura y lo vemos.',
    ['«Te ofrecemos cerrar hoy.» ¿Te llegó este mensaje?', 'Si el seguro te escribió esto, no contestes todavía.',
     '«Es lo que corresponde.» No siempre.', 'Este mensaje llega a los pocos días del choque.'],
    ['Si te llegó un mensaje así, comentá CHOQUE o mandanos una captura y lo vemos.', 'Guardá el chat y escribinos.',
     'Comentá CHOQUE y te escribimos por privado.']),
  ver('C', 'esverdad', '¿Es verdad que lo que te ofrece el seguro es lo que te corresponde?', [
    L('0:00', 'E', 'Doctor, ¿es verdad que lo que te ofrece el seguro es lo que te corresponde?', 'Arranque · la pregunta en una caja'),
    L('0:04', 'V', 'Te lo respondo porque me lo preguntan mucho. No necesariamente.', AV),
    L('0:08', 'V', 'Lo que te ofrecen sale de mirar el auto.', AV),
    L('0:12', 'V', 'Lo que te corresponde sale de mirarte a vos: la lesión, el tratamiento y los días que no trabajaste.', AV),
    L('0:19', 'V', 'Son dos cuentas distintas.')],
    'Si te ofrecieron algo, comentá CHOQUE o mandanos un mensaje antes de firmar.',
    ['Doctor, ¿es verdad que lo que te ofrece el seguro es lo que te corresponde?', '¿Es verdad que el seguro te paga lo justo?',
     'Lo que te ofrecen y lo que te corresponde son dos cuentas distintas.', 'Te lo respondo porque me lo preguntan mucho.'],
    ['Si te ofrecieron algo, comentá CHOQUE o mandanos un mensaje antes de firmar.', 'Comentá CHOQUE y te escribimos por privado.',
     'Mandáselo a alguien que acaba de chocar.'])]))

# 11 · solo o con abogado
T.append(tema('T11', 'Arreglar con el seguro: solo o con abogado', 'Carlos', 'CHOQUE', 'A',
  'es el formato de la referencia tal cual; dos personas en cámara (las colaboraciones son lo que más rinde en la cuenta).', [
  ver('A', 'solovs', 'Arreglar con el seguro: solo vs con abogado', [
    L('0:00', 'S', 'Me ofrecieron una plata rápido y firmé.', 'Arranque · arriba: SIN ABOGADO / CON ABOGADO'),
    L('0:03', 'K', 'A mí me ofrecieron lo mismo, pero mi abogado lo rechazó en el acto.'),
    L('0:07', 'K', 'Me mandó al médico para documentar la lesión.', AV),
    L('0:10', 'S', 'Yo con eso no llegué a pagar ni los repuestos. Y la kinesio me salió de mi bolsillo.'),
    L('0:16', 'K', 'Yo no puse un peso. Reclamamos los gastos médicos y los días que no pude ir a trabajar.', AV + ' · «no puse un peso» depende de cómo cobra el estudio'),
    L('0:23', 'V', 'La aseguradora no es tu amiga. Es una empresa, y su negocio es pagarte lo menos posible.', 'A cámara')],
    'Antes de firmar, comentá CHOQUE o mandanos un mensaje.',
    ['Me ofrecieron una plata rápido y firmé.', 'Mismo choque, mismo seguro, dos decisiones distintas.',
     'Arreglar con el seguro: solo o con abogado.', 'Los dos tuvieron el mismo choque. Uno firmó.'],
    ['Antes de firmar, comentá CHOQUE o mandanos un mensaje.', 'La aseguradora no es tu amiga: comentá CHOQUE o escribinos.',
     'Mandáselo a alguien que está por firmar.'], 'Duración ≈35 s'),
  ver('B', 'cadena', 'El seguro me ofrece arreglar rápido. ¿Acepto?', [
    L('0:00', 'E', 'Doctor, el seguro me ofrece arreglar rápido. ¿Acepto?', 'Arranque · la pregunta en una caja'),
    L('0:03', 'V', 'Cuidado. Primero fijate qué incluye.'),
    L('0:06', 'E', '¿Y si necesito la plata ya?'),
    L('0:08', 'V', 'Lo entiendo. Pero lo que firmás hoy después no se vuelve a abrir.', AV),
    L('0:13', 'E', '¿Y la kinesio quién la paga?'),
    L('0:15', 'V', 'Eso también se reclama, igual que los días que no fuiste a trabajar.', AV),
    L('0:20', 'V', 'No improvises: primero que lo mire alguien, después decidís.')],
    'Si te ofrecieron arreglar, comentá CHOQUE o mandanos un mensaje.',
    ['Doctor, el seguro me ofrece arreglar rápido. ¿Acepto?', 'Te ofrecen arreglar rápido. Tres preguntas antes de aceptar.',
     '«¿Y si necesito la plata ya?» Te contesto.', 'Arreglar rápido con el seguro: lo que nadie te pregunta.'],
    ['Si te ofrecieron arreglar, comentá CHOQUE o mandanos un mensaje.', 'No improvises: comentá CHOQUE o escribinos.',
     'Mandáselo a alguien que está por firmar.']),
  ver('C', 'jamas', 'Jamás arregles con el seguro sin revisar esto', [
    L('0:00', 'V', 'Jamás arregles con el seguro sin revisar esto.', 'Arranque'),
    L('0:03', 'V', 'Uno: si incluye tu lesión, no solo el auto.', AV + ' · En pantalla: 1'),
    L('0:07', 'V', 'Dos: si incluye lo que gastaste en médicos y remedios.', AV + ' · En pantalla: 2'),
    L('0:11', 'V', 'Tres: si incluye los días que no pudiste trabajar.', AV + ' · En pantalla: 3'),
    L('0:15', 'V', 'Si falta una, no firmes.')],
    'Si estás por arreglar, comentá CHOQUE o mandanos un mensaje.',
    ['Jamás arregles con el seguro sin revisar esto.', 'Tres cosas que tiene que incluir el arreglo con el seguro.',
     'Antes de firmar con el seguro, mirá estas tres.', 'Si el arreglo no dice esto, no firmes.'],
    ['Si estás por arreglar, comentá CHOQUE o mandanos un mensaje.', 'Guardalo para cuando te toque.', 'Mandáselo a alguien que está por firmar.'])]))

# 12 · las excusas para no consultar
T.append(tema('T12', 'Las excusas para no consultar', 'amplio', 'CONSULTA', 'A',
  'es el formato que más te gustó y se graba en una sola toma.', [
  ver('A', '60s', 'Seis excusas para no consultar, en sesenta segundos', [
    L('0:00', 'V', 'Seis excusas para no consultar, en sesenta segundos.', 'Arranque · reloj en 01:00'),
    L('0:03', 'E', 'Lo voy a pensar.'),
    L('0:04', 'V', '¿Qué querés pensar? ¿Si tenés caso? Eso te lo decimos nosotros.'),
    L('0:08', 'E', 'Un abogado es caro.'),
    L('0:09', 'V', 'Caro es firmar lo primero que te ofrecen.', AV + ' · sin prometer nada de honorarios'),
    L('0:12', 'E', 'Lo hablo con mi señora.'),
    L('0:13', 'V', 'Buenísimo. Vengan los dos y lo vemos juntos.'),
    L('0:16', 'E', 'No es el momento.'),
    L('0:17', 'V', '¿Qué tiene que pasar para que sea el momento? Los reclamos tienen plazo.', AV),
    L('0:21', 'E', 'Mandame información.'),
    L('0:22', 'V', '¿Qué querés saber? Te lo digo ahora, más rápido que un mail.'),
    L('0:25', 'E', 'Lo arreglo solo con el seguro.'),
    L('0:27', 'V', 'Perfecto. ¿Y cómo vas a saber si lo que te ofrecen es poco?'),
    L('0:30', 'V', 'Cada excusa es una duda disfrazada.')],
    'Comentá CONSULTA o mandanos un mensaje, y la duda te la sacamos hoy.',
    ['Seis excusas para no consultar, en sesenta segundos.', 'Seis excusas que escuchamos todas las semanas. Tengo un minuto.',
     '«Lo voy a pensar.» Y otras cinco, contra reloj.', 'Un minuto, seis excusas, seis respuestas.'],
    ['Comentá CONSULTA o mandanos un mensaje, y la duda te la sacamos hoy.', '¿Cuál de las seis es la tuya? Comentá CONSULTA o escribinos.',
     'Mandáselo a alguien que lo viene pensando hace meses.'], 'Duración ≈40 s'),
  ver('B', 'cadena', '¿Y si lo pienso un tiempo?', [
    L('0:00', 'E', 'Doctor, ¿y si lo pienso un tiempo?', 'Arranque · la pregunta en una caja'),
    L('0:03', 'V', 'Cuidado: los reclamos tienen plazo.', AV),
    L('0:06', 'E', '¿Y si sale caro?'),
    L('0:07', 'V', 'Caro es firmar lo primero que te ofrecen.'),
    L('0:10', 'E', '¿Y si no tengo caso?'),
    L('0:11', 'V', 'Te lo decimos y listo.'),
    L('0:13', 'V', 'No improvises: primero preguntá, después decidís.')],
    'Comentá CONSULTA o mandanos un mensaje.',
    ['Doctor, ¿y si lo pienso un tiempo?', 'Las tres dudas antes de consultar, contestadas.',
     '¿Y si no tengo caso? Te contesto.', 'Lo estás pensando hace meses. Escuchá esto.'],
    ['Comentá CONSULTA o mandanos un mensaje.', 'No improvises: comentá CONSULTA o escribinos.', 'Mandáselo a alguien que lo viene pensando.']),
  ver('C', 'solovs', 'El que lo pensó y el que consultó', [
    L('0:00', 'S', 'Yo lo estoy pensando.', 'Arranque · arriba: LO PENSÓ / CONSULTÓ'),
    L('0:02', 'K', 'Yo ya consulté.'),
    L('0:04', 'S', 'Es que me da miedo que salga caro.'),
    L('0:06', 'K', 'A mí me dijeron primero si tenía caso. Después hablamos de lo otro.', AV),
    L('0:11', 'S', 'Y mientras, el seguro me sigue llamando.'),
    L('0:14', 'K', 'A mí ya no: ahora hablan con mi abogado.'),
    L('0:17', 'V', 'Pensarlo está bien. Pero los reclamos tienen plazo.', 'A cámara · ' + AV)],
    'Comentá CONSULTA o mandanos un mensaje.',
    ['Yo lo estoy pensando. Yo ya consulté.', 'Mismo accidente: uno lo pensó, el otro consultó.',
     'Los dos tenían la misma duda. Uno preguntó.', 'Lo que pasa mientras lo pensás.'],
    ['Comentá CONSULTA o mandanos un mensaje.', 'Mandáselo a alguien que lo viene pensando.', 'Comentá CONSULTA y te escribimos por privado.'])]))

# 13 · feriado
T.append(tema('T13', 'Trabajar un feriado', 'amplio', 'CONSULTA', 'A',
  'es la fila «Jamás» que ya se usó con Lucía; solo tiene sentido publicarlo antes de un feriado.', [
  ver('A', 'jamas', 'Jamás trabajes un feriado sin saber esto', [
    L('0:00', 'V', 'Jamás trabajes un feriado sin saber esto.', 'Arranque'),
    L('0:03', 'V', 'Uno: no se paga como un día normal.', AV + ' · En pantalla: 1'),
    L('0:07', 'V', 'Dos: tiene que figurar aparte en tu recibo.', AV + ' · En pantalla: 2'),
    L('0:11', 'V', 'Tres: si no te lo pagaron bien, se puede reclamar.', AV + ' · En pantalla: 3')],
    'Si trabajaste un feriado y no te lo pagaron bien, comentá CONSULTA o mandanos un mensaje.',
    ['Jamás trabajes un feriado sin saber esto.', 'Si te toca trabajar el feriado, mirá esto.',
     'Tres cosas que tiene que tener tu recibo si trabajaste un feriado.', 'El feriado no se paga como un día normal.'],
    ['Si trabajaste un feriado y no te lo pagaron bien, comentá CONSULTA o mandanos un mensaje.', 'Mandáselo a alguien que trabaja el feriado.',
     'Guardalo para el próximo feriado.']),
  ver('B', 'placa', '¿Te pueden hacer trabajar un feriado?', [
    L('0:00', 'P', '¿TE PUEDEN HACER TRABAJAR UN FERIADO?', 'Arranque'),
    L('0:03', 'V', 'Depende del trabajo. Pero si lo trabajás, no se paga como un día cualquiera.', AV),
    L('0:08', 'V', 'Tiene que figurar en tu recibo.', AV),
    L('0:11', 'V', 'Y si no te lo pagaron bien, se puede reclamar.', AV)],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje.',
    ['¿Te pueden hacer trabajar un feriado?', 'Te toca trabajar el feriado. Esto te tienen que pagar.',
     'El feriado trabajado no es un día más.', 'Antes del fin de semana largo, mirá esto.'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje.', 'Mandáselo a alguien que trabaja el feriado.', 'Guardalo para el próximo feriado.']),
  ver('C', 'pyr', 'Me pagaron el feriado como un día normal', [
    L('0:00', 'E', 'Me hicieron trabajar el feriado y me lo pagaron como un día normal.', 'Arranque'),
    L('0:03', 'V', 'Eso no está bien. El feriado trabajado se paga distinto.', AV),
    L('0:07', 'E', '¿Y cómo me doy cuenta?'),
    L('0:08', 'V', 'Fijate en tu recibo: tiene que figurar aparte.', AV),
    L('0:11', 'E', '¿Y si no figura?'),
    L('0:12', 'V', 'Se puede reclamar. Guardá el recibo.', AV)],
    'Si te pasó, comentá CONSULTA o mandanos un mensaje.',
    ['Me hicieron trabajar el feriado y me lo pagaron como un día normal.', 'Trabajaste el feriado. ¿Te lo pagaron bien?',
     'El feriado trabajado se paga distinto. Te explico.', 'Fijate esto en tu recibo después del feriado.'],
    ['Si te pasó, comentá CONSULTA o mandanos un mensaje.', 'Comentá CONSULTA y te escribimos por privado.', 'Mandáselo a alguien que trabajó el feriado.'])],
  aviso='Si nadie lo elige para antes del fin de semana largo de diciembre, vuelve al banco.'))

# hechos: los cuatro publicados
def hecho(r, k, tipo, titulo, ej, ejde, meta, pal):
    lin, _ = de_octubre(k)
    return {'r': r, 'tipo': tipo, 'titulo': titulo, 'meta': meta, 'ej': ej, 'ejde': ejde, 'nota': '', 'lineas': lin,
            'cierre': 'Comentá ' + pal + ' o mandanos un mensaje.', 'hooks': [], 'cierres': [], 'hookIdx': 0, 'versiones': []}

H = [
  hecho('B-G3', '3B', 'Pregunta y respuesta · Diego · DESPIDO', 'Despidos', 'DeuyEQRp-cp', 'El reel publicado', 'Publicado el 20-10 · 2.772 vistas · 6 seguidores nuevos · el mejor de la cuenta', 'DESPIDO'),
  hecho('D-08', '2A', 'Jamás · Diego · DESPIDO', 'Jamás te vayas de un trabajo sin cobrar esto', 'De-KjTUpS4c', 'El reel publicado', 'Publicado el 26-10 · 1.229 vistas · 4 compartidos', 'DESPIDO'),
  hecho('B-G4', '3A', 'Pregunta y respuesta · Mónica · CONSULTA', '¿Firmar o no firmar?', 'DfQK3ctBpza', 'El reel publicado', 'Publicado el 02-11 · 650 vistas · 1 seguidor nuevo', 'CONSULTA'),
  hecho('R-17', '2B', 'Sí, podés · Roberto · ART', 'No hace falta un accidente', 'Dfp3W1nBWJN', 'El reel publicado', 'Publicado el 12-11 · 530 vistas a los 4 días', 'ART'),
]

ORDEN = ['T01', 'T12', 'T08', 'T07', 'T02', 'T09']
PORQUE = {
  'T01': 'Semana del 24-11. Despido es lo que más rinde en la cuenta, y diciembre lo pide.',
  'T12': 'Semana del 01-12. El formato que más te gustó; se graba en una sola toma.',
  'T08': 'Semana del 08-12. Tránsito tuvo cero reels el ciclo pasado; antes de las rutas de las fiestas.',
  'T07': 'Semana del 15-12. La mecánica del reel que más rindió en el rubro este mes; el único para Mónica.',
  'T02': 'Semana del 22-12. Despido otra vez, justo antes de fin de año.',
  'T09': 'Semana del 29-12. Ya guionado (C-17).',
}

D = {
  'titulo': 'Un reel por semana. Elegí cuál grabás.',
  'intro': [
    'Acá están los videos para lo que queda del año: trece temas, y cada uno en tres formatos distintos (A, B y C). Se publica uno por semana, así que no hace falta grabarlos todos: cada abogado del estudio elige los que quiere hacer.',
    'Arriba, «Para grabar ahora», el orden que sugerimos si nadie elige otro. Abajo, «Para más adelante», el resto. Y al final, «Hechos», los cuatro que ya se publicaron, con sus números.',
    'Cada versión tiene a la derecha el video que la inspiró. Tocá las letras A, B o C para cambiar de formato.',
    'Todos los textos se pueden cambiar: tocá cualquier frase y escribí encima. Se guarda solo. Abajo de cada guion hay otros arranques y cierres para elegir.',
    'Lo marcado «A validar» lo tiene que confirmar Sergio antes de publicar. Ninguno lleva cifras ni artículos de ley.',
  ],
  'reglas': [
    'Un reel por semana, los martes.',
    'Todos cierran pidiendo un comentario con la palabra (CHOQUE, ART, DESPIDO o CONSULTA) o un mensaje.',
    'Cuando un reel se graba, tocá «Marcar hecho» y pasa a la fila «Hechos».',
  ],
  'refs': [],
  'tanda': {'titulo': 'Para grabar ahora', 'resumen': 'El orden sugerido, uno por semana. Cada tema en tres formatos, con su referencia al lado. Abre en la versión recomendada',
            'items': T + H, 'variaciones': []},
  'jornada': {'orden': ORDEN, 'porque': PORQUE},
  'hechos': [h['r'] for h in H],
}
src = ('/* Guiones de noviembre-diciembre 2026 · Sergio Rosa y Asociados. Lo genera armar-tablero.py: no editar a mano.\n'
       '   Fuente: vault-obsidian-git/clientes/sergio-rosa/REELS-2026-11.md. */\nwindow.GUIONES = ' + json.dumps(D, ensure_ascii=False, indent=1) + ';\n')
open('guiones.js', 'w', encoding='utf8').write(src)
print('ok', len(T), 'temas,', sum(1 + len(t['versiones']) for t in T), 'versiones,', len(H), 'hechos')
