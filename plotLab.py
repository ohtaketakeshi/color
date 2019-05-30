import plotly
import plotly.graph_objs as go
import numpy as np
import colour

d65 = colour.ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
def sRGB2Lab(rgb):
    return colour.XYZ_to_Lab(colour.sRGB_to_XYZ(rgb / 255, illuminant=d65), illuminant=d65)

gridN = 9

grid = np.linspace(0,256,gridN,True) - 1
grid[0] = 0

rr, gg, bb = np.meshgrid(grid,grid,grid,indexing="ij")
rgb = np.stack((rr,gg,bb), axis=3)
ind_Xp = rgb[:,:,:,0]==255
ind_Xm = rgb[:,:,:,0]==0
ind_Yp = rgb[:,:,:,1]==255
ind_Ym = rgb[:,:,:,1]==0
ind_Zp = rgb[:,:,:,2]==255
ind_Zm = rgb[:,:,:,2]==0

print("convert sRGB to Lab")
lab = np.apply_along_axis(sRGB2Lab, 3, rgb)

print("extract faces")
vXp = lab[ind_Xp].reshape((-1,3))
vXm = lab[ind_Xm].reshape((-1,3))
vYp = lab[ind_Yp].reshape((-1,3))
vYm = lab[ind_Ym].reshape((-1,3))
vZp = lab[ind_Zm].reshape((-1,3))
vZm = lab[ind_Zp].reshape((-1,3))

cXp = rgb[ind_Xp].reshape((-1,3))
cXm = rgb[ind_Xm].reshape((-1,3))
cYp = rgb[ind_Yp].reshape((-1,3))
cYm = rgb[ind_Ym].reshape((-1,3))
cZp = rgb[ind_Zm].reshape((-1,3))
cZm = rgb[ind_Zp].reshape((-1,3))

faces = []
for i in range(gridN-1):
    for j in range(gridN-1):
        faces.append([i*gridN + j, (i+1)*gridN + j, i*gridN + (j+1)])
        faces.append([(i+1)*gridN + j, (i+1)*gridN + (j+1), i*gridN + (j+1)])
faces = np.array(faces, dtype=int)

v_planes = [vXp, vXm, vYp, vYm, vZp, vZm]
c_planes = [cXp, cXm, cYp, cYm, cZp, cZm]

data = []
for v,c in zip(v_planes,c_planes):
    edge = []
    for i in range(gridN):
        for j in range(gridN):
            if i < gridN-1:
                edge += [v[i*gridN+j], v[(i+1)*gridN + j], [None]*3]
            if j < gridN-1:
                edge += [v[i*gridN+j], v[i*gridN + (j+1)], [None]*3]
    edge = np.array(edge)
    go_edge = go.Scatter3d(
        x = edge[:,1],
        y = edge[:,2],
        z = edge[:,0],
        mode="lines",
        line=go.scatter3d.Line(color=('rgb(100,100,100)'))
    )
    go_mesh = go.Mesh3d(
        x = v[:,1],
        y = v[:,2],
        z = v[:,0],
        i = faces[:,0],
        j = faces[:,1],
        k = faces[:,2],
        vertexcolor=c,
        flatshading=True
    )
    data.append(go_mesh)
    data.append(go_edge)

layout = go.Layout(
    scene = dict (
        xaxis = dict (
            range = [-127,127]
        ),
        yaxis = dict(
            range = [-127,127]
        ),
        zaxis = dict(
            range = [0,100]
        )
    )
)
fig = go.Figure(data=data, layout=layout)
print("plot")
plotly.offline.plot(fig)