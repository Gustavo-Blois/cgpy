import glfw
import glm

# Estado da câmera
cameraPos   = glm.vec3(0.0, 0.0, 3.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp    = glm.vec3(0.0, 1.0, 0.0)

# Configuração de movimento
polygonal_mode = False
deltaTime = 0.0

# Variáveis usadas para controle das transformações
pulse_mode = False
rotate_mode = False
move_mode = False
# Controle de mouse e zoom
firstMouse = True
lastX = 0.0
lastY = 0.0
yaw = -90.0
pitch = 0.0
fov = 45.0

def key_event(window, key, scancode, action, mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode, deltaTime, pulse_mode, move_mode, rotate_mode


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
        print(f"[DEBUG] Modo poligonal: {polygonal_mode}")
    if key == glfw.KEY_U and action == glfw.PRESS:
        pulse_mode = not pulse_mode
    if key == glfw.KEY_R and action == glfw.PRESS:
        rotate_mode = not rotate_mode
    if key == glfw.KEY_M and action == glfw.PRESS:
        move_mode = not move_mode

    
    cameraPos.x = max(-60.0, min(60.0, cameraPos.x))
    cameraPos.y = max(-3.0, min(30.0, cameraPos.y))
    cameraPos.z = max(-60.0, min(60.0, cameraPos.z))
    

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

def scroll_callback(window, xoffset, yoffset):
    global fov
    fov -= yoffset
    fov = max(1.0, min(fov, 45.0))

def framebuffer_size_callback(window, width, height):
    from OpenGL.GL import glViewport
    glViewport(0, 0, width, height)
