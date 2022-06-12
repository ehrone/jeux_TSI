import OpenGL.GL as GL
import pyrr, time
import numpy as np 
import sympy as s

class Transformation3D: 
    def __init__(self, euler = pyrr.euler.create(), center = pyrr.Vector3(), translation = pyrr.Vector3()):
        # un tableau qui stocke les angles specifiques de euler
        self.rotation_euler = euler.copy()
        # une cipie d'un vecteur en 3 dim
        self.rotation_center = center.copy()
        # une cipie d'un vecteur en 3 dim
        self.translation = translation.copy()

class Object:
    def __init__(self, vao, nb_triangle, program, texture):
        self.vao = vao
        self.nb_triangle = nb_triangle
        self.program = program
        self.texture = texture
        self.visible = True


    def draw(self):
        if self.visible : 
            GL.glUseProgram(self.program)
            GL.glBindVertexArray(self.vao)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
            GL.glDrawElements(GL.GL_TRIANGLES, 3*self.nb_triangle, GL.GL_UNSIGNED_INT, None)
            GL.glUseProgram(self.program)





class Object3D(Object):
    def __init__(self, vao, nb_triangle, program, texture, transformation, z,longeur, largeur, points, centre):
        super().__init__(vao, nb_triangle, program, texture)
        self.transformation = transformation
        # booléen qui permet de faire sauter l'objet
        self.saut = False
        # perùmet de passer de la phase de montée a la phase de descente dans le saut
        self.counter = 2
        # le PFD de l'objet
        # les forces crées par les saut où les collisions
        self.forces = 0
        # les forces qui servent a simuler la gravité
        self.pesanteur = 0
        self.reactance = 0
        self.vel = -0.3
        #repop de la plateforme
        self.z = z
        self.z_init = z
        #self.z = 0
        self.longeur = longeur
        self.largeur = largeur

        self.__points = points
        self.hitbox = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        self.centre = centre
        self.delta_x = -1
        self.delta_y = 1
        self.delta_z = 1


    def update_center(self):
        self.centre = [self.transformation.translation.x, self.transformation.translation.y, self.transformation.translation.z]

    def update_hitbox(self):
        i=0
        for point in self.__points:
            x = self.transformation.translation.x + point[0]
            y = self.transformation.translation.y + point[1]
            z = self.transformation.translation.z + point[2]
            self.hitbox[i] = [x, y, z]
            i +=1

    def collision(self, obj):

        obj.update_center()
        self.update_center()
        
        x = [self.centre[0], self.centre[0]+self.delta_x]
        y = [self.centre[1], self.centre[1]+self.delta_y] # 0 : point bas , 1 : point haut
        z = [self.centre[2], self.centre[2]+self.delta_z] # 0 : point arrière, 1 : point avant

        x_obstacle = [obj.centre[0], obj.centre[0]+obj.delta_x]
        y_obstacle = [obj.centre[1], obj.centre[1]+obj.delta_y]
        z_obstacle = [obj.centre[2], obj.centre[2]+obj.delta_z]

        print(' joueur : ', x)
        print(' obstacle : ', x_obstacle)
        
        if (x[0] >= x_obstacle[0] and x[0]<= x_obstacle[1]) or (x[0] <= x_obstacle[0] and x[0]>= x_obstacle[1]) or (x[1] >= x_obstacle[0] and x[1]<= x_obstacle[1]) or (x[1] <= x_obstacle[0] and x[1]>= x_obstacle[1]) :# on regarde si il y a collision sur les x
            print(" coin : x sur l'obstacle ")
            if (float(z[0])>= z_obstacle[0] and z[0]<= z_obstacle[1]) or (z[1]>= z_obstacle[0] and z[1]<= z_obstacle[1]) :
                print(" collision ")
           


    def re_init_saut(self):
        # on vient de finir la phase de saut, on réinitialise le compteur
        if self.saut== False:
            self.counter = 2
            self.forces = 0 

    def action_saut(self):
        if self.saut == True :
            #print(self.objs[0].counter)

            #phase montante du saut
            if self.counter > 0 :
                #print(' saut montée')
                self.forces = (self.counter/2)**2
                #print((self.objs[0].counter/2)**2)
                self.counter -=1
                                     
            # on a fini la phase de descente du saut
            elif self.counter == -3:
                self.saut = False 
                self.re_init_saut()
                #print('fin de saut')

            # phase de détente du saut
            elif self.counter <= 0: 
                self.forces = -(self.counter/2)**2
                self.counter -=1
                #print(' saut descente')

            delta = self.forces + self.pesanteur+ self.reactance
            # on applique la translation à l'objet
            self.transformation.translation +=\
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler), pyrr.Vector3([0, delta, 0]))
            time.sleep(0.02)
    
    def move(self):
        # on modifit la position de l'objet du décors pyrr.vecteur3d(le tableau)
        # la variable qui indiquer a combien derriere le cube le tuile passée se met derrière l'actuelle
        seuil = 2
        # on fait avancer la platforme normaleent, on car on est pas encore au bout
        if self.z >= -(self.longeur+seuil):
            self.transformation.translation +=\
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler), pyrr.Vector3([0, 0, self.vel]))
            self.z += self.vel
        
        # on est arrivé en bout de platforme, donc on la fait réapparaitre derrière la deuxiéme
        else :
            # la dalle est maintenant derrière le cube, donc pour la mettre à la suite de la deuzième dalle 
            # il faut translater de 2*longeur et il faut aussi prendre en compte le déplacemlent qui est continu
            self.transformation.translation +=\
            pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler), pyrr.Vector3([0, 0, self.longeur*2-self.vel]))
            # on réinitialise la position de départ de la dale de sol
            self.z = self.longeur
            
    def draw(self):
        GL.glUseProgram(self.program)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "translation_model")

        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_model")
        # Modifie la variable pour le programme courant
        translation = self.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "rotation_center_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_model")
        # Modifie la variable pour le programme courant
        rotation_center = self.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(self.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(self.program, "rotation_model")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_model")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)

        super().draw()


# Cette classe est utilisé pou créer les obstacles
class decors(Object3D):
    def __init__(self, vao, nb_triangle, program, texture, transformation,z, longeur, largeur, points, centre):
        super().__init__(vao, nb_triangle, program, texture,transformation,z,longeur,largeur,points, centre)
        self.transformation = transformation 
        self.vel = -0.3
        self.x = 0
        self.longeur = longeur
        self.largeur = largeur
        self.delta_x = -2
        self.delta_y =1
        self.delta_z = 1

    def move(self):
        self.transformation.translation +=\
        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler), pyrr.Vector3([0, 0, self.vel]))
        self.x += self.vel

class Camera:
    def __init__(self, transformation = Transformation3D(translation=pyrr.Vector3([0, 1, 0], dtype='float32')), projection = pyrr.matrix44.create_perspective_projection(60, 1, 0.01, 100)):
        self.transformation = transformation
        self.projection = projection

class Text(Object):
    def __init__(self, value, bottomLeft, topRight, vao, nb_triangle, program, texture):
        self.value = value
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        super().__init__(vao, nb_triangle, program, texture)

    def draw(self):
        GL.glUseProgram(self.program)
        GL.glDisable(GL.GL_DEPTH_TEST)
        size = self.topRight-self.bottomLeft
        size[0] /= len(self.value)
        loc = GL.glGetUniformLocation(self.program, "size")
        if (loc == -1) :
            print("Pas de variable uniforme : size")
        GL.glUniform2f(loc, size[0], size[1])
        GL.glBindVertexArray(self.vao)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        for idx, c in enumerate(self.value):
            loc = GL.glGetUniformLocation(self.program, "start")
            if (loc == -1) :
                print("Pas de variable uniforme : start")
            GL.glUniform2f(loc, self.bottomLeft[0]+idx*size[0], self.bottomLeft[1])

            loc = GL.glGetUniformLocation(self.program, "c")
            if (loc == -1) :
                print("Pas de variable uniforme : c")
            GL.glUniform1i(loc, np.array(ord(c), np.int32))

            GL.glDrawElements(GL.GL_TRIANGLES, 3*2, GL.GL_UNSIGNED_INT, None)
        GL.glEnable(GL.GL_DEPTH_TEST)

    @staticmethod
    def initalize_geometry():
        p0, p1, p2, p3 = [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]
        geometrie = np.array([p0+p1+p2+p3], np.float32)
        index = np.array([[0, 1, 2]+[0, 2, 3]], np.uint32)
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, geometrie, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        vboi = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)
        return vao

