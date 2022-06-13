import glm
import math


class MVPController:
    def __init__(self, callback_update, width: int, height: int):
        self.callback_update = callback_update
        self.width = width
        self.height = height
        self.position = glm.vec3(-0.0878369,       1.3335,     -1.96448) #Initial position of camera
        self.pitch = -0.5
        self.yaw = 1.55 #-0.5
        self.roll = 0.0
        self.speed = 0.4
        self.mouse_speed = 0.01
        self.fov = 90
        self.calc_view_projection()

    def calc_mvp(self, model_matrix=glm.mat4(1.0)):
        return self.projection_matrix * self.view_matrix * model_matrix

    def calc_view_projection(self):
        #self.direction = glm.vec3(-1, -1, 2)

        #We create a direction vector based on the formula
        #found at the link provided from the instructions      
        x = math.cos(self.yaw) * math.cos(self.pitch)
        y = math.sin(self.pitch)
        z = math.sin(self.yaw) * math.cos(self.pitch)
        self.direction = glm.normalize(glm.vec3(x,y,z));
 
        #self.right = glm.vec3(0, 1, 0)
        #right vector = normalized cross product between an up vector and direction vector
        self.right = glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.direction))

        #self.up = glm.vec3(0, -1, 0)
        #up vector = cross product between direction vector and right vector
        self.up = glm.cross(self.direction, self.right)

        self.view_matrix = glm.lookAt(self.position,
                          self.position + self.direction,
                          self.up)
        
        self.projection_matrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000)

    def on_keyboard(self, key: bytes, x: int, y: int):
        #We check if any key from w,a,s,d,e,r is pressed and change the position accordingly(we are using the speed provided at init)
        #Note that in each case we make the opposite transformation comparing to our movement. For example, if camera is going to move left
        #the object is going to move right.
        #Forward
        if (key == bytes("w","utf-8") or key == bytes("W","utf-8")):
            self.position += self.speed * self.direction
        #Backward
        if (key == bytes("s","utf-8") or key == bytes("S","utf-8")):
            self.position -= self.speed * self.direction
        #Left
        if (key == bytes("a","utf-8") or key == bytes("A","utf-8")):
            self.position -= glm.normalize(glm.cross(self.direction, self.up)) * self.speed
        #Right
        if (key == bytes("d","utf-8") or key == bytes("D","utf-8")):
            self.position += glm.normalize(glm.cross(self.direction, self.up)) * self.speed
        #Up
        if (key == bytes("e","utf-8") or key == bytes("E","utf-8")):
            self.position -= self.speed * self.up
        #Down
        if (key == bytes("r","utf-8") or key == bytes("R","utf-8")):
            self.position += self.speed * self.up

        self.calc_view_projection()
        self.callback_update()

    def on_mouse(self, key: int, up: int, x: int, y: int):
        if key == 0 and up == 0:
            self.last_x = x
            self.last_y = y

    def on_mousemove(self, x: int, y: int):
        x_diff = self.last_x - x
        y_diff = self.last_y - y
        self.last_x = x
        self.last_y = y
        #Previously was:
        #self.yaw -= y_diff * self.mouse_speed
        #self.pitch -= x_diff * self.mouse_speed
        self.yaw -= x_diff * self.mouse_speed
        self.pitch -= y_diff * self.mouse_speed
        self.calc_view_projection()
        self.callback_update()

    def on_special_key(self, *args):
        pass

