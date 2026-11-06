import sys; sys.path.insert(0,'/tmp/kalkulus/python')
from figs_b12 import *
import numpy as np
def save(fig,n): fig.savefig(OUT+n,dpi=130,bbox_inches='tight'); plt.close(fig)
def grid(r,n=60):
    u=np.linspace(-r,r,n); return np.meshgrid(u,u)

# grafik z=4-x^2-y^2
fig,ax=ax3(elev=25,azim=-60); X,Y=grid(2); Z=4-X**2-Y**2; Z=np.where(Z>=0,Z,np.nan)
ax.plot_surface(X,Y,Z,cmap='Blues',alpha=.9,linewidth=0); lim(ax,(-2,2),(-2,2),(0,4)); save(fig,'b14-1-grafik.png')

# kontur z=x^2+y^2 dan pelana
fig,(a,b)=plt.subplots(1,2,figsize=(9,4)); X,Y=grid(2,200)
c=a.contour(X,Y,X**2+Y**2,levels=[0.25,1,2.25,4],colors=BL); a.clabel(c,fmt='%g'); a.set_title('$z=x^2+y^2$'); a.set_aspect('equal')
c=b.contour(X,Y,X**2-Y**2,levels=[-3,-2,-1,0,1,2,3],colors=BL); b.clabel(c,fmt='%g'); b.set_title('$z=x^2-y^2$'); b.set_aspect('equal')
for q in (a,b): q.set_xlabel('$x$'); q.set_ylabel('$y$')
save(fig,'b14-1-kontur.png')

# limit xy/(x^2+y^2)
fig,ax=ax3(elev=25,azim=-60); X,Y=grid(2,80); R=X**2+Y**2; Z=np.where(R>1e-6,X*Y/np.where(R>1e-6,R,1),np.nan)
ax.plot_surface(X,Y,Z,cmap='coolwarm',linewidth=0,alpha=.95); lim(ax,(-2,2),(-2,2),(-.6,.6)); save(fig,'b14-2-xy.png')

# turunan parsial: z=4-x^2-2y^2 irisan di (1,1)
fig,ax=ax3(elev=25,azim=-55); X,Y=grid(2); Z=4-X**2-2*Y**2
ax.plot_surface(X,Y,Z,color=BL,alpha=.3,linewidth=0)
u=np.linspace(-2,2,100); ax.plot(u,np.ones_like(u),4-u**2-2,color=RD,lw=2.2); ax.plot(np.ones_like(u),u,4-1-2*u**2,color=GR,lw=2.2)
ax.scatter(1,1,1,color='k',s=30)
s=np.linspace(-.8,.8,2); ax.plot(1+s,1+0*s,1-2*s,color=RD,ls='--'); ax.plot(1+0*s,1+s,1-4*s,color=GR,ls='--')
lim(ax,(-2,2),(-2,2),(-5,4)); save(fig,'b14-3-parsial.png')

# bidang singgung z=x^2+y^2 at (1,1,2): z=2x+2y-2
fig,ax=ax3(elev=22,azim=-55); X,Y=grid(2,50); ax.plot_surface(X,Y,X**2+Y**2,color=BL,alpha=.35,linewidth=0)
U,V=np.meshgrid(np.linspace(0,2,10),np.linspace(0,2,10)); ax.plot_surface(U,V,2*U+2*V-2,color=OR,alpha=.55,linewidth=0)
ax.scatter(1,1,2,color='k',s=30); lim(ax,(-2,2),(-2,2),(0,8)); save(fig,'b14-4-bidang.png')

# gradien pada kontur f=x^2+4y^2... f=x^2+y^2/... 
fig,ax=plt.subplots(figsize=(5.4,4.6)); X,Y=grid(3,300); F=X**2+2*Y**2
c=ax.contour(X,Y,F,levels=[1,2,4,6,9,12],colors=BL); ax.clabel(c,fmt='%g')
for (x,y) in [(1,0.5),(-1.5,1),(0.5,-1.2),(2,-.5)]:
    g=np.array([2*x,4*y]); g=g/np.linalg.norm(g)*0.8; ax.annotate('',(x+g[0],y+g[1]),(x,y),arrowprops=dict(arrowstyle='->',color=RD,lw=2)); ax.plot(x,y,'ko',ms=4)
ax.set_aspect('equal'); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_title('Gradien $\\nabla f$ tegak lurus kurva ketinggian'); save(fig,'b14-6-gradien.png')

# titik kritis f=x^3-3x+y^2?? gunakan f=x^3-3x^2... pakai f = x^3 - 12 x + y^2 -> hmm; pakai f=x^2 y... gunakan f=x^3+y^3-3xy
fig,ax=plt.subplots(figsize=(5.4,4.6)); X,Y=np.meshgrid(np.linspace(-2,2.2,300),np.linspace(-2,2.2,300)); F=X**3+Y**3-3*X*Y
c=ax.contour(X,Y,F,levels=[-1,-.5,0,0.5,2,4,8],colors=BL); ax.clabel(c,fmt='%g')
ax.plot(0,0,'o',color=RD); ax.plot(1,1,'o',color=GR); ax.text(.1,.1,'pelana',color=RD); ax.text(1.05,1.05,'min lokal',color=GR)
ax.set_aspect('equal'); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); save(fig,'b14-7-kritis.png')

# lagrange: f=x+2y ... pakai f=xy pada x^2+y^2=1? gunakan f=x^2+2y^2? pakai maksimum x+y... f=x*y on x^2+y^2=2 -> pilih f=x^2+2y^2? pakai f=x+2y on circle radius1
fig,ax=plt.subplots(figsize=(5.4,4.6)); X,Y=grid(3,300)
c=ax.contour(X,Y,X+2*Y,levels=[-2.236,-1,0,1,2,2.236],colors=GY); ax.clabel(c,fmt='%.3g')
th=np.linspace(0,2*np.pi,300); ax.plot(np.cos(th),np.sin(th),color=BL,lw=2.2)
ax.plot(1/5**.5,2/5**.5,'o',color=RD); ax.plot(-1/5**.5,-2/5**.5,'o',color=GR)
ax.annotate('',(1/5**.5+.5,2/5**.5+1.0),(1/5**.5,2/5**.5),arrowprops=dict(arrowstyle='->',color=RD,lw=1.8))
ax.set_aspect('equal'); ax.set_xlim(-2,2.5); ax.set_ylim(-2,2.5); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); save(fig,'b14-8-lagrange.png')
print('ok')
