# Terrain_generator_3D
Terrain generator code using Perlin noise to make 3D STL models that can be used in simulations easily. These can be converted to urdf files that can be used in ROS or Pybullet simulations. 

## Dependencies 

```bash
pip install noise
pip install numpy-stl
pip install numpy-stl trimesh
```

## Examples

<table>
  <tr>
    <td><img src="https://github.com/shepai/Terrain_generator_3D/blob/main/assets/example1.png?raw=true" alt="Image 1" width="200" /></td>
    <td><img src="https://github.com/shepai/Terrain_generator_3D/blob/main/assets/example2.png?raw=true" alt="Image 2" width="200" /></td>
  </tr>
  <tr>
    <td><img src="https://github.com/shepai/Terrain_generator_3D/blob/main/assets/example3.png?raw=true" alt="Image 3" width="200" /></td>
    <td><img src="https://github.com/shepai/Terrain_generator_3D/blob/main/assets/example4.png?raw=true" alt="Image 4" width="200" /></td>
  </tr>
</table>

```python

from Terrain_gen import generator

#create generator and make an stl and then make a urdf
test=generator(size = 100,scale = 50, octaves = 10, persistence = 0.9, lacunarity = 5.0)
test.saveSTL("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.stl")
test.saveObj("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.obj")
test.create_urdf("/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.stl","/its/home/drs25/Documents/GitHub/Terrain_generator_3D/assets/test.urdf")
```