import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT = '/tmp/kalkulus/assets/img/'
BL, RD, GR, OR, GY = '#1f5fa8', '#c0392b', '#1e8449', '#d68910', '#7f8c8d'

def ax3(figsize=(5.6, 5.0), elev=22, azim=-58):
    fig = plt.figure(figsize=figsize, facecolor='white')
    ax = fig.add_subplot(111, projection='3d', facecolor='white')
    ax.view_init(elev=elev, azim=azim)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor('#cccccc')
    ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel('$z$')
    return fig, ax

def lim(ax, x, y, z):
    ax.set_xlim(*x); ax.set_ylim(*y); ax.set_zlim(*z)
    try: ax.set_box_aspect((x[1]-x[0], y[1]-y[0], z[1]-z[0]))
    except Exception: pass

def arrow(ax, p, q, c='k', lw=2, **kw):
    p = np.array(p, float); q = np.array(q, float); d = q - p
    ax.quiver(*p, *d, color=c, linewidth=lw, arrow_length_ratio=0.12, **kw)

def txt(ax, p, s, c='k', fs=11):
    ax.text(p[0], p[1], p[2], s, color=c, fontsize=fs)

def save(fig, name):
    fig.savefig(OUT + name, dpi=130, facecolor='white', bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

def poly(ax, pts, c, alpha=0.25, ec=None):
    pc = Poly3DCollection([pts], alpha=alpha, facecolor=c, edgecolor=ec or c, linewidth=1)
    ax.add_collection3d(pc)

# ---------- 12.1
def f_titik():
    fig, ax = ax3()
    P = np.array([2, 3, 4])
    x, y, z = P
    for a, b in [((0,0,0),(x,0,0)),((x,0,0),(x,y,0)),((x,y,0),(x,y,z)),((0,0,0),(0,y,0)),((0,y,0),(x,y,0)),
                 ((0,0,0),(0,0,z)),((0,0,z),(x,0,z)),((x,0,z),(x,y,z)),((0,y,0),(0,y,z)),((0,y,z),(x,y,z)),((0,0,z),(0,y,z)),((x,0,0),(x,0,z))]:
        ax.plot(*zip(a, b), color=GY, ls='--', lw=1)
    ax.plot([0, x], [0, y], [0, z], color=RD, lw=2)
    ax.scatter(*P, color=RD, s=45)
    txt(ax, (x+.1, y, z+.2), '$P(2,3,4)$', RD)
    txt(ax, (x, y, -.5), '$(2,3,0)$', GY, 9)
    txt(ax, (x+.1, -.2, 0), '$(2,0,0)$', GY, 9)
    txt(ax, (-.2, y+.3, 0), '$(0,3,0)$', GY, 9)
    txt(ax, (-.7, -.2, z), '$(0,0,4)$', GY, 9)
    lim(ax, (0, 4), (0, 5), (0, 5.5))
    ax.set_xticks([0,1,2,3,4]); ax.set_yticks(range(0,6)); ax.set_zticks(range(0,6))
    save(fig, 'b12-1-titik.png')

def f_bola():
    fig, ax = ax3(elev=20, azim=-55)
    c = np.array([2, -1, 3]); r = 4
    u, v = np.meshgrid(np.linspace(0, 2*np.pi, 41), np.linspace(0, np.pi, 21))
    X = c[0]+r*np.cos(u)*np.sin(v); Y = c[1]+r*np.sin(u)*np.sin(v); Z = c[2]+r*np.cos(v)
    ax.plot_surface(X, Y, Z, color=BL, alpha=0.18, linewidth=0.3, edgecolor='#7aa5d6')
    ax.scatter(*c, color=RD, s=40)
    t = np.linspace(0, 2*np.pi, 100)
    ax.plot(c[0]+r*np.cos(t), c[1]+r*np.sin(t), c[2]+0*t, color=RD, lw=1.6)
    ax.plot([c[0], c[0]+r], [c[1], c[1]], [c[2], c[2]], color=OR, lw=2)
    txt(ax, (c[0]+.2, c[1], c[2]+.4), '$C(2,-1,3)$', RD)
    txt(ax, (c[0]+r/2-.4, c[1], c[2]-.9), '$r=4$', OR)
    lim(ax, (-3, 7), (-6, 6), (-2, 8))
    save(fig, 'b12-1-bola.png')

# ---------- 12.2
def f_jumlah():
    fig, ax = ax3(elev=24, azim=-62)
    a = np.array([3, 0, 0.0]); b = np.array([1, 2.5, 1.5]); o = np.zeros(3)
    arrow(ax, o, a, BL); arrow(ax, o, b, GR); arrow(ax, o, a+b, RD, 2.5)
    ax.plot(*zip(a, a+b), color=GR, ls='--', lw=1.2); ax.plot(*zip(b, a+b), color=BL, ls='--', lw=1.2)
    poly(ax, [o, a, a+b, b], OR, 0.18)
    txt(ax, a*0.55+[0, -.1, -.5], r'$\mathbf{a}$', BL, 13)
    txt(ax, b*0.55+[-.3, 0, .2], r'$\mathbf{b}$', GR, 13)
    txt(ax, (a+b)*0.6+[.2, 0, .3], r'$\mathbf{a}+\mathbf{b}$', RD, 13)
    lim(ax, (0, 4.5), (0, 3.5), (0, 2.5))
    save(fig, 'b12-2-jumlah.png')

def f_posisi():
    fig, ax = ax3(elev=22, azim=-60)
    A = np.array([2, 1, 1.0]); B = np.array([4, 4, 3.0]); o = np.zeros(3)
    arrow(ax, o, A, GY, 1.6); arrow(ax, o, B, GY, 1.6); arrow(ax, A, B, RD, 2.8)
    ax.scatter(*A, color=BL, s=35); ax.scatter(*B, color=BL, s=35)
    txt(ax, A+[.1, 0, -.5], '$A$', BL, 12); txt(ax, B+[.1, 0, .2], '$B$', BL, 12)
    txt(ax, (A+B)/2+[.3, 0, 0], r'$\overrightarrow{AB}=\mathbf{b}-\mathbf{a}$', RD, 11)
    txt(ax, A*0.5+[0, .2, .3], r'$\mathbf{a}$', GY, 12); txt(ax, B*0.45+[.3, -.2, .2], r'$\mathbf{b}$', GY, 12)
    lim(ax, (0, 5), (0, 5), (0, 4))
    save(fig, 'b12-2-posisi.png')

# ---------- 12.3
def f_proyeksi():
    fig = plt.figure(figsize=(5.6, 3.6), facecolor='white'); ax = fig.add_subplot(111)
    b = np.array([4.0, 1.0]); a = np.array([2.5, 2.8])
    p = a.dot(b)/b.dot(b)*b
    ax.annotate('', xy=b, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=GR, lw=2))
    ax.annotate('', xy=a, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=BL, lw=2))
    ax.annotate('', xy=p, xytext=(0, 0), arrowprops=dict(arrowstyle='->', color=RD, lw=3))
    ax.plot([a[0], p[0]], [a[1], p[1]], color=GY, ls='--')
    s = 0.18; u = b/np.linalg.norm(b); w = np.array([-u[1], u[0]])
    ax.plot(*zip(p-s*u, p-s*u+s*w, p+s*w), color=GY, lw=1)
    ax.text(*(a+[-.1, .15]), r'$\mathbf{a}$', color=BL, fontsize=14)
    ax.text(*(b+[.1, 0]), r'$\mathbf{b}$', color=GR, fontsize=14)
    ax.text(*(p*0.5+[0.1, -.4]), r'$\mathrm{proj}_{\mathbf{b}}\mathbf{a}$', color=RD, fontsize=12)
    ax.text(*(0.55*a+0.45*p+[.15, 0]), r'$\mathbf{a}-\mathrm{proj}_{\mathbf{b}}\mathbf{a}$', color=GY, fontsize=10)
    ax.text(0.7, 0.12, r'$\theta$', fontsize=12)
    ax.set_xlim(-0.3, 5); ax.set_ylim(-0.6, 3.5); ax.set_aspect('equal'); ax.axis('off')
    save(fig, 'b12-3-proyeksi.png')

def f_bidangmiring():
    fig = plt.figure(figsize=(5.6, 3.4), facecolor='white'); ax = fig.add_subplot(111)
    th = np.radians(25); L = 6
    ax.plot([0, L*np.cos(th), L*np.cos(th), 0], [0, L*np.sin(th), 0, 0], color='k')
    c = np.array([3.4*np.cos(th), 3.4*np.sin(th)])
    n = np.array([-np.sin(th), np.cos(th)]); t = np.array([np.cos(th), np.sin(th)])
    c = c + 0.25*n
    ax.annotate('', xy=c+[0, -2.2], xytext=c, arrowprops=dict(arrowstyle='->', color=RD, lw=2.5))
    ax.annotate('', xy=c-2.2*np.cos(th)*n*0+[0, 0]-np.array([0, 0]), xytext=c, arrowprops=dict(arrowstyle='-', color='none'))
    w = 2.2
    ax.annotate('', xy=c-w*np.sin(th)*t*(-1)*0 - w*np.sin(th)*t, xytext=c, arrowprops=dict(arrowstyle='->', color=OR, lw=2))
    ax.annotate('', xy=c-w*np.cos(th)*n, xytext=c, arrowprops=dict(arrowstyle='->', color=GR, lw=2))
    ax.text(c[0]+.15, c[1]-2.1, r'$\mathbf{W}$', color=RD, fontsize=13)
    ax.text(c[0]-w*np.sin(th)*np.cos(th)-1.0, c[1]-w*np.sin(th)*np.sin(th)+.05, r'sejajar bidang', color=OR, fontsize=10)
    ax.text(c[0]-w*np.cos(th)*n[0]+.1, c[1]-w*np.cos(th)*n[1]-.1, r'tegak lurus', color=GR, fontsize=10)
    ax.text(4.3, 0.18, r'$25^\circ$', fontsize=12)
    ax.set_xlim(-0.3, 6.6); ax.set_ylim(-0.5, 3.6); ax.set_aspect('equal'); ax.axis('off')
    save(fig, 'b12-3-bidangmiring.png')

# ---------- 12.4
def f_silang():
    fig, ax = ax3(elev=22, azim=-55)
    a = np.array([3, 0, 0.0]); b = np.array([1, 2.5, 0.0]); c = np.cross(a, b); c = c/np.linalg.norm(c)*3
    o = np.zeros(3)
    poly(ax, [o, a, a+b, b], OR, 0.25)
    arrow(ax, o, a, BL); arrow(ax, o, b, GR); arrow(ax, o, c, RD, 2.5)
    txt(ax, a*.6+[0, -.2, -.3], r'$\mathbf{a}$', BL, 13); txt(ax, b*.6+[-.4, 0, 0], r'$\mathbf{b}$', GR, 13)
    txt(ax, c+[.1, 0, .1], r'$\mathbf{a}\times\mathbf{b}$', RD, 13)
    txt(ax, (a+b)*.55, 'luas', OR, 10)
    lim(ax, (0, 4.5), (0, 3.5), (0, 3.5))
    save(fig, 'b12-4-silang.png')

def f_paralel():
    fig, ax = ax3(elev=20, azim=-62)
    a = np.array([3, 0, 0.0]); b = np.array([1, 2.5, 0.0]); c = np.array([0.8, 0.8, 2.2]); o = np.zeros(3)
    faces = [[o, a, a+b, b], [c, c+a, c+a+b, c+b], [o, a, a+c, c], [b, a+b, a+b+c, b+c], [o, b, b+c, c], [a, a+b, a+b+c, a+c]]
    for f in faces: poly(ax, f, BL, 0.12, '#5b7fa8')
    arrow(ax, o, a, BL, 2.2); arrow(ax, o, b, GR, 2.2); arrow(ax, o, c, RD, 2.2)
    txt(ax, a*.6+[0, -.2, -.3], r'$\mathbf{a}$', BL, 13); txt(ax, b*.6+[-.4, 0, 0], r'$\mathbf{b}$', GR, 13)
    txt(ax, c*.6+[-.5, 0, 0], r'$\mathbf{c}$', RD, 13)
    lim(ax, (0, 5), (0, 3.5), (0, 3))
    save(fig, 'b12-4-paralelepipedum.png')

# ---------- 12.5
def f_garis():
    fig, ax = ax3(elev=22, azim=-60)
    P0 = np.array([1, 1, 0.5]); d = np.array([1, 0.8, 0.9])
    t = np.linspace(-1.2, 2.6, 2)
    L = np.array([P0 + s*d for s in t])
    ax.plot(L[:, 0], L[:, 1], L[:, 2], color=BL, lw=2.2)
    o = np.zeros(3)
    arrow(ax, o, P0, GY, 1.5); arrow(ax, P0, P0+d, RD, 2.5)
    P = P0 + 1.8*d
    arrow(ax, o, P, GR, 1.5)
    ax.plot(*zip(P0, P), color=OR, lw=3)
    ax.scatter(*P0, color=BL, s=30); ax.scatter(*P, color=BL, s=30)
    txt(ax, P0+[.1, 0, -.4], r'$P_0$', BL, 12); txt(ax, P+[.1, 0, .1], r'$P(x,y,z)$', BL, 11)
    txt(ax, P0*.45+[.1, .2, .1], r'$\mathbf{r}_0$', GY, 12); txt(ax, P*.5+[.3, -.3, 0], r'$\mathbf{r}$', GR, 12)
    txt(ax, P0+d*.4+[-.1, .4, 0], r'$\mathbf{v}$', RD, 12)
    lim(ax, (0, 4), (0, 3.5), (0, 3.2))
    save(fig, 'b12-5-garis.png')

def f_bidang():
    fig, ax = ax3(elev=22, azim=-58)
    n = np.array([1.0, 1.5, 2.0]); P0 = np.array([2, 1.5, 1.5])
    e1 = np.cross(n, [0, 0, 1]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1); e2 /= np.linalg.norm(e2)
    s = 2.2
    pts = [P0+s*(i*e1+j*e2) for i, j in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    poly(ax, pts, BL, 0.22)
    nn = n/np.linalg.norm(n)*2.2
    arrow(ax, P0, P0+nn, RD, 2.6)
    Q = P0 + 1.0*e1 + 0.7*e2
    ax.plot(*zip(P0, Q), color=GR, lw=2.2)
    ax.scatter(*P0, color=BL, s=35); ax.scatter(*Q, color=GR, s=35)
    txt(ax, P0+[.15, 0, -.5], r'$P_0$', BL, 12); txt(ax, Q+[.15, 0, .15], r'$P(x,y,z)$', GR, 11)
    txt(ax, P0+nn+[.1, 0, .1], r'$\mathbf{n}$', RD, 13)
    txt(ax, (P0+Q)/2+[0, .1, -.55], r'$\mathbf{r}-\mathbf{r}_0$', GR, 11)
    lim(ax, (0, 4.5), (0, 4), (0, 4.5))
    save(fig, 'b12-5-bidang.png')

def f_skew():
    fig, ax = ax3(elev=20, azim=-50)
    P1 = np.array([0, 0, 0.0]); d1 = np.array([1, 0.2, 0.0])
    P2 = np.array([1.0, -1.5, 2.0]); d2 = np.array([0.2, 1, 0.0])
    s1, s2 = 1.2, 1.0
    for P, d, c in [(P1, d1, BL), (P2, d2, GR)]:
        pts = np.array([P-2.2*d, P+2.4*d]); ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=c, lw=2.4)
    # closest points
    A = np.array([[d1@d1, -d1@d2], [d1@d2, -d2@d2]]); b = np.array([(P2-P1)@d1, (P2-P1)@d2])
    t, s = np.linalg.solve(A, b)
    Q1 = P1+t*d1; Q2 = P2+s*d2
    ax.plot(*zip(Q1, Q2), color=RD, lw=2.5, ls='-')
    ax.scatter(*Q1, color=RD, s=25); ax.scatter(*Q2, color=RD, s=25)
    txt(ax, P1-2.0*d1+[0, 0, .3], r'$L_1$', BL, 13); txt(ax, P2+2.0*d2+[0, 0, .3], r'$L_2$', GR, 13)
    txt(ax, (Q1+Q2)/2+[.15, 0, 0], 'jarak', RD, 11)
    lim(ax, (-2.5, 3.2), (-2.2, 3.0), (0, 2.5))
    save(fig, 'b12-5-skew.png')

# ---------- 12.6
def surf(ax, X, Y, Z, c=BL, alpha=0.35):
    ax.plot_surface(X, Y, Z, color=c, alpha=alpha, linewidth=0.25, edgecolor='#6d93c4', rstride=1, cstride=1)

def f_silinder():
    fig = plt.figure(figsize=(11, 3.8), facecolor='white')
    t = np.linspace(0, 2*np.pi, 60)
    ax = fig.add_subplot(131, projection='3d', facecolor='white'); ax.view_init(22, -55)
    x = np.linspace(-2, 2, 30); z = np.linspace(-2, 4, 12); X, Z = np.meshgrid(x, z); surf(ax, X, X**2, Z)
    ax.set_title(r'$y=x^2$', fontsize=11); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel('$z$')
    ax = fig.add_subplot(132, projection='3d', facecolor='white'); ax.view_init(22, -55)
    T, Y = np.meshgrid(t, np.linspace(-3, 3, 10)); surf(ax, 2*np.cos(T), Y, 2*np.sin(T), GR)
    ax.set_title(r'$x^2+z^2=4$', fontsize=11); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel('$z$')
    ax = fig.add_subplot(133, projection='3d', facecolor='white'); ax.view_init(22, -55)
    T, Z = np.meshgrid(t, np.linspace(-2, 2, 10)); surf(ax, 3*np.cos(T), 2*np.sin(T), Z, OR)
    ax.set_title(r'$\frac{x^2}{9}+\frac{y^2}{4}=1$', fontsize=11); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel('$z$')
    fig.subplots_adjust(wspace=0.05)
    save(fig, 'b12-6-silinder.png')

def traces(ax, fn, ranges):
    pass

def f_elipsoid():
    fig, ax = ax3(elev=20, azim=-55)
    u, v = np.meshgrid(np.linspace(0, 2*np.pi, 49), np.linspace(0, np.pi, 25))
    a, b, c = 3, 2, 1.5
    surf(ax, a*np.cos(u)*np.sin(v), b*np.sin(u)*np.sin(v), c*np.cos(v), BL, 0.25)
    t = np.linspace(0, 2*np.pi, 100)
    ax.plot(a*np.cos(t), b*np.sin(t), 0*t, color=RD, lw=2)
    ax.plot(a*np.cos(t), 0*t, c*np.sin(t), color=GR, lw=2)
    ax.plot(0*t, b*np.cos(t), c*np.sin(t), color=OR, lw=2)
    lim(ax, (-3.2, 3.2), (-3.2, 3.2), (-2.5, 2.5))
    save(fig, 'b12-6-elipsoid.png')

def f_hip1():
    fig, ax = ax3(elev=18, azim=-55)
    t = np.linspace(0, 2*np.pi, 60); z = np.linspace(-1.6, 1.6, 40); T, Z = np.meshgrid(t, z)
    R = np.sqrt(1+Z**2)
    surf(ax, 3*R*np.cos(T), 2*R*np.sin(T), Z, BL, 0.3)
    ax.plot(3*np.cos(t), 2*np.sin(t), 0*t, color=RD, lw=2)
    zz = np.linspace(-1.6, 1.6, 60)
    ax.plot(3*np.sqrt(1+zz**2), 0*zz, zz, color=GR, lw=2); ax.plot(-3*np.sqrt(1+zz**2), 0*zz, zz, color=GR, lw=2)
    ax.plot(0*zz, 2*np.sqrt(1+zz**2), zz, color=OR, lw=2); ax.plot(0*zz, -2*np.sqrt(1+zz**2), zz, color=OR, lw=2)
    lim(ax, (-7, 7), (-5, 5), (-1.6, 1.6))
    save(fig, 'b12-6-hiperboloid1.png')

def f_hip2():
    fig, ax = ax3(elev=16, azim=-55)
    t = np.linspace(0, 2*np.pi, 60); z = np.linspace(1, 2.4, 25); T, Z = np.meshgrid(t, z)
    R = np.sqrt(Z**2-1)
    for sg in (1, -1):
        surf(ax, 3*R*np.cos(T), 2*R*np.sin(T), sg*Z, BL if sg > 0 else GR, 0.3)
    zz = np.linspace(1, 2.4, 50)
    for sg in (1, -1):
        ax.plot(3*np.sqrt(zz**2-1), 0*zz, sg*zz, color=RD, lw=2); ax.plot(-3*np.sqrt(zz**2-1), 0*zz, sg*zz, color=RD, lw=2)
    ax.plot([0, 0], [0, 0], [-1, -1], 'o', color='k'); ax.plot([0], [0], [1], 'o', color='k')
    lim(ax, (-6, 6), (-4, 4), (-2.4, 2.4))
    save(fig, 'b12-6-hiperboloid2.png')

def f_parab_e():
    fig, ax = ax3(elev=20, azim=-55)
    r = np.linspace(0, 1, 25); t = np.linspace(0, 2*np.pi, 60); R, T = np.meshgrid(r, t)
    X = 2*2*R*np.cos(T); Y = 3*2*R*np.sin(T)
    Z = X**2/4+Y**2/9
    surf(ax, X, Y, Z, BL, 0.3)
    s = np.linspace(-4, 4, 80)
    ax.plot(s, 0*s, s**2/4, color=GR, lw=2); ax.plot(0*s, 1.5*s, (1.5*s)**2/9, color=OR, lw=2)
    ax.plot(4*np.cos(np.linspace(0, 2*np.pi, 100)), 6*np.sin(np.linspace(0, 2*np.pi, 100)), 4+0*np.linspace(0, 2*np.pi, 100), color=RD, lw=2)
    lim(ax, (-4, 4), (-6, 6), (0, 4.2))
    save(fig, 'b12-6-paraboloid-eliptik.png')

def f_parab_h():
    fig, ax = ax3(elev=22, azim=-60)
    x = np.linspace(-2, 2, 40); y = np.linspace(-2, 2, 40); X, Y = np.meshgrid(x, y)
    Z = Y**2/4*1.0 - X**2/1.0*0.5
    Z = Y**2 - X**2
    surf(ax, X, Y, Z, BL, 0.35)
    s = np.linspace(-2, 2, 60)
    ax.plot(s, 0*s, -s**2, color=GR, lw=2.2); ax.plot(0*s, s, s**2, color=OR, lw=2.2)
    ax.scatter([0], [0], [0], color='k', s=25)
    lim(ax, (-2, 2), (-2, 2), (-4, 4))
    save(fig, 'b12-6-paraboloid-hiperbolik.png')

def f_kerucut():
    fig, ax = ax3(elev=18, azim=-55)
    t = np.linspace(0, 2*np.pi, 60); z = np.linspace(-2, 2, 30); T, Z = np.meshgrid(t, z)
    surf(ax, 2*Z*np.cos(T), 3*Z*np.sin(T), Z, BL, 0.3)
    ax.plot(2*2*np.cos(t), 3*2*np.sin(t), 2+0*t, color=RD, lw=2)
    s = np.linspace(-2, 2, 20)
    ax.plot(0*s, 3*s, s, color=OR, lw=2.2); ax.plot(0*s, -3*s, s, color=OR, lw=2.2)
    ax.scatter([0], [0], [0], color='k', s=25)
    lim(ax, (-4.5, 4.5), (-6.5, 6.5), (-2, 2))
    save(fig, 'b12-6-kerucut.png')

def f_irisan():
    fig, ax = ax3(elev=20, azim=-60)
    t = np.linspace(0, 2*np.pi, 60); z = np.linspace(-1, 3, 30); T, Z = np.meshgrid(t, z)
    surf(ax, Z*np.cos(T), Z*np.sin(T), Z, BL, 0.2)
    xs = np.linspace(-2.2, 2.2, 80); ys = (xs**2-1)/2; zs = ys+1
    ax.plot(xs, ys, zs, color=RD, lw=2.5)
    Y, X = np.meshgrid(np.linspace(-1, 3, 5), np.linspace(-3, 3, 5)); 
    ax.plot_surface(X, Y, Y+1, color=OR, alpha=0.12)
    lim(ax, (-3, 3), (-1, 3), (-1, 3))
    save(fig, 'b12-6-irisan.png')

if __name__ == '__main__':
    for f in [f_titik, f_bola, f_jumlah, f_posisi, f_proyeksi, f_bidangmiring, f_silang, f_paralel, f_garis, f_bidang, f_skew,
              f_silinder, f_elipsoid, f_hip1, f_hip2, f_parab_e, f_parab_h, f_kerucut, f_irisan]:
        f()
    print('ok')
