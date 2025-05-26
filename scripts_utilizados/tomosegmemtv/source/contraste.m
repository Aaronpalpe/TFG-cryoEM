E = imread('C:\Users\aaron\Desktop\FoilHole_22351071_Data_22332517_13_20240524_083212_Fractions_corr.jpg', 'jpg');
figure(1)
imshow(E, []) % Reescala con max y minimo en grises

[Ny, Nx, Nz] = size(E);

% Check if the image is 2D or 3D

s = 25; % Ejemplo de factor de escala
sg = 6; % Ejemplo de varianza para el prefiltrado gaussiano
m = -1; % Ejemplo de ángulo semiabierto del missing wedge
d = 1; % Ejemplo de datos de entrada
v = 1; % Modo verbose desactivado

for s = 30:5:40
    for sg = 5:1:10
        figure(3)
        S = dtvoting(E, s, sg, m, d, v);
        imshow(S, []);
        imwrite(mat2gray(S), ['C:\Users\aaron\Desktop\matriz\', num2str(s), '-', num2str(sg), '.jpg']);

    end
end

