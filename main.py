from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text, decors
import numpy as np
import OpenGL.GL as GL
import pyrr
import time

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

    """"
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('Bob le', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_text(o)
    o = Text('Cube', np.array([-0.5, -0.2], np.float32), np.array([0.5, 0.3], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_text(o)
    """

    viewer.run()


if __name__ == '__main__':
    main()