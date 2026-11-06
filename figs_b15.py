import sys; sys.path.insert(0,'/tmp/kalkulus/python')
from figs_b12 import *
import numpy as np
from matplotlib.patches import Polygon
def save(fig,n): fig.savefig(OUT+n,dpi=130,bbox_inches='tight'); plt.close(fig)

# Riemann boxes
fig,ax=ax3(elev=28,azim=-55); f=lambda x,y:16-x*x-2*y*y
n=4;h=2/n
for i in range(n):
    for j in range(n):
        xm,ym=(i+.5)*h,(j+.5)*h; z=f(xm,ym)
        ax.bar3d(i*h,j*h,0,h,h,z,color=BL,alpha=.35,edgecolor='#1f5fa8',linewidth=.5,shade=True)
X,Y=np.meshgrid(np.linspace(0,2,30),np.linspace(0,2,30)); ax.plot_wireframe(X,Y,f(X,Y),color=RD,lw=.6,rstride=3,cstride=3)
lim(ax,(0,2),(0,2),(0,16)); save(fig,'b15-1-riemann.png')

# tipe I dan II
fig,(a,b)=plt.subplots(1,2,figsize=(9,3.8)); x=np.linspace(-1,1,200)
a.fill_between(x,2*x**2,1+x**2,color=BL,alpha=.3); a.plot(x,2*x**2,color=RD,lw=2); a.plot(x,1+x**2,color=GR,lw=2)
a.annotate('',(0.5,0.5+0.25),(0.5,0.5+.0),arrowprops=dict(arrowstyle='<->',color='k')) if False else None
a.set_title('Tipe I: $2x^2\\leq y\\leq 1+x^2$'); a.set_xlabel('$x$'); a.set_ylabel('$y$'); a.grid(alpha=.3)
y=np.linspace(0,2,200); xl=np.maximum(0,y/2); 
# daerah y=x^2..y=2x : tipe II
yy=np.linspace(0,4,300); b.fill_betweenx(yy,yy/2,np.sqrt(yy),color=BL,alpha=.3)
xx=np.linspace(0,2,100); b.plot(xx,xx**2,color=RD,lw=2,label='$y=x^2$'); b.plot(xx,2*xx,color=GR,lw=2,label='$y=2x$')
b.set_title('Tipe II: $y/2\\leq x\\leq\\sqrt{y}$, $0\\leq y\\leq4$'); b.legend(); b.set_xlabel('$x$'); b.grid(alpha=.3)
save(fig,'b15-3-tipe.png')

# kutub
fig,(a,b)=plt.subplots(1,2,figsize=(9,4),subplot_kw={}); 
th=np.linspace(np.pi/6,np.pi/2.5,60)
for r in (1,2,3): a.plot(r*np.cos(th),r*np.sin(th),color=GY,lw=.8)
for t in (np.pi/6,np.pi/2.5): a.plot([np.cos(t),3*np.cos(t)],[np.sin(t),3*np.sin(t)],color=GY,lw=.8)
r=np.linspace(1,3,2)
th2=np.linspace(np.pi/6,np.pi/2.5,60)
a.fill(np.r_[np.cos(th2),3*np.cos(th2[::-1])],np.r_[np.sin(th2),3*np.sin(th2[::-1])],color=BL,alpha=.35)
a.set_aspect('equal'); a.set_title('Persegi panjang kutub $1\\leq r\\leq3$, $\\pi/6\\leq\\theta\\leq2\\pi/5$'); a.set_xlim(0,3.3); a.set_ylim(0,3.3)
t=np.linspace(0,2*np.pi,400); rr=1+np.cos(t); b.fill(rr*np.cos(t),rr*np.sin(t),color=BL,alpha=.3); b.plot(rr*np.cos(t),rr*np.sin(t),color=RD,lw=2)
b.set_aspect('equal'); b.set_title('Kardioid $r=1+\\cos\\theta$'); 
for q in (a,b): q.grid(alpha=.3)
save(fig,'b15-4-kutub.png')

# padat antara dua paraboloid
fig,ax=ax3(elev=18,azim=-60); u=np.linspace(0,2*np.pi,60); r=np.linspace(0,1,25); U,R=np.meshgrid(u,r)
X=2*R*np.cos(U); Y=np.sqrt(2)*R*np.sin(U)
ax.plot_surface(X,Y,X**2+3*Y**2,color=BL,alpha=.55,linewidth=0); ax.plot_surface(X,Y,8-X**2-Y**2,color=OR,alpha=.45,linewidth=0)
lim(ax,(-2.2,2.2),(-1.6,1.6),(0,8.5)); save(fig,'b15-7-padat.png')

# tetrahedron
fig,ax=ax3(elev=22,azim=-50)
V=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
for tri in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]:
    ax.add_collection3d(Poly3DCollection([[V[i] for i in tri]],alpha=.3,facecolor=BL,edgecolor='k'))
lim(ax,(0,1.1),(0,1.1),(0,1.1)); save(fig,'b15-7-tetra.png')

# koordinat tabung
fig,ax=ax3(elev=22,azim=-55); r_,t_,z_=2,np.pi/3,1.5
P=np.array([r_*np.cos(t_),r_*np.sin(t_),z_]); Q=np.array([P[0],P[1],0])
arrow(ax,(0,0,0),P,RD,2); ax.plot([Q[0],P[0]],[Q[1],P[1]],[0,z_],color=GR,lw=2,ls='--')
ax.plot([0,Q[0]],[0,Q[1]],[0,0],color=BL,lw=2); th=np.linspace(0,t_,30); ax.plot(.7*np.cos(th),.7*np.sin(th),0*th,color=OR,lw=2)
txt(ax,P*1.05,'$P(r,\\theta,z)$'); txt(ax,Q*.5+np.array([.1,-.2,0]),'$r$',BL); txt(ax,(.9,.15,0),'$\\theta$',OR); txt(ax,(P[0]+.1,P[1],z_/2),'$z$',GR)
lim(ax,(0,2.5),(0,2.5),(0,2)); save(fig,'b15-8-tabung.png')

# koordinat bola
fig,ax=ax3(elev=22,azim=-55); rho,ph,tt=2.5,np.pi/4,np.pi/3
P=rho*np.array([np.sin(ph)*np.cos(tt),np.sin(ph)*np.sin(tt),np.cos(ph)]); Q=np.array([P[0],P[1],0])
arrow(ax,(0,0,0),P,RD,2); ax.plot([Q[0],P[0]],[Q[1],P[1]],[0,P[2]],color=GY,ls='--'); ax.plot([0,Q[0]],[0,Q[1]],[0,0],color=BL,lw=2)
a_=np.linspace(0,ph,30); ax.plot(.8*np.sin(a_)*np.cos(tt),.8*np.sin(a_)*np.sin(tt),.8*np.cos(a_),color=GR,lw=2)
b_=np.linspace(0,tt,30); ax.plot(.9*np.cos(b_),.9*np.sin(b_),0*b_,color=OR,lw=2)
txt(ax,P*1.05,'$P(\\rho,\\theta,\\phi)$'); txt(ax,(.3,.1,.9),'$\\phi$',GR); txt(ax,(1,.2,0),'$\\theta$',OR); txt(ax,P*.5+np.array([.1,0,.1]),'$\\rho$',RD)
lim(ax,(0,2.2),(0,2.2),(0,2.6)); save(fig,'b15-9-bola.png')

# jacobian
fig,(a,b)=plt.subplots(1,2,figsize=(8.6,3.8))
a.add_patch(Polygon([(0,0),(1,0),(1,1),(0,1)],color=BL,alpha=.35)); a.set_xlim(-.3,1.3); a.set_ylim(-.3,1.3); a.set_title('Bidang $uv$: persegi satuan'); a.set_xlabel('$u$'); a.set_ylabel('$v$')
P=[(0,0),(2,1),(3,4),(1,3)]; b.add_patch(Polygon(P,color=OR,alpha=.4)); b.set_xlim(-.5,3.5); b.set_ylim(-.5,4.5); b.set_title('Bidang $xy$: $x=2u+v,\\ y=u+3v$'); b.set_xlabel('$x$'); b.set_ylabel('$y$')
for q in (a,b): q.set_aspect('equal'); q.grid(alpha=.3)
save(fig,'b15-10-jacobian.png')
print('ok')
