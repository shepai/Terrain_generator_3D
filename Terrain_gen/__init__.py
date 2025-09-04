import numpy as np
from stl import mesh
import noise
import trimesh
from scipy.spatial import Delaunay

class generator:
    def __init__(self,size = 100):
         # size of the terrain (100x100 grid)
         # Scaling factor for the Perlin noise
         # Number of layers of noise to add complexity to the terrain
         # How much each layer contributes to the overall shape
         # Frequency change between octaves
         # Create an empty grid for the vertices
         self.size=size
    def generateTactileData(self,filename):
        x_vals = np.arange(0, 6 * self.size +0.5, 0.1)
        y_vals = np.arange(0, 6 * self.size + 1.2, 0.1)
        x, y = np.meshgrid(x_vals, y_vals)
        # z1
        A1 = 1
        A2 = 0
        f1 = 1
        f2 = 1
        phi = np.pi / 2
        z1 = A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        # z2
        A2 = 1
        z2 = A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        # z3
        z3 = np.zeros_like(x)
        N = 25
        for ii in range(1, N + 1, 2):
            A1 = (8 / np.pi**2) * ((-1)**((ii - 1) // 2)) / ii**2
            A2 = A1
            f1 = f2 = ii
            phi = 0
            z3 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        # z4
        z4 = np.zeros_like(x)
        N = 101
        for ii in range(1, N + 1, 2):
            A1 = 4 / (np.pi * ii)
            A2 = A1
            f1 = f2 = ii
            phi = 0
            z4 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        # z5
        z5 = np.zeros_like(x)
        N = 25
        for ii in range(1, N + 1, 2):
            A1 = (8 / np.pi**2) * ((-1)**((ii - 1) // 2)) / ii**2
            A2 = 0
            f1 = f2 = ii
            phi = 0
            z5 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        # z6
        z6 = np.zeros_like(x)
        N = 101
        for ii in range(1, N + 1, 2):
            A1 = 4 / (np.pi * ii)
            A2 = 0
            f1 = f2 = ii
            phi = 0
            z6 += A1 * np.sin(f1 * x) + A2 * np.sin(f2 * y + phi)
        Zs=[z1,z2,z3,z4,z5,z6]
        f=filename.split(".")
        for i,z in enumerate(Zs):
            self.export_surface_to_solid_block(x, y, z, filename=f[0]+str(i)+"."+f[1])
    def surface_to_stl(self,x, y, z, filename='output.stl', height_offset=0):
        # Flatten the meshgrid and shift z if needed
        vertices = np.column_stack((x.ravel(), y.ravel(), z.ravel() + height_offset))
        
        # Create faces using row and column indexing
        n_rows, n_cols = x.shape
        faces = []
        for i in range(n_rows - 1):
            for j in range(n_cols - 1):
                idx = i * n_cols + j
                faces.append([idx, idx + 1, idx + n_cols])
                faces.append([idx + 1, idx + n_cols + 1, idx + n_cols])
        
        # Convert to numpy arrays
        faces = np.array(faces)
        
        # Create mesh and export
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        mesh.export(filename)
        print(f"Exported {filename}")

    def export_surface_to_solid_block(self,x, y, z, filename="solid_block.stl", thickness=7.0):
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        thickness=thickness-(np.max(z)-np.min(z))
        print(thickness)
        assert x.shape == y.shape == z.shape

        # Flatten to 1D for triangulation
        x_flat = x.ravel()
        y_flat = y.ravel()
        z_flat = z.ravel()
        top_vertices = np.column_stack((x_flat, y_flat, z_flat))

        # Triangulate x-y
        tri = Delaunay(np.column_stack((x_flat, y_flat)))
        top_faces = tri.simplices


        # Export as mesh
        mesh = trimesh.Trimesh(vertices=top_vertices, faces=top_faces, process=True)
        mesh.export(filename)
        print(f"Exported watertight solid block to {filename}")
    def generateNoise(self,filename,scale = 50, octaves = 10, persistence = 0.9, lacunarity = 5.0):
        vertices = np.zeros((self.size, self.size, 3), dtype=np.float32)

        # Create the terrain using Perlin noise
        for x in range(self.size):
            for y in range(self.size):
                z = noise.pnoise2(x / scale, y / scale, octaves=octaves,
                                persistence=persistence, lacunarity=lacunarity)
                vertices[x, y] = [x, y, z * 10]  # Scale the z-value for height
        self.size=self.size
        # Now we need to create triangles for the mesh
        # Each square on the grid will have 2 triangles
        faces = []
        for x in range(self.size - 1):
            for y in range(self.size - 1):
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
        if ".stl" not in filepath: filepath+=".stl"
        self.terrain.save(filepath)
    def saveObj(self,filepath):
        self.saveSTL(filepath.replace(".obj",".stl"))
        trimesh_mesh = trimesh.load_mesh(filepath.replace(".obj",".stl"))
        # Save the mesh as an OBJ file
        obj_filename = filepath.replace(".stl",".obj")
        trimesh_mesh.export(obj_filename)
    def create_urdf(self,stl_filename, urdf_filename, link_name="terrain_link"):
        #self.terrain.save(stl_filename)
        urdf_content = f"""
    <?xml version="0.0" ?>
<robot name="plane">
  <link name="planeLink">
  <contact>
      <lateral_friction value="1"/>
  </contact>
    <inertial>
      <origin xyz="X Y Z" rpy="0 0 0"/>
       <mass value=".0"/>
       <inertia ixx="0" ixy="0" ixz="0" iyy="0" iyz="0" izz="0"/>
    </inertial>
    <visual>
      <origin xyz="X Y Z" rpy="0 0 0"/>
      <geometry>
				<mesh filename="{stl_filename}" scale="0.05 0.05 0.05"/>
      </geometry>
       <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision concave="yes"> 
      <origin xyz="X Y Z" rpy="0 0 0"/>
      <geometry>
	 	<mesh filename="{stl_filename}" scale="0.05 0.05 0.05"/>
      </geometry>
    </collision>
  </link>
</robot>

    """
        # Save the URDF content to a file
        with open(urdf_filename, 'w') as urdf_file:
            urdf_file.write(urdf_content)

        print(f"URDF file '{urdf_filename}' generated successfully.")

if __name__=="__main__":
    test=generator(size = 12)
    test.generateTactileData("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/tactile.stl")
    #test.saveSTL("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/tactile.stl")
    #test.saveObj("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/tactile.obj")
    test.create_urdf("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/tactile0.stl","/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/tactile.urdf")
