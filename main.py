import glfw

glfw.init()
window = glfw.create_window(640, 480, "Teste", None, None)
print("Contexto válido?" , "SIM" if glfw.get_current_context() else "NÃO")
glfw.terminate()