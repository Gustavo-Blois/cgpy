import glm
import numpy as np
from camera import cameraPos, cameraFront, cameraUp, fov

# Essa função cria a matriz de modelo aplicando:
# 1. Escala
# 2. Rotação (em torno de eixo arbitrário)
# 3. Translação
def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    angle = glm.radians(angle)
    matrix_transform = glm.mat4(1.0)

    # Aplico as transformações na ordem inversa da leitura (S * R * T)
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))
    if angle != 0:
        matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))

    return np.array(matrix_transform)

# Cria a matriz de visualização com base na posição da câmera e direção
def view():
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
    return np.array(mat_view)

# Gera a matriz de projeção em perspectiva
def projection(aspect_ratio):
    mat_projection = glm.perspective(glm.radians(fov), aspect_ratio, 0.1, 100.0)
    return np.array(mat_projection)
