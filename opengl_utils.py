import numpy as np
import glm

# Retorna matriz de translação manual
def translation_matrix(x, y, z):
    return np.array(glm.translate(glm.mat4(1.0), glm.vec3(x, y, z)))

# Retorna matriz de escala
def scale_matrix(sx, sy, sz):
    return np.array(glm.scale(glm.mat4(1.0), glm.vec3(sx, sy, sz)))

# Retorna matriz de rotação em torno de eixo arbitrário (em graus)
def rotation_matrix(angle_degrees, x, y, z):
    angle_rad = glm.radians(angle_degrees)
    return np.array(glm.rotate(glm.mat4(1.0), angle_rad, glm.vec3(x, y, z)))

# Combina todas as transformações: escala → rotação → translação
def compose_transformations(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    T = translation_matrix(t_x, t_y, t_z)
    R = rotation_matrix(angle, r_x, r_y, r_z)
    S = scale_matrix(s_x, s_y, s_z)
    return T @ R @ S  # ordem reversa: S -> R -> T
