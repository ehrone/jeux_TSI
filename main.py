from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text, decors
import numpy as np
import OpenGL.GL as GL
import pyrr

"""vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Zebi le', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    o = Text('Dinosaure', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)"""

def platforme(x,z,longeur, largeur, viewer, prog):
    """ Cette fontion sert à génerer une platforme
    PARAMETRES :
        entrées :
            x : le x autour duquel on centre la platforme
            z : le z de depart de la platforme
            largeur : largeur de la platforme
            longeur : longeur de la platforme
            viewer : objet de class viewer qui gère le monde
    
    """
    m = Mesh()
    p0, p1, p2, p3 = [-x-largeur/2, 0, z], [x-largeur/2, 0, z], [x-largeur/2, 0, z+longeur], [-x-largeur/2, 0, z+longeur]
    n, c = [0, 1, 0], [1, 0, 0]
    # les coordonnes de textures
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), prog, texture, Transformation3D(),z, longeur, largeur)
    viewer.add_object(o)


def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    # on decale de 2 vers nous l acamera dans l'espace
    viewer.cam.transformation.translation.y = 2
    # on definit le centre de rotation de la camera
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    # on recupere les coordonnées de notre cube
    m = Mesh.load_obj('cube.obj')
    #m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = 0
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('grass.jpg')
    points= [ [0,0,0], [1,0,0], [1,0,1], [0,0,1], [0,1,0], [1,1,0], [1,1,1], [0,1,1]]
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr,0, 1,1, points)
    viewer.add_object(o)

    longeur = 50
    largeur = 5

    # Première platforme
    m = Mesh()
    p0, p1, p2, p3 = [-largeur, 0, -2], [largeur, 0, -2], [largeur, 0, longeur], [-largeur, 0, longeur]
    n, c = [0, 1, 0], [1, 0, 0]
    # les coordonnes de textures
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    points= [ [-largeur, 0, -2], [largeur, 0, -2], [largeur, 0, longeur], [-largeur, 0, longeur], [-largeur, 0, -2], [largeur, 0, -2], [largeur, 0, longeur], [-largeur, 0, longeur]]
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),0, longeur, largeur, points)
    viewer.add_object(o)

    # Deuxième platforme
    m = Mesh()
    p0, p1, p2, p3 = [-largeur, 0, longeur], [largeur, 0, longeur], [largeur, 0, (longeur)*2], [-largeur, 0, (longeur)*2]
    n, c = [0, 1, 0], [1, 0, 0]
    # les coordonnes de textures
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    points= [[-largeur, 0, longeur], [largeur, 0, longeur], [largeur, 0, (longeur)*2], [-largeur, 0, (longeur)*2], [-largeur, 0, longeur], [largeur, 0, longeur], [largeur, 0, (longeur)*2], [-largeur, 0, (longeur)*2]]
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D(),longeur, longeur, largeur, points)
    viewer.add_object(o)

    
    # creation d'un obstacle DEMANDER A MAT COM%MENT IL PLACE SON OBJET
    # on recupere les coordonnées de notre rectangle
    m = Mesh.load_obj('obstacle.obj')
    #m.normalize()
    #m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
    tr = Transformation3D()
    tr.translation.x = 0
    tr.translation.y = 0
    tr.translation.z = 5
    #tr.rotation_center.z = 0.5
    texture = glutils.load_texture('grass.jpg')
    """m = Mesh()
    p0, p1, p2, p3 = [-largeur, 0, 0.5], [largeur/4, 0, 0.5], [largeur/4, 2, 0.5], [-largeur, 2, 0.5]
    n, c = [0, 1, 0], [1, 1, 1]
    # les coordonnes de textures
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)"""
    texture = glutils.load_texture('mur.jpg')
    points= [[-largeur, 0, 0.5], [largeur/4, 0, 0.5], [largeur/4, 2, 0.5], [-largeur, 2, 0.5], [-largeur, 0, 0.5], [largeur/4, 0, 0.5], [largeur/4, 2, 0.5], [-largeur, 2, 0.5]]
    obstacle = decors(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr ,0,0,0, points)
    viewer.add_object(obstacle) 

    viewer.run()




if __name__ == '__main__':
    main()