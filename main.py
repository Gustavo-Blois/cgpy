import glfw
from OpenGL.GL import *
import numpy as np
import os
from shader_s import Shader
from camera import *
from transform import model, view, projection
from model_loader import load_obj_and_texture
from skybox import create_skybox, load_cubemap, draw_skybox

# Inicializando GLFW e criando janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

largura, altura = 800, 600
window = glfw.create_window(largura, altura, "Meu Projeto 3D", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela GLFW")

glfw.make_context_current(window)

# Setando callbacks e capturando mouse
lastX, lastY = largura / 2.0, altura / 2.0
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_key_callback(window, key_event)
glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_scroll_callback(window, scroll_callback)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# Compilando shaders
main_shader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
skybox_shader = Shader("shaders/skybox.vs", "shaders/skybox.fs")
main_shader.use()
program = main_shader.getProgram()

# Inicializando listas de vértices e texturas
vertices_list = []
textures_coord_list = []

# Carregando modelo e texturas
vert_ini, vert_count, tex_id = load_obj_and_texture(
    'assets/objetos/spiderman/spiderman.obj',
    ['assets/objetos/spiderman/spiderman.png'],
    vertices_list,
    textures_coord_list,
    texture_start_id=0
)
# Exibe a janela antes de criar o skybox
glfw.show_window(window)
glEnable(GL_DEPTH_TEST)
glfw.make_context_current(window)
glfw.poll_events()  # Processa eventos pendentes para "ativar" o contexto
glClear(GL_COLOR_BUFFER_BIT)  # Operação OpenGL simples para forçar inicialização
glfw.swap_buffers(window)


# Carregando skybox
faces = [
    "assets/skybox/right.png",
    "assets/skybox/left.png",
    "assets/skybox/top.png",
    "assets/skybox/bottom.png",
    "assets/skybox/front.png",
    "assets/skybox/back.png"
]


#skybox_vao = create_skybox()
#skybox_texture = load_cubemap(faces)

# Enviando dados para GPU
buffer_VBO = glGenBuffers(2)
vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[0])
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
stride = vertices.strides[0]
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))

textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])
textures['position'] = textures_coord_list
glBindBuffer(GL_ARRAY_BUFFER, buffer_VBO[1])
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
stride = textures.strides[0]
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, False, stride, ctypes.c_void_p(0))


polygonal_mode = False

# Loop principal
while not glfw.window_should_close(window):
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame

    glfw.poll_events()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Desenhando o modelo com shader principal
    main_shader.use()
    mat_model = model(0.0, 0, 0, 1, 0, 0, -5, 1.5, 1.5, 1.5)
    glUniformMatrix4fv(glGetUniformLocation(program, "model"), 1, GL_TRUE, mat_model)

    mat_view = view()
    glUniformMatrix4fv(glGetUniformLocation(program, "view"), 1, GL_TRUE, mat_view)

    mat_proj = projection(largura / altura)
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, GL_TRUE, mat_proj)

    glBindTexture(GL_TEXTURE_2D, 0)
    glDrawArrays(GL_TRIANGLES, vert_ini, vert_count)

    # Desenhando a skybox por último
    #draw_skybox(skybox_vao, skybox_texture, mat_view, mat_proj, skybox_shader)

    glfw.swap_buffers(window)

glfw.terminate()
