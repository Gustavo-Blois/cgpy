import glfw
import glm

# Estado da câmera: posição, direção e orientação
cameraPos   = glm.vec3(0.0, 0.0, 3.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp    = glm.vec3(0.0, 1.0, 0.0)

# Controle de mouse e zoom
firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = 0.0  # inicializo depois com tamanho da tela
lastY = 0.0
fov = 45.0

# Controle de tempo pra animações suaves
deltaTime = 0.0
lastFrame = 0.0

# Usei WASD pra mover e o mouse pra olhar em volta (igual a um jogo 3D)
def key_event(window, key, scancode, action, mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode, deltaTime

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    cameraSpeed = 50 * deltaTime
    if key == glfw.KEY_W and (action == glfw.PRESS or action == glfw.REPEAT):
        cameraPos += cameraSpeed * cameraFront
    if key == glfw.KEY_S and (action == glfw.PRESS or action == glfw.REPEAT):
        cameraPos -= cameraSpeed * cameraFront
    if key == glfw.KEY_A and (action == glfw.PRESS or action == glfw.REPEAT):
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if key == glfw.KEY_D and (action == glfw.PRESS or action == glfw.REPEAT):
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    if key == glfw.KEY_P and action == glfw.PRESS:
        polygonal_mode = not polygonal_mode

# Atualiza viewport quando a janela muda de tamanho
def framebuffer_size_callback(window, width, height):
    from OpenGL.GL import glViewport
    glViewport(0, 0, width, height)

# Aqui controlo a câmera com o mouse, atualizando yaw e pitch
def mouse_callback(window, xpos, ypos):
    global cameraFront, lastX, lastY, firstMouse, yaw, pitch

    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    pitch = max(min(pitch, 89.0), -89.0)

    front = glm.vec3()
    front.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    front.y = glm.sin(glm.radians(pitch))
    front.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)

# Com a rolagem do mouse eu aproximo ou afasto o zoom (FOV da câmera)
def scroll_callback(window, xoffset, yoffset):
    global fov
    fov -= yoffset
    fov = max(1.0, min(fov, 45.0))
