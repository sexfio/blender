import bpy
import bmesh
import random as rnd

def DeleteAll():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
    
def RndColor():
    return [rnd.uniform(0,1.0),rnd.uniform(0,1.0),rnd.uniform(0,1.0),1.0]

def SetMaterial(obj,color):
    material = bpy.data.materials.new(name=f'rnd color material')   # maybe repeated
    material.use_nodes = True
    #rnd_material.diffuse_color = RndColor()
    #bpy.data.materials[rnd_material.name].node_tree.nodes["Emission"].inputs[0].default_value = (0.0441256, 0.57093, 1, 1)
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = rnd.uniform(0,1)
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = rnd.uniform(0,1)
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    obj.data.materials.append(material)

def go_1():
    DeleteAll()

    a = []
    for _ in range(9):
        x = rnd.uniform(-5,5)
        y = rnd.uniform(-5,5)
        z = rnd.uniform(-5,5)
        a.append([x,y,z])
        print(x,y,z)
        
    for aa in a:
        if aa[2] <= -2:
            bpy.ops.mesh.primitive_ico_sphere_add(radius=1, location=[aa[0],aa[1],aa[2]])
        elif aa[2] > -2 and aa[2] <= 1:
            bpy.ops.mesh.primitive_cube_add(size=1,location=[aa[0],aa[1],aa[2]])
        else:        
            bpy.ops.mesh.primitive_cone_add(location=[aa[0],aa[1],aa[2]])
        obj = bpy.context.active_object
        SetMaterial(obj,RndColor())
    
    cubes = []
    for obj in bpy.data.objects:
        if "Cube" in obj.name:
            cubes.append(obj)
    
    for cube in cubes:
        location = cube.location
        bpy.data.objects.remove(cube)
        bpy.ops.mesh.primitive_monkey_add(location=location)
        obj = bpy.context.active_object
        SetMaterial(obj,RndColor())

#----------------------------------------------------------------------------------------
if _name_ == "__main__":
    go_1()