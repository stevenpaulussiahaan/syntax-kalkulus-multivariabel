import sys; sys.path.insert(0,'/tmp/kalkulus/python')
from figs_b12 import *
import numpy as np
from matplotlib.patches import Polygon, FancyArrowPatch
def save(fig,n): fig.savefig(OUT+n,dpi=130,bbox_inches='tight'); plt.close(fig)
def field(ax,F,r=2,n=11,title=''):
    x=np.linspace(-r,r,n); X,Y=np.meshgrid(x,x); U,V=F(X,Y); M=np.hypot(U,V); M[M==0]=1
    ax.quiver(X,Y,U/M*0.35,V/M*0.35,M,angles='xy',scale_units='xy',scale=1,cmap='Blues',width=.006,headwidth=4)
    ax.set_aspect('equal'); ax.set_title(title); ax.set_xlim(-r-.3,r+.3); ax.set_ylim(-r-.3,r+.3); ax.grid(alpha=.3)
fig,ax=plt.subplots(1,3,figsize=(11.5,3.8))
field(ax[0],lambda x,y:(-y,x),title='$\\mathbf{F}=\\langle-y,x\\rangle$ (putaran)')
field(ax[1],lambda x,y:(x,y),title='$\\mathbf{F}=\\langle x,y\\rangle$ (memancar)')
field(ax[2],lambda x,y:(y*0+1,np.sin(x)),title='$\\mathbf{F}=\\langle1,\\sin x\\rangle$')
save(fig,'b16-1-medan.png')
# gradien + kontur
fig,ax=plt.subplots(figsize=(5.2,4.6)); x=np.linspace(-2,2,200); X,Y=np.meshgrid(x,x)
ax.contour(X,Y,X**2-Y**2,levels=np.arange(-4,5,1),colors=GY,linewidths=.8)
xs=np.linspace(-2,2,9); Xs,Ys=np.meshgrid(xs,xs); ax.quiver(Xs,Ys,2*Xs,-2*Ys,color=BL,angles='xy',scale=40,width=.004)
ax.set_aspect('equal'); ax.set_title('Medan gradien $\\nabla f$, $f=x^2-y^2$'); save(fig,'b16-1-gradien.png')
# dua lintasan
fig,ax=plt.subplots(figsize=(5.2,4.6)); t=np.linspace(0,1,100)
ax.plot(t,t**2,color=BL,lw=2.2,label='$C_1$: $y=x^2$'); ax.plot(t,t,color=RD,lw=2.2,label='$C_2$: $y=x$')
x=np.linspace(-.2,1.2,12); X,Y=np.meshgrid(x,x); ax.quiver(X,Y,-Y,X,color=GY,angles='xy',scale=14,width=.004)
ax.plot([0,1],[0,1],'ko'); ax.set_aspect('equal'); ax.legend(); ax.set_xlim(-.2,1.2); ax.set_ylim(-.2,1.2); ax.grid(alpha=.3); save(fig,'b16-2-lintasan.png')
# Green
fig,(a,b)=plt.subplots(1,2,figsize=(9,3.8)); th=np.linspace(0,2*np.pi,200)
a.fill(2*np.cos(th),1.3*np.sin(th),color=BL,alpha=.25); a.plot(2*np.cos(th),1.3*np.sin(th),color=BL,lw=2)
a.annotate('',(0,1.3),(-.4,1.29),arrowprops=dict(arrowstyle='->',color=RD,lw=2)); a.annotate('',(0.4,-1.29),(0,-1.3),arrowprops=dict(arrowstyle='<-',color=RD,lw=2)); a.text(0,0,'$D$',ha='center',fontsize=14)
a.set_title('Orientasi positif: $D$ di sebelah kiri'); a.set_aspect('equal')
R=np.array([[0,0],[1,0],[0,1]]); b.fill(*zip(*R),color=BL,alpha=.25); b.plot(*zip(*np.vstack([R,R[0]])),color=BL,lw=2); b.set_title('Segitiga $(0,0),(1,0),(0,1)$'); b.set_aspect('equal')
for q in (a,b): q.grid(alpha=.3)
save(fig,'b16-4-green.png')
# curl/divergensi intuisi
fig,ax=plt.subplots(1,3,figsize=(11.5,3.8))
field(ax[0],lambda x,y:(-y,x),title='curl $>0$ (berputar berlawanan arah jarum jam)')
field(ax[1],lambda x,y:(y,0*x),title='geseran $\\langle y,0\\rangle$: curl $\\neq0$, div $=0$')
field(ax[2],lambda x,y:(-x,-y),title='$\\langle-x,-y\\rangle$: div $<0$ (menyerap)')
for a in ax: a.title.set_fontsize(9)
save(fig,'b16-5-curl.png')
# permukaan parametrik: bola, torus, helikoid
fig=plt.figure(figsize=(11.5,3.8),facecolor='white')
def sub(i):
    a=fig.add_subplot(1,3,i,projection='3d'); a.view_init(22,-58)
    for q in (a.xaxis,a.yaxis,a.zaxis): q.pane.set_facecolor((1,1,1,0)); q.pane.set_edgecolor('#cccccc')
    return a
u,v=np.meshgrid(np.linspace(0,np.pi,30),np.linspace(0,2*np.pi,50))
a=sub(1); a.plot_surface(np.sin(u)*np.cos(v),np.sin(u)*np.sin(v),np.cos(u),cmap='Blues',linewidth=0); a.set_title('Bola'); a.set_box_aspect((1,1,1))
u,v=np.meshgrid(np.linspace(0,2*np.pi,50),np.linspace(0,2*np.pi,30))
a=sub(2); a.plot_surface((3+np.cos(v))*np.cos(u),(3+np.cos(v))*np.sin(u),np.sin(v),cmap='Oranges',linewidth=0); a.set_title('Torus'); a.set_box_aspect((1,1,.35)); a.set_zlim(-3,3)
u,v=np.meshgrid(np.linspace(0,1,15),np.linspace(0,4*np.pi,80))
a=sub(3); a.plot_surface(u*np.cos(v),u*np.sin(v),v/3,cmap='Greens',linewidth=0); a.set_title('Helikoid'); a.set_box_aspect((1,1,1.2))
save(fig,'b16-6-permukaan.png')
# Stokes: paraboloid + circle
fig,ax=ax3(elev=22,azim=-55); r=np.linspace(0,1,20); t=np.linspace(0,2*np.pi,60); R,T=np.meshgrid(r,t)
ax.plot_surface(R*np.cos(T),R*np.sin(T),1-R**2,color=BL,alpha=.45,linewidth=0)
ax.plot(np.cos(t),np.sin(t),0*t,color=RD,lw=2.5); arrow(ax,(1,0,0),(1,.5,0),RD,2)
for (x,y) in [(0,0),(.5,.4),(-.5,.4),(.4,-.5)]:
    z=1-x*x-y*y; n=np.array([2.*x,2.*y,1.]); n/=np.linalg.norm(n); arrow(ax,(x,y,z),(x+.5*n[0],y+.5*n[1],z+.5*n[2]),GR,1.8)
lim(ax,(-1.2,1.2),(-1.2,1.2),(0,1.8)); save(fig,'b16-8-stokes.png')
# divergensi: silinder tertutup
fig,ax=ax3(elev=22,azim=-55); t=np.linspace(0,2*np.pi,60); z=np.linspace(0,2,2); T,Z=np.meshgrid(t,z)
ax.plot_surface(np.cos(T),np.sin(T),Z,color=BL,alpha=.25,linewidth=0)
for zz in (0,2):
    rr=np.linspace(0,1,2); R,T2=np.meshgrid(rr,t); ax.plot_surface(R*np.cos(T2),R*np.sin(T2),zz+0*R,color=OR,alpha=.35,linewidth=0)
for a_ in np.linspace(0,2*np.pi,8,endpoint=False): arrow(ax,(np.cos(a_),np.sin(a_),1),(1.5*np.cos(a_),1.5*np.sin(a_),1),RD,1.8)
arrow(ax,(0,0,2),(0,0,2.6),RD,2); arrow(ax,(0,0,0),(0,0,-.6),RD,2)
lim(ax,(-1.6,1.6),(-1.6,1.6),(-.7,2.7)); save(fig,'b16-9-diverg.png')
print('ok')
