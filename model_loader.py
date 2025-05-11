import numpy as np
from PIL import Image
from OpenGL.GL import *

# Aqui leio um .obj e extraio as infos de vértices, texturas e materiais (se tiver)
def load_model_from_file(filename):
    vertices = []
    texture_coords = []
    faces = []
    material = None

    with open(filename, "r") as f:
        for line in f:
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                vertices.append(list(map(float, values[1:4])))
            elif values[0] == 'vt':
                texture_coords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'f':
                face = []
                face_texture = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)
                faces.append((face, face_texture, material))

    model = {
        'vertices': vertices,
        'texture': texture_coords,
        'faces': faces
    }

    return model

# Essa função serve pra converter polígonos com mais de 3 vértices em triângulos
def circular_sliding_window_of_three(arr):
    if len(arr) == 3:
        return arr
    circular_arr = arr + [arr[0]]
    result = []
    for i in range(len(circular_arr) - 2):
        result.extend(circular_arr[i:i+3])
    return result

# Carrego a textura da imagem e configuro os parâmetros dela na GPU
def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(img_textura)
    img = img.convert("RGB")
    img_width, img_height = img.size
    image_data = img.tobytes("raw", "RGB", 0, -1)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

# Aqui junto tudo: carrego o .obj, extraio vértices e texturas, carrego texturas
def load_obj_and_texture(objFile, texturesList, vertices_list, textures_coord_list, texture_start_id=0):
    modelo = load_model_from_file(objFile)

    verticeInicial = len(vertices_list)
    faces_visited = []

    for face in modelo['faces']:
        if face[2] not in faces_visited:
            faces_visited.append(face[2])
        for vertice_id in circular_sliding_window_of_three(face[0]):
            vertices_list.append(modelo['vertices'][vertice_id - 1])
        for texture_id in circular_sliding_window_of_three(face[1]):
            textures_coord_list.append(modelo['texture'][texture_id - 1])

    verticeFinal = len(vertices_list)

    for i in range(len(texturesList)):
        load_texture_from_file(texture_start_id, texturesList[i])
        texture_start_id += 1

    return verticeInicial, verticeFinal - verticeInicial, texture_start_id
