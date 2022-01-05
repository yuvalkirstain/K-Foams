from pymesh import Mesh
from pymesh.wires import WireNetwork, Inflator
from pymesh.meshio import save_mesh
from numpy import ndarray, array
import math
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def graph2mesh(vertices: ndarray, edges: ndarray, edge_thickness: float = 0.05, expansion: float = 20) -> Mesh:
    """
    converts a graph into a mesh object. see https://pymesh.readthedocs.io/en/latest/wire_mesh.html for more details.
    :param vertices: coordinates of vertices.
    :param edges: A list of vertex index pairs.
    :param edge_thickness: thickness of edges.
    :param expansion: thickness of edges.
    :return mesh: the resulting mesh.
    """
    V = []
    E = []
    for v in vertices:
        V.append(expansion * array(v))
    for e in edges:
        v1, v2 = e
        if (v2, v1) in E:
            continue
        E.append((v1, v2))

    V, E = array(V), array(E)

    wire_network = WireNetwork().create_from_data(V, E)
    inflator = Inflator(wire_network)
    inflator.inflate(edge_thickness, allow_self_intersection=True, per_vertex_thickness=False)
    mesh = inflator.mesh
    return mesh


def plot_graph_2d(vertices: ndarray, edges: ndarray) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111)

    x_values = [round(val[0]) for val in vertices]
    y_values = [round(val[1]) for val in vertices]

    for xi in range(math.floor(min(x_values)), math.floor(max(x_values)) + 1):
        ax.axvline(x=xi, linestyle='--')
    for yi in range(math.floor(min(y_values)), math.floor(max(y_values)) + 1):
        ax.axhline(y=yi, linestyle='--')

    for p1_idx, p2_idx in edges:
        ax.plot(*zip(vertices[p1_idx], vertices[p2_idx]), 'ko-')

    ax.set_aspect('equal')
    fig.set_size_inches((10, 10))
    fig.show()


def plot_graph_3d(vertices: ndarray, edges: ndarray) -> None:
    fig = go.Figure()

    for v1_idx, v2_idx in edges:
        x1, y1, z1 = vertices[v1_idx]
        x2, y2, z2 = vertices[v2_idx]
        fig.add_trace(go.Scatter3d(
            x=[x1, x2], y=[y1, y2], z=[z1, z2],
            marker=dict(
                size=5,
                color='blue'
            ),
            line=dict(
                color='grey',
                width=4
            )
        ))

    fig.show()


def plot_mesh(mesh: Mesh) -> None:
    """
    plots a mesh.
    :param mesh: a mesh object.
    """
    fig = go.Figure(data=[
        go.Mesh3d(
            x=mesh.vertices[:, 0],
            y=mesh.vertices[:, 1],
            z=mesh.vertices[:, 2],
            i=mesh.faces[:, 0],
            j=mesh.faces[:, 1],
            k=mesh.faces[:, 2],
            showscale=True,
            colorscale='agsunset',
            opacity=0.50,
        )
    ])

    fig.show()


def save_mesh(mesh: Mesh, save_dir: str) -> None:
    save_mesh(save_dir, mesh)




