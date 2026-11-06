import sys; sys.path.insert(0,'/tmp/kalkulus/python')
from figs_b12 import *
import numpy as np
def save(fig,n): fig.savefig(OUT+n,dpi=130,bbox_inches='tight'); plt.close(fig)

# heliks
fig,ax=ax3(); t=np.linspace(0,4*np.pi,400)
ax.plot(np.cos(t),np.sin(t),t,color=BL,lw=2)
ax.plot(np.cos(t),np.sin(t),0*t,color=GY,lw=1,ls='--')
lim(ax,(-1.3,1.3),(-1.3,1.3),(0,13)); save(fig,'b13-1-heliks.png')

# kubik terpilin + sekan
fig,ax=ax3(elev=20,azim=-120); t=np.linspace(-0.2,2.2,300)
ax.plot(t,t**2,t**3,color=BL,lw=2)
s=np.linspace(-0.3,1.3,10); ax.plot(1+s,1+3*s,1+7*s,color=RD,lw=1.8)
for p in [(1,1,1),(2,4,8)]: ax.scatter(*p,color=RD,s=30)
lim(ax,(-0.3,2.5),(-0.5,5.5),(-1,9)); save(fig,'b13-1-kubik.png')

# silinder-bidang
fig,ax=ax3(elev=20,azim=-50); t=np.linspace(0,2*np.pi,300)
ax.plot(np.cos(t),np.sin(t),2-np.sin(t),color=BL,lw=2.2)
ph=np.linspace(0,2*np.pi,40); z=np.linspace(0,3.5,2); P,Z=np.meshgrid(ph,z)
ax.plot_surface(np.cos(P),np.sin(P),Z,color=GY,alpha=0.12,linewidth=0)
lim(ax,(-1.4,1.4),(-1.4,1.4),(0,3.5)); save(fig,'b13-1-irisan.png')

# tangen kubik di t=1
fig,ax=ax3(elev=20,azim=-120); t=np.linspace(0,1.8,300)
ax.plot(t,t**2,t**3,color=BL,lw=2)
arrow(ax,(1,1,1),(2,3,4),RD,2.2)
ax.scatter(1,1,1,color=RD,s=30); txt(ax,(2.05,3.05,4.1),"$r'(1)$",RD)
lim(ax,(0,2.2),(0,3.6),(0,6)); save(fig,'b13-2-tangen.png')

# TNB heliks
fig,ax=ax3(elev=22,azim=-55); t=np.linspace(0,3*np.pi,300)
ax.plot(np.cos(t),np.sin(t),t/2,color=GY,lw=1.6)
t0=np.pi/2; P=np.array([np.cos(t0),np.sin(t0),t0/2])
T_=np.array([-np.sin(t0),np.cos(t0),0.5]);T_/=np.linalg.norm(T_)
N_=np.array([-np.cos(t0),-np.sin(t0),0])
B_=np.cross(T_,N_)
for v,c,l in [(T_,RD,'$T$'),(N_,GR,'$N$'),(B_,OR,'$B$')]:
    arrow(ax,P,P+0.9*v,c,2.2); txt(ax,P+1.0*v,l,c)
ax.scatter(*P,color='k',s=25); lim(ax,(-1.5,1.5),(-1.5,1.5),(0,5)); save(fig,'b13-3-tnb.png')

# lingkaran oskulasi parabola
fig,ax=plt.subplots(figsize=(5.4,4.4)); x=np.linspace(-1.6,1.6,300)
ax.plot(x,x**2,color=BL,lw=2,label='$y=x^2$')
th=np.linspace(0,2*np.pi,300); ax.plot(0.5*np.cos(th),0.5+0.5*np.sin(th),color=RD,lw=1.6,label='lingkaran oskulasi di $(0,0)$, $r=1/2$')
ax.plot(0,0,'ko'); ax.set_aspect('equal'); ax.set_xlim(-1.6,1.6); ax.set_ylim(-0.3,2.6)
ax.grid(alpha=.3); ax.legend(fontsize=8,loc='upper center'); save(fig,'b13-3-oskulasi.png')

# proyektil
fig,ax=plt.subplots(figsize=(6,3.4)); a=np.radians(40);v=30;g=9.8
tt=np.linspace(0,2*v*np.sin(a)/g,200)
ax.plot(v*np.cos(a)*tt,v*np.sin(a)*tt-0.5*g*tt**2,color=BL,lw=2)
for k in range(0,4):
    t_=k; ax.plot(v*np.cos(a)*t_,v*np.sin(a)*t_-0.5*g*t_**2,'o',color=RD)
ax.set_xlabel('$x$ (m)'); ax.set_ylabel('$y$ (m)'); ax.grid(alpha=.3); ax.set_aspect('equal'); save(fig,'b13-4-proyektil.png')
print('ok')
