import bpy
import bmesh
import random as rnd
import time

def wfileline(filename,s,mode=8):
    if mode == 8:
        f= open(filename,"a")
        f.write (s + "\n")
        f.closed
    elif mode == 2:
        f = open(filename, "w")
        f.write(s + "\n")
        f.closed

def deleteall():
    changemode('object')
    bpy.ops.object.select_all(action='SELECT')      
    bpy.ops.object.delete(use_global=False, confirm=False)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
        
def deleteallmaterials():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
        
def rndcolor():
    return [rnd.uniform(0,1.0),rnd.uniform(0,1.0),rnd.uniform(0,1.0),1.0]

def create_material_principled(color, name=None, return_nodes=True):
    if name is None:
        name = ""
        
    material = bpy.data.materials.new(name=f"material.principled.{name}")
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0
    material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    
    if return_nodes:
        return material, material.node_tree.nodes
    else:
        return 

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
    
def changemode(mode='object'):
    if bpy.context.active_object == None:
        return
    
    if mode == 'object':
        if bpy.context.active_object.mode == 'OBJECT':
            return
        else:
            bpy.ops.object.editmode_toggle()
            return
    elif mode == 'edit':
        if bpy.context.active_object.mode == 'EDIT':
            return
        else:
            bpy.ops.object.editmode_toggle()
            return
    
def key_z_at_frame(obj, at_frame, loc):
    obj.keyframe_insert(data_path='location', frame=at_frame)
    act = obj.animation_data.action
    fc = act.fcurves.find('location', index=2)
    for kp in fc.keyframe_points:
        if kp.co[0] == at_frame:
            kp.co[1] = loc
            
def bmesh_from_object(obj):
    """
    Object/Edit Mode get mesh, use bmesh_to_object() to write back.
    """
    me = obj.data
    is_editmode = (obj.mode == 'EDIT')
    if is_editmode:
        bm = bmesh.from_edit_mesh(me)
    else:
        bm = bmesh.new()
        bm.from_mesh(me)
    return bm


def bmesh_to_object(obj, bm):
    """
    Object/Edit Mode update the object.
    """
    me = obj.data
    is_editmode = (obj.mode == 'EDIT')
    if is_editmode:
        bmesh.update_edit_mesh(me, True)
    else:
        bm.to_mesh(me)
    # grr... cause an update
    if me.vertices:
        me.vertices[0].co[0] = me.vertices[0].co[0]
        
#-------------------------------------------------------------------------------------------------------
    
def go1():
    deleteall()
    
    #bpy.ops.mesh.primitive_cube_add()
    #bpy.ops.mesh.primitive_torusknot_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False)
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    obj = bpy.context.active_object

    changemode('edit')
    
    bpy.ops.mesh.select_all()
    mat,_ = create_material_emission([0,0,0,1.0],"black1",0)
    obj.data.materials.append(mat)
    
    mat,_ = create_material_emission([0,0,0,1.0],"black2",0)
    obj.data.materials.append(mat)
    
    objbmesh = bmesh.from_edit_mesh(obj.data)
    cur_frame = bpy.context.scene.frame_current   #返回当前frame

    for face in objbmesh.faces:
        if rnd.uniform(0,1) >= 0:
            mat,_ = create_material_emission(rndcolor(),"test",rnd.uniform(1,6),True)
            obj.data.materials.append(mat)
            
            obj.active_material_index = face.index
            #mat.inputs[1].keyframe_insert("default_value", frame=cur_frame)
            
            face.select = True
            bpy.ops.object.material_slot_assign()
            face.select = False
            
    changemode('object')
    
def go2():   #just change the color of material
    obj = bpy.context.active_object
    
    changemode('edit')
    
    bpy.ops.mesh.select_all()
    #mat,_ = create_material_emission([0,0,0,1.0],"black",0)
    #obj.data.materials.append(mat)
    
    objbmesh = bmesh.from_edit_mesh(obj.data)
    cur_frame = bpy.context.scene.frame_current   #返回当前frame

    for face in objbmesh.faces:
        if rnd.uniform(0,1) >= 0:
            mat = obj.data.materials[face.material_index]
            mat.node_tree.nodes["Emission"].inputs[0].default_value = rndcolor()
            
            #mat.inputs[1].keyframe_insert("default_value", frame=cur_frame)
            
            
    changemode('object')
    
def go3():   #maybe stronger code
    deleteall()
    
    #bpy.ops.mesh.primitive_cube_add()
    #bpy.ops.mesh.primitive_torusknot_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), change=False)
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    
    obj = bpy.context.active_object

    changemode('edit')
    
    #bpy.ops.mesh.select_all()
    mat,_ = create_material_emission(rndcolor(),"black1",0)
    obj.data.materials.append(mat)
    
    objbmesh = bmesh.from_edit_mesh(obj.data)
    cur_frame = bpy.context.scene.frame_current   #返回当前frame

    for i,face in enumerate(objbmesh.faces):
        if rnd.uniform(0,1) >= 0:
            mat,_ = create_material_emission(rndcolor(),"test",rnd.uniform(1,6))
            obj.data.materials.append(mat)
            
            obj.material_slots.update()
            face.material_index = obj.material_slots.find(mat.name)
            
            #bpy.data.materials[mat.name].node_tree.nodes["Emission"].inputs[0].keyframe_insert("default_value", frame=1)
            
            for ii in range(1,250,rnd.randint(5,20)):
                mat.node_tree.nodes["Emission"].inputs[0].default_value = rndcolor()
                mat.node_tree.nodes["Emission"].inputs[1].default_value = rnd.uniform(1,6)
                bpy.data.materials[mat.name].node_tree.nodes["Emission"].inputs[0].keyframe_insert("default_value", frame=ii)
                bpy.data.materials[mat.name].node_tree.nodes["Emission"].inputs[1].keyframe_insert("default_value", frame=ii)
    
    changemode('object')
    
#----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    go3()
    
    
#obj.data.materials[objbmesh.faces[0].material_index].name
#obj.active_material_index   当前选中的material是第几个material  0->
#obj.active_material.name    当前选中的material's name
#objbmesh.faces[0].material_index   指定某面的material是第几个material  0->
#face.index 0->
#obj.material_slots.find(mat.name)

#mat.inputs[1].keyframe_insert("default_value", frame=cur_frame)

