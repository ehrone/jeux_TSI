#!/usr/bin/env python3
import glutils
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
import time
import random as r
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text, decors

class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = [] # Le joueur et les plateformes
        self.obs = [] # Les obstacles
        self.txt = [] # Les textes
        self.touch = {}     

    def run(self):
        # boucle d'affichage

        ## teemps initial
        temps_init = time.time()
        #print("temps-init" + str(temps_init))


        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            ## on recup une valeur de temps et on test si on ajoute un mur
            d1 = time.time()
            #print("d1" + str(d1))
            dlt = r.randint(3,5)
            if d1 - temps_init > dlt:
                self.invocation()
                temps_init = time.time()
            self.update_key()
            for obj in self.objs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    # si on est pas le joueur on fait se déplacer l'objet (ce sont les obstacles qui se déplacent)
                    if self.objs.index(obj) != 0 :
                        obj.move()
                        #pass
                            
                    self.update_camera(obj.program)
                    # on appel la fonction de saut
                    obj.action_saut()
                obj.draw()

            for obj in self.obs:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                    obj.move()
                    self.objs[0].collision(obj, self.obs.index(obj))
                    #avec un if    obj.pop()  # ici on test si on est derriere le joueur pour retirer l'obstacle de la liste
                obj.draw()
                
            for obj in self.txt:
                GL.glUseProgram(obj.program)
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                    obj.draw()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action
    
    # Le joueur et les plateformes
    def add_object(self, obj):
        self.objs.append(obj)

    # Les obstacles
    def add_obstacle(self, obs):
        self.obs.append(obs)

    # Les textes
    def add_text(self, obs):
        self.txt.append(obs)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)

    def update_key(self):
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0.1, 0, 0]))
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([-0.1, 0, 0]))
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.1]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0].transformation.translation += \
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, -0.1]))
        
        # retirer le texte quand on veut lancer le jeu
        if glfw.KEY_ENTER in self.touch and self.touch[glfw.KEY_ENTER] > 0:
            self.txt.pop()
            self.txt.pop()

        # si on veut controler la caméra avec IJKL
        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1
        #if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
            #self.objs[0] c'est le dinausore

        # on rajoute le saut mais on fait un pfd avec la force de poussée qui va contre le poids, comme ça on crée une gravité et on fait juste varier la poussée
        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE ] > 0:
            # on va déclancher la fonction pour faire sauter le perso, qui est premier dans la liste des objets
            self.objs[0].saut = True

        # ici on déplace la caméra vace l'objet, pour qu'elle le suive
        # on la fait tourner de autant que l'on fait tourner l'objet

        self.cam.transformation.rotation_euler = self.objs[0].transformation.rotation_euler.copy() 
        self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += np.pi
        # on recentre la camera sur l'objet
        self.cam.transformation.rotation_center = self.objs[0].transformation.translation + self.objs[0].transformation.rotation_center
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 1, 10])
        self.cam.transformation.rotation_euler[pyrr.euler.index().roll] = 0.4
        self.cam.transformation.translation = self.objs[0].transformation.translation + pyrr.Vector3([0, 2, 5])

    ### Invocation des murs adverse
    # On avance selon z

    def invocation(self):
        program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
        #print("J'invoque !")
        m = Mesh.load_obj('obstacle.obj')
        #m.normalize()
        #m.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        tr = Transformation3D()
        x = r.randint(-5,5)
        tr.translation.x = x
        tr.translation.y = 0
        tr.translation.z = self.objs[0].centre[2] + 10 ### hitBox 
        #tr.rotation_center.z = 0.5
        texture = glutils.load_texture('grass.jpg')
        centre =[0+tr.translation.x , 0+tr.translation.y , 0+tr.translation.z]
        obstacle = decors(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr ,0,0,0, centre)
        self.add_obstacle(obstacle)
        #print("J'ai invoqué")