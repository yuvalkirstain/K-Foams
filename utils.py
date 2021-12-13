from pymesh import Mesh
from pymesh.wires import WireNetwork, Inflator
from pymesh.meshio import save_mesh
from numpy import ndarray
import plotly.graph_objects as go


def graph2mesh(vertices: ndarray, edges: ndarray, edge_thickness: float = 0.05) -> Mesh:
    """
    converts a graph into a mesh object. see https://pymesh.readthedocs.io/en/latest/wire_mesh.html for more details.
    :param vertices: coordinates of vertices.
    :param edges: A list of vertex index pairs.
    :param edge_thickness: thickness of edges.
    :return mesh: the resulting mesh.
    """
    wire_network = WireNetwork().create_from_data(vertices.T, edges)
    inflator = Inflator(wire_network)
    inflator.inflate(edge_thickness, allow_self_intersection=True, per_vertex_thickness=False)
    mesh = inflator.mesh
    return mesh


def plot_graph(vertices: ndarray, edges: ndarray) -> None:
    fig = go.Figure()

    for v1_idx, v2_idx in edges.tolist():
        x1, y1, z1 = vertices[:, v1_idx]
        x2, y2, z2 = vertices[:, v2_idx]
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




