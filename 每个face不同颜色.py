import bpy
import bmesh
import random as rnd
import time

def deleteall():
    bpy.ops.object.select_all(action='SELECT')      
    bpy.ops.object.delete(use_global=False, confirm=False)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
        
def deleteallmaterials():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
        
def rndcolor():
    return [rnd.uniform(0,1.0),rnd.uniform(0,1.0),rnd.uniform(0,1.0),1.0]

def create_material_emission(color, name=None, energy=30, return_nodes=True):
    if name is None:
        name = ""

    material = bpy.data.materials.new(name=f"material.emission.{name}")
    material.use_nodes = True

    out_node = material.node_tree.nodes.get("Material Output")
    bsdf_node = material.node_tree.nodes.get("Principled BSDF")
    material.node_tree.nodes.remove(bsdf_node)

    node_emission = material.node_tree.nodes.new(type="ShaderNodeEmission")
    node_emission.inputs["Color"].default_value = color
    node_emission.inputs["Strength"].default_value = energy

    node_emission.location = 0, 0
    material.node_tree.links.new(node_emission.outputs["Emission"], out_node.inputs["Surface"])

    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return
    
def go():
    deleteall()
    
    #bpy.ops.mesh.primitive_torusknot_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False)
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    obj = bpy.context.active_object

    bpy.ops.object.editmode_toggle()
    
    bpy.ops.mesh.select_all()
    mat,_ = create_material_emission([0,0,0,1.0],"black",0)
    obj.data.materials.append(mat)

    objbmesh = bmesh.from_edit_mesh(obj.data)

    for face in objbmesh.faces:
        if rnd.uniform(0,1) >= 0:
            mat,_ = create_material_emission(rndcolor(),"test",rnd.uniform(1,6))
            obj.data.materials.append(mat)
            
            obj.active_material_index = face.index
            
            face.select = True
            bpy.ops.object.material_slot_assign()
            face.select = False
            
    bpy.ops.object.editmode_toggle()
        

if __name__ == "__main__":
    go()
    
    
    