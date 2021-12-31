import numpy as np
from math import cos, sin
import random


def create_k_nearest_foams_graph(grid_cells_points, grid_cells_sizes, angle, stretch, k, dim):
    vertices = generate_vertices(grid_cells_points, grid_cells_sizes, dim)
    edges = generate_edges(vertices, angle, stretch, k, dim)

    return vertices, edges


def generate_vertices(grid_cells_points, grid_cells_sizes, dim):
    vertices = []
    for cell_idx in range(len(grid_cells_points)):
        cell_start_point = grid_cells_points[cell_idx]
        cell_size = grid_cells_sizes[cell_idx]
        cell_random_point = [random.uniform(cell_start_point[d], cell_start_point[d] + cell_size) for d in range(dim)]
        vertices.append(tuple(cell_random_point))

    return vertices


def generate_edges(vertices, angles, stretches, k, dim):
    edges = []

    vertices_M = [get_distance_matrix(angles[point_idx], stretches[point_idx], dim)
                  for point_idx in range(len(vertices))]

    for point_idx in range(len(vertices)):
        point_distances = get_point_distances(point_idx, vertices, vertices_M)

        point_knn = sorted(point_distances, key=lambda x: x[1])[:k] # sort by distance
        point_edges = [(point_idx, neighbor_idx) for neighbor_idx, dist in point_knn]
        edges.extend(point_edges)

    return edges


def get_distance_matrix(angle, stretch, dim):
    E = create_rotation_matrix(angle, dim)
    U = create_stretch_matrix(stretch)
    EtU = np.matmul(np.transpose(E), U)
    M = np.matmul(EtU, E)
    return M


def create_rotation_matrix(angle, dim):
    if dim == 2:
        theta = angle
        R = np.array([
            [cos(theta), -sin(theta)],
            [sin(theta), cos(theta)]
        ])
    elif dim == 3:
        psi = angle[0]
        phi = angle[1]
        theta = angle[2]

        R = np.array([
            [cos(psi) * cos(theta) * cos(phi) - sin(psi) * sin(phi),
             -cos(psi) * cos(theta) * sin(phi) - sin(psi) * cos(phi),
             cos(psi) * sin(theta)],

            [sin(psi) * cos(theta) * cos(phi) + cos(psi) * cos(phi),
             -sin(psi) * cos(theta) * sin(phi) + cos(psi) * cos(phi),
             sin(psi) * sin(theta)],

            [-sin(theta) * cos(phi),
             sin(theta) * sin(phi),
             cos(theta)]])
    else:
        raise ValueError('only support 3D and 2D cases')
    return R


def create_stretch_matrix(stretch):
    U = np.diag(np.power(stretch, -2))
    return U


def get_point_distances(point_idx, vertices, vertices_M):
    point_distances = []
    for curr_point_idx in range(len(vertices)):
        if curr_point_idx == point_idx:
            continue

        d_ij = distance(vertices[point_idx], vertices[curr_point_idx],
                        vertices_M[point_idx], vertices_M[curr_point_idx])
        point_distances.append((curr_point_idx, d_ij))

    return point_distances


def distance(point_i, point_j, M_i, M_j):
    p_i, p_j = np.array(point_i), np.array(point_j)
    d_pi_pj = np.sqrt(np.matmul(np.matmul(np.transpose((p_i - p_j)), M_i), (p_i - p_j)))
    d_pj_pi = np.sqrt(np.matmul(np.matmul(np.transpose((p_j - p_i)), M_j), (p_j - p_i)))
    return (d_pi_pj + d_pj_pi) / 2