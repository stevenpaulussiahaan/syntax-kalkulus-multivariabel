import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT='/tmp/kalkulus/assets/img/'; BL,RD,GR,OR='#1f5fa8','#c0392b','#1e8449','#d68910'
def save(fig,n): fig.savefig(OUT+n,dpi=130,bbox_inches='tight'); plt.close(fig)
x=np.linspace(0,4,400)
fig,ax=plt.subplots(1,3,figsize=(11,3.4))
ax[0].plot(x,.4*np.exp(3*x/3)*0+ (2/5)*np.exp(-3*x*0)*0+ 0.5*np.exp(-x)+0.5*np.exp(-4*x),color=BL); ax[0].set_title('$r_1\\neq r_2$ real: $e^{-x}$, $e^{-4x}$')
ax[1].plot(x,(1+3*x)*np.exp(-x),color=GR); ax[1].set_title('$r$ ganda: $(c_1+c_2x)e^{-x}$')
ax[2].plot(x,np.exp(-.5*x)*(np.cos(3*x)+.5*np.sin(3*x)),color=RD); ax[2].plot(x,np.exp(-.5*x),'k--',lw=.8); ax[2].plot(x,-np.exp(-.5*x),'k--',lw=.8); ax[2].set_title('$r=-0.5\\pm 3i$: osilasi teredam')
for a in ax: a.grid(alpha=.3); a.set_xlabel('$x$'); a.axhline(0,color='k',lw=.5)
save(fig,'b17-1-kasus.png')
t=np.linspace(0,6,600); fig,ax=plt.subplots(figsize=(6.2,3.6))
ax.plot(t,np.exp(-t)*(np.cos(2*t)+.5*np.sin(2*t)),color=RD,label='kurang teredam $c=2,k=5$')
ax.plot(t,(1+2*t)*np.exp(-2*t),color=GR,label='teredam kritis $c=4,k=4$')
ax.plot(t,(4*np.exp(-t)-np.exp(-4*t))/3,color=BL,label='lewat teredam $c=5,k=4$')
ax.axhline(0,color='k',lw=.5); ax.grid(alpha=.3); ax.set_xlabel('$t$'); ax.set_ylabel('$x$'); ax.legend(fontsize=8); save(fig,'b17-3-redaman.png')
t=np.linspace(0,30,1500); fig,(a,b)=plt.subplots(1,2,figsize=(10,3.5))
a.plot(t,t/6*np.sin(3*t),color=BL); a.plot(t,t/6,'k--',lw=.7); a.plot(t,-t/6,'k--',lw=.7); a.set_title("Resonansi $x''+9x=\\cos3t$"); a.set_xlabel('$t$'); a.grid(alpha=.3)
w=np.linspace(0,4,400); b.plot(w,2/np.sqrt((4-w**2)**2+.25*w**2),color=RD); b.set_title('Amplitudo keadaan tunak ($m=1,c=0.5,k=4,F=2$)'); b.set_xlabel('$\\omega$'); b.grid(alpha=.3)
save(fig,'b17-3-resonansi.png')
x=np.linspace(0,7,500); fig,ax=plt.subplots(figsize=(6.2,3.8))
ax.plot(x,np.cos(x),'k',lw=2,label='$\\cos x$')
from math import factorial
for N,c in [(2,GR),(4,OR),(8,BL)]:
    s=sum((-1)**n*x**(2*n)/factorial(2*n) for n in range(N//2+1)); ax.plot(x,s,color=c,label='derajat %d'%N)
ax.set_ylim(-3,3); ax.grid(alpha=.3); ax.legend(fontsize=8); ax.set_xlabel('$x$'); save(fig,'b17-4-deret.png')
print('ok')
