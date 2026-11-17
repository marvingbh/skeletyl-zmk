import re, json, sys, pathlib
km = open(pathlib.Path(__file__).resolve().parent.parent / 'config/skeletyl.keymap').read()
names = {'base_layer':'Base','fn_layer':'FN','nav_layer':'NAV','ptr_layer':'Mouse','num_layer':'NUM','sym_layer':'SYM'}
LN = {1:'FN',2:'NAV',3:'Mouse',4:'NUM',5:'SYM'}
MOD = {'LGUI':'⌘','RGUI':'⌘','LALT':'⌥','RALT':'⌥','LCTRL':'⌃','RCTRL':'⌃','LSHFT':'⇧','RSHFT':'⇧'}
K = {'SPACE':'Space','RET':'Enter','ESC':'Esc','TAB':'Tab','BSPC':'⌫','DEL':'Del','SQT':"'",'COMMA':',','DOT':'.','FSLH':'/',
     'LBKT':'[','RBKT':']','EQUAL':'=','BSLH':'\\','MINUS':'-','SEMI':';','GRAVE':'`','UP':'↑','DOWN':'↓','LEFT':'←','RIGHT':'→',
     'CAPS':'Caps','END':'End','HOME':'Home','PG_UP':'PgUp','PG_DN':'PgDn','INS':'Ins','PSCRN':'PrtSc','SLCK':'ScrLk','PAUSE_BREAK':'Pause'}
SH = {'N1':'!','N2':'@','N3':'#','N4':'$','N5':'%','N6':'^','N7':'&','N8':'*','N9':'(','N0':')','LBKT':'{','RBKT':'}','EQUAL':'+',
      'BSLH':'|','MINUS':'_','SEMI':':','GRAVE':'~','DOT':'>','COMMA':'<','SQT':'"','FSLH':'?'}
def key(k):
    m = re.fullmatch(r'LS\((\w+)\)', k)
    if m: return SH[m.group(1)]
    if k in MOD: return MOD[k]
    if re.fullmatch(r'N\d', k): return k[1]
    if re.fullmatch(r'F\d+', k): return k
    return K.get(k, k)
out = {}
for blk, nm in names.items():
    body = re.search(blk + r'\s*\{\s*bindings = <(.*?)>;', km, re.S).group(1)
    toks = re.findall(r'&\w+(?: [\w()]+)*', body)
    toks = re.findall(r'&(\w+)((?: (?:[A-Z_0-9]+(?:\([A-Z_0-9]+\))?|\d+))*)', body)
    keys = []
    for b, args in toks:
        a = args.split()
        if b == 'kp': keys.append({'t': key(a[0])})
        elif b in ('hml','hmr','hms','hsl','hsr'): keys.append({'t': key(a[1]), 'h': MOD[a[0]]})
        elif b == 'lt': keys.append({'t': key(a[1]), 'h': LN[int(a[0])], 'l': 1})
        elif b == 'trans': keys.append({'t':'▽','x':1})
        elif b == 'none': keys.append({'t':''})
        elif b == 'bootloader': keys.append({'t':'Boot','s':1})
        elif b == 'out': keys.append({'t':'USB/BT','s':1})
        elif b == 'bt': keys.append({'t':'BT clear' if a[0]=='BT_CLR' else 'BT '+a[1],'s':1})
        elif b == 'mkp': keys.append({'t':{'LCLK':'L click','RCLK':'R click','MCLK':'Mid click'}[a[0]]})
        else: raise SystemExit(b)
    assert len(keys) == 36, (nm, len(keys))
    out[nm] = keys
# the guide's mouse layer kept base Z// as ▽; trans shows that already
js = '  var L = ' + json.dumps(out, ensure_ascii=False) + ';'
hold = '''  var hold = { FN: "hold <b>Esc</b> (left inner thumb)", NAV: "hold <b>Enter</b> (right thumb)", Mouse: "hold <b>Z</b> or <b>/</b>",
               NUM: "hold <b>Space</b> or <b>Del</b>", SYM: "hold <b>Tab</b> (left outer thumb) or <b>⌫</b>", Base: "Normal typing. Nothing held." };'''
for f in sys.argv[1:]:
    s = open(f).read()
    s, n1 = re.subn(r'  var L = \{.*?\};\n', lambda m: js + '\n', s, count=1)
    s, n2 = re.subn(r'  var hold = \{.*?\};', lambda m: hold, s, count=1, flags=re.S)
    assert n1 == 1 and n2 == 1, f
    open(f, 'w').write(s)
    print('patched', f)
print(' '.join(k['t'] for k in out['SYM']))
