import numpy as np
from stl import mesh
import noise

class generator:
    def __init__(self,size = 100,scale = 50, octaves = 10, persistence = 0.9, lacunarity = 5.0):
         # size of the terrain (100x100 grid)
         # Scaling factor for the Perlin noise
         # Number of layers of noise to add complexity to the terrain
         # How much each layer contributes to the overall shape
         # Frequency change between octaves
         # Create an empty grid for the vertices
        vertices = np.zeros((size, size, 3), dtype=np.float32)

        # Create the terrain using Perlin noise
        for x in range(size):
            for y in range(size):
                z = noise.pnoise2(x / scale, y / scale, octaves=octaves,
                                persistence=persistence, lacunarity=lacunarity)
                vertices[x, y] = [x, y, z * 10]  # Scale the z-value for height

        # Now we need to create triangles for the mesh
        # Each square on the grid will have 2 triangles
        faces = []
        for x in range(size - 1):
            for y in range(size - 1):
                # Get the vertices of the square
                v1 = vertices[x, y]
                v2 = vertices[x + 1, y]
                v3 = vertices[x, y + 1]
                v4 = vertices[x + 1, y + 1]

                # Create two triangles from the square
                faces.append([v1, v2, v3])  # Triangle 1
                faces.append([v2, v4, v3])  # Triangle 2

        # Convert the faces to a format suitable for the STL file
        faces = np.array(faces)

        # Create the mesh
        terrain_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

        for i, face in enumerate(faces):
            for j in range(3):
                terrain_mesh.vectors[i][j] = face[j]
        self.terrain=terrain_mesh
    def saveSTL(self,filepath):
        if ".stl" not in filepath: filepath+=".stl"
        self.terrain.save(filepath)
    def create_urdf(self,stl_filename, urdf_filename, link_name="terrain_link"):
        self.terrain.save(stl_filename)
        urdf_content = f"""<?xml version="1.0"?>
    <robot name="terrain">
    <link name="{link_name}">
        <visual>
        <geometry>
            <mesh filename="{stl_filename}" scale="1 1 1"/>
        </geometry>
        <material name="terrain_material">
            <color rgba="0.8 0.8 0.8 1.0"/>
        </material>
        </visual>
        <collision>
        <geometry>
            <mesh filename="{stl_filename}" scale="1 1 1"/>
        </geometry>
        </collision>
    </link>
    </robot>
    """
        # Save the URDF content to a file
        with open(urdf_filename, 'w') as urdf_file:
            urdf_file.write(urdf_content)

        print(f"URDF file '{urdf_filename}' generated successfully.")
