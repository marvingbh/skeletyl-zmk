import sys, runpy, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from build123d import *
script, png, pcb = sys.argv[1:4]
sys.argv = [script, pcb, '/private/tmp/claude-501/-Users-marcus-personal/0fdb6f46-01a0-4251-bdb0-324ae5f6b378/scratchpad/case/out']
g = runpy.run_path(script, run_name='__main__')
sys.argv = ['check', script, png]
tray, cover = g['tray'], g['cover']
def outline(face):
    pts=[]
    for w in face.wires():
        vs=[v for v in w.positions(np.linspace(0,1,400))]
        pts.append(np.array([[p.X,p.Y] for p in vs]))
    return pts
fig,axs=plt.subplots(1,2,figsize=(18,8),gridspec_kw={'width_ratios':[1.4,1]})
ax=axs[0]
for f,c,lab in [(g['outer'],'#3060a0','case outer'),(g['inner_f'],'#80a0d0','case inner'),(g['pcb_face'],'k','PCB'),(g['cover_out'],'#e08030','cover')]:
    for i,p in enumerate(outline(f)): ax.plot(p[:,0],p[:,1],color=c,lw=1.2 if c!='k' else 0.8,label=lab if i==0 else None)
P=g['P']
mx,my=g['mcu_x'],g['mcu_y']
ax.add_patch(plt.Rectangle((mx-9,-(my+16.65)),18,33.3,fill=False,color='red',lw=1.5,label='nice!nano (18x33)'))
ax.add_patch(plt.Rectangle((mx-4.5,-(my-16.65)-0.5),9,1.5+0.5,color='red'))
bx0=g['pod_x0']+g['BAT_CLR']; by0=g['pod_y0']+g['BAT_CLR']+1
ax.add_patch(plt.Rectangle((bx0,-(by0+g['BAT'][1])),g['BAT'][0],g['BAT'][1],fill=False,color='green',lw=1.5,label='bateria 20x38'))
px,py=g['psw_x'],g['psw_y']; ax.add_patch(plt.Rectangle((px-3.5,-(py+1.5)),7,3,color='purple',label='chave liga/desliga'))
for h in g['holes']:
    x,y=P(*h); ax.add_patch(plt.Circle((x,y),1.7,color='blue' if h in g['TRAY_HOLES'] else 'orange'))
ax.set_aspect('equal'); ax.legend(fontsize=8,loc='lower left'); ax.grid(lw=0.2); ax.set_title('Vista de cima (lado esquerdo)')
# cross-section through MCU centre, along x
ax=axs[1]
yc=-my
for part,c in [(tray,'#3060a0'),(cover,'#e08030')]:
    sec = part & Box(500,0.2,100,align=(Align.CENTER,Align.CENTER,Align.MIN)).moved(Location((0,yc,-10)))
    for f in sec.faces():
        if abs(f.normal_at().Y)>0.9:
            for w in f.wires():
                pts=np.array([[p.X,p.Z] for p in w.positions(np.linspace(0,1,300))]); ax.fill(pts[:,0],pts[:,1],color=c,alpha=0.85,lw=0)
zb,zt=g['Z_PCB_BOT'],g['Z_PCB_TOP']
ax.add_patch(plt.Rectangle((min(p[0] for p in g['loop']),zb),g['X_EDGE']-min(p[0] for p in g['loop']),zt-zb,color='green',alpha=0.6,label='PCB'))
ax.add_patch(plt.Rectangle((mx-9,zt+2.5),18,1.2+1.5,color='red',alpha=0.6,label='nice!nano em headers (~2.5mm)'))
ax.add_patch(plt.Rectangle((bx0,g['FLOOR']),g['BAT'][0],g['BAT'][2],color='lime',alpha=0.6,label='bateria 9mm'))
ax.set_xlim(195,270); ax.set_aspect('equal'); ax.legend(fontsize=8,loc='upper left'); ax.grid(lw=0.2); ax.set_title(f'Corte na altura do controlador (y={my})')
plt.tight_layout(); fig.savefig(sys.argv[2],dpi=95)
