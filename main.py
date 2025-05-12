import glfw
import random
import math
import sys
from OpenGL.GL import *
import numpy as np
import camera  # use apenas este import
from shader_s import Shader
from transform import model, view, projection
from model_loader import load_obj_and_texture
from skybox import create_skybox, load_cubemap, draw_skybox

def desenha_objeto(angle, rx, ry, rz, tx, ty, tz, sx, sy, sz, textureId, verticeInicial, quantosVertices, program):
    mat_model = model(angle, rx, ry, rz, tx, ty, tz, sx, sy, sz)
    loc_model = glGetUniformLocation(program,"model")
    glUniformMatrix4fv(loc_model,1,GL_TRUE,mat_model)

    glBindTexture(GL_TEXTURE_2D,textureId)

    glDrawArrays(GL_TRIANGLES,verticeInicial,quantosVertices)


# Casa AABB antes de transformação
house_min_x, house_max_x = -4.622727, 3.229458
house_min_z, house_max_z = -2.887431, 3.188514
# Transformação aplicada à casa: scale=5, translate=(-30, -5, 30)
scale_house = 5.0
tx_house, ty_house, tz_house = -30.0, -5.0, 30.0
# AABB pós-transformação (apenas X/Z relevantes para rejeição de ruínas)
house_min_x_t = house_min_x * scale_house + tx_house
house_max_x_t = house_max_x * scale_house + tx_house
house_min_z_t = house_min_z * scale_house + tz_house
house_max_z_t = house_max_z * scale_house + tz_house
# Inicializando GLFW e criando janela
glfw.init()

largura, altura = 800, 600
window = glfw.create_window(largura, altura, "Meu Projeto 3D", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar janela GLFW")

glfw.make_context_current(window)

# Setando callbacks e capturando mouse
camera.lastX = largura / 2.0
camera.lastY = altura / 2.0
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_key_callback(window, camera.key_event)
glfw.set_cursor_pos_callback(window, camera.mouse_callback)
glfw.set_scroll_callback(window, camera.scroll_callback)
glfw.set_framebuffer_size_callback(window, camera.framebuffer_size_callback)

# Compilando shaders
main_shader = Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
skybox_shader = Shader("shaders/skybox.vs", "shaders/skybox.fs")
main_shader.use()
program = main_shader.getProgram()


# Carregando modelo e texturas
vertices_list, textures_coord_list = [], []
tex_id = 0
vert_ruina_ini, vert_ruina_count, tex_id = load_obj_and_texture(
    'assets/objetos/ruinas/ruinas.obj',
    ['assets/objetos/ruinas/albedo.jpg'],
    vertices_list,
    textures_coord_list,
    tex_id
)

vert_chao_ini, vert_chao_count, tex_chao_id = load_obj_and_texture(
    'assets/objetos/chao/chao.obj',
    ['assets/objetos/chao/text_Albedo.png'],vertices_list,textures_coord_list,    tex_id

)
vert_chest_ini, vert_chest_count, tex_chest_id = load_obj_and_texture(
    'assets/objetos/chest/Chest.obj',
    ['assets/objetos/chest/ChestAlbedo.png'],vertices_list,textures_coord_list,    tex_chao_id
)
vert_coral_ini, vert_coral_count, tex_coral_id = load_obj_and_texture(
    'assets/objetos/coral/coral1.obj',
    ['assets/objetos/coral/coral1Basecolor.jpg'],vertices_list,textures_coord_list,    tex_chest_id
)

vert_starfish_ini, vert_starfish_count, tex_starfish_id = load_obj_and_texture(
    'assets/objetos/starfish/starfish.obj',
    ['assets/objetos/starfish/starfish.png'],vertices_list,textures_coord_list,    tex_coral_id
)

vert_casa_ini, vert_casa_count, tex_casa_id = load_obj_and_texture(
    'assets/objetos/house/house.obj',
    ['assets/objetos/house/house.png'],vertices_list,textures_coord_list,    tex_starfish_id
)


vert_esqueleto_ini, vert_esqueleto_count, tex_esqueleto_id = load_obj_and_texture(
    'assets/objetos/skeleton/skeleton.obj',
    ['assets/objetos/skeleton/skeleton.png'],vertices_list,textures_coord_list,    tex_casa_id
)

vert_hay_ini, vert_hay_count, tex_hay_id = load_obj_and_texture(
    'assets/objetos/haybed/haybedOBJ.obj',
    ['assets/objetos/haybed/HayBaseColor.png'],vertices_list,textures_coord_list,    tex_esqueleto_id
)
vert_wood_ini, vert_wood_count, tex_wood_id = load_obj_and_texture(
    'assets/objetos/woodbed/woodbedOBJ.obj',
    ['assets/objetos/woodbed/bedwood.png'],vertices_list,textures_coord_list,    tex_hay_id
)

vert_fish_ini, vert_fish_count, tex_fish_id = load_obj_and_texture(
    'assets/objetos/fish/fish.obj',
    ['assets/objetos/fish/fish_texture.png'],vertices_list,textures_coord_list,    tex_wood_id
)

glfw.show_window(window)
glfw.focus_window(window)
glEnable(GL_DEPTH_TEST)
glfw.make_context_current(window)
glfw.poll_events()
glClear(GL_COLOR_BUFFER_BIT)
glfw.swap_buffers(window)

# Carregando skybox
faces = [
    "assets/skybox/px.png", "assets/skybox/nx.png",
    "assets/skybox/py.png", "assets/skybox/ny.png",
    "assets/skybox/pz.png", "assets/skybox/nz.png"
]
skybox_vao = create_skybox()
skybox_texture = load_cubemap(faces)

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

# Controle de tempo
lastFrame = 0.0

#variáveis de transformação
pulse = 0.0

def is_far_enough(pos, existing, min_dist=15.0):
    return all(math.dist(pos, p) > min_dist for p in existing)

occupied = []

ruin_positions = []
while len(ruin_positions) < 7:
    angle,x, z = random.uniform(0,360), random.uniform(0, 100), random.uniform(-100, 0)
    if not (house_min_x_t < x < house_max_x_t and house_min_z_t < z < house_max_z_t):
        posa = (angle, x, -5.0, z)
        pos = (x, -5.0, z)
        if is_far_enough(pos, occupied):
            ruin_positions.append(posa)
            occupied.append(pos)

coral_positions = []
while len(coral_positions) < 30:
    x, z = random.uniform(0, 45), random.uniform(-45, 0)
    if not (-35 < x < -25 and 25 < z < 35):
        coral_positions.append((x, -2, z))

fish_positions = []
while len(fish_positions) < 20:
    pos = (random.uniform(-40, 40), random.uniform(10, 20), random.uniform(-40, 40))
    if is_far_enough(pos, fish_positions):
        fish_positions.append(pos)

starfish_positions = [(random.uniform(-30, 30), random.uniform(-2,10), random.uniform(-30, 30)) for _ in range(25)]

# Loop principal
while not glfw.window_should_close(window):
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame
    camera.deltaTime = deltaTime  # sincroniza com módulo camera

    glfw.poll_events()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if camera.polygonal_mode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    if camera.pulse_mode:
        pulse = math.sin(currentFrame)

    if camera.rotate_mode: 
        rotate = math.sin(currentFrame) * 360
    else:
        rotate = 0
    
    if camera.move_mode: 
        move = currentFrame % 90
    else:
        move = 0

    


    main_shader.use()
    for angle, tx, ty, tz in ruin_positions:
        desenha_objeto(angle, 0, 1, 0, tx, ty,tz, 1.5, 1.5, 1.5,0,vert_ruina_ini,vert_ruina_count,program)
    desenha_objeto(0.0, 0, 0, 1, -10, -5, -5, 100.5, 100.5, 100.5,1,vert_chao_ini,vert_chao_count,program)
    for tx, ty, tz in coral_positions:
        desenha_objeto(0.0, 0, 0, 1, tx, ty, tz, 7.0 + pulse, 7.0 , 7.0 + pulse,3,vert_coral_ini,vert_coral_count,program)
    for tx, ty, tz in starfish_positions:
        desenha_objeto(rotate, 0, 0, 1, tx, ty, tz, 7.0, 7.0, 7.0,4,vert_starfish_ini,vert_starfish_count,program)
    for tx, ty, tz in fish_positions:
        desenha_objeto(90.0, 0, 1, 0, tx + move, ty, tz , 7.0, 7.0, 7.0,9,vert_fish_ini,vert_fish_count,program)


    #interno
    desenha_objeto(90.0, 0, 1, 0, -30, -5, 30, 5.0, 5.0, 5.0,5,vert_casa_ini,vert_casa_count,program)
    desenha_objeto(90.0, 0, 1, 0, -40, -5, 40, 0.2, 0.2, 0.2,2,vert_chest_ini,vert_chest_count,program)
    desenha_objeto(90.0, 0, 0, 1, -30, -5, 30, 5.0, 5.0, 5.0,6,vert_esqueleto_ini,vert_esqueleto_count,program)
    desenha_objeto(180.0, 0, 1, 0, -30, -5, 20, 1.0, 1.0, 1.0,7,vert_hay_ini,vert_hay_count,program)
    desenha_objeto(180.0, 0, 1, 0, -30, -5, 20, 1.0, 1.0, 1.0,8,vert_wood_ini,vert_wood_count,program)


    mat_view = view()
    glUniformMatrix4fv(glGetUniformLocation(program, "view"), 1, GL_TRUE, mat_view)

    mat_proj = projection(largura / altura)
    glUniformMatrix4fv(glGetUniformLocation(program, "projection"), 1, GL_TRUE, mat_proj)

    draw_skybox(skybox_vao, skybox_texture, mat_view, mat_proj, skybox_shader)

    glfw.swap_buffers(window)

glfw.terminate()

