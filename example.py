from Terrain_gen import generator

#create generator and make an stl and then make a urdf
test=generator(50,90,9,0.5,5)
test.saveSTL("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.stl")
test.saveObj("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.obj")
test.create_urdf("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.stl","/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.urdf")

#view mesh
import matplotlib
matplotlib.use('TKAgg')
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Create a new plot
figure = pyplot.figure()
axes = figure.add_subplot(projection='3d')

# Load the STL files and add the vectors to the plot
your_mesh = test.terrain
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()