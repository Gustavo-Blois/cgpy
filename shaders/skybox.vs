#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 TexCoords;

uniform mat4 view;
uniform mat4 projection;

void main()
{
    // Removemos a translação da matriz de view para fixar a skybox na posição da câmera
    mat4 rotView = mat4(mat3(view));
    vec4 pos = projection * rotView * vec4(aPos, 1.0);
    gl_Position = pos.xyww; // manter z = w para desenhar sempre "atrás"

    TexCoords = aPos;
}