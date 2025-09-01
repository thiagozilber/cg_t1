import OpenGL.GL as gl
import OpenGL.GLUT as glut
from math import sqrt, cos, sin

class World:
    class Entity:
        def __init__(self, id):
            self.id = id
            self.frame_info = []
            self.trail = []
            self.index = 0
            self.x = 0
            self.y = 0
            self.color = (1.0, 1.0, 1.0)
            self.alpha = 1.0
            self.radius = 0.1
            
        def update_entity(self):
            x, y = self.get_next_frame()
            self.x = x
            self.y = y
            
        def draw_self(self):
            gl.glPushMatrix()
            gl.glTranslatef(0, 0, 0)
            gl.glColor3f(*self.color)
            gl.glBegin(gl.GL_TRIANGLE_FAN)
            gl.glVertex2f(self.x, self.y)  # Center of the circle
            for i in range(361):  # 360 degrees + 1 to close the circle
                angle = i * 3.14159 / 180  # Convert degrees to radians
                gl.glVertex2f(self.radius * cos(angle), self.radius * sin(angle))
            gl.glEnd()
            gl.glPopMatrix()
            
        def get_next_frame(self):
            if self.index < len(self.frame_info):
                self.x, self.y, trash = self.frame_info[self.index]
                self.index += 1
                return self.x, self.y
            return -1, -1
    
    def __init__(self, filename, w, h):
        self.entities = []
        self.frame, self.frame_limit = 0, 0
        self.w, self.h = w, h
        self.max_dist = sqrt(self.w**2 + self.h**2)
        self.bg_color = (1.0, 1.0, 1.0)
        self.read_dataset(filename)

    def read_dataset(self, filename):
    #This function will create n entities = to the number of newlines in the text file and then populate each entity's self.frame_info with the (x, y, frame_num) data
        with open(filename, 'r') as file:
            trash = file.readline() # skip header
            id_counter = 0
            for line in file:
                entity = self.Entity(id_counter)
                id_counter += 1
                pos = line.index('\t')
                line = line[pos+1:-1] # skip first number
                line = line.strip()
                line = line.replace(')', ';')
                line = line.replace('(', '')
                line = line.split(';')
                for entry in line:
                    parts = entry.split(',')
                    if len(parts) == 3:
                        x, y, frame = map(int, parts)
                        entity.frame_info.append((x, y, frame))
                self.entities.append(entity)
        for entity in self.entities:
            if self.frame_limit < entity.frame_info[-1][2]:
                self.frame_limit = entity.frame_info[-1][2]
    
    def calculate_proximity(self, entity):
        closest = None
        for other in self.entities:
            if other.id != entity.id:
                dist = ((entity.x - other.x) ** 2 + (entity.y - other.y) ** 2) ** 0.5
                if closest is None or dist < closest:
                    closest = dist
        return closest
    
    def normalize(self, dist):
        return 1 - (dist / self.max_dist) # 1 - (dist / max_dist) = 0 quando dist == max_dist, e vice versa
        # 1 - (etc) pq a proporção que eu quero é inversa

    def handle_proximity(self, entity, dist):
        norm = self.normalize(dist)
        entity.color = (norm, norm, norm)

    def update(self):
        for entity in self.entities:
            entity.update_entity()
            self.handle_proximity(entity, self.calculate_proximity(entity)) # calcula a proximidade e atualiza a cor
        self.frame += 1
        if self.frame >= self.frame_limit:
            for entity in self.entities:
                entity.index = 0
                entity.color = (0.0, 0.0, 0.0)
            self.frame = 0

def main():
    world = World("Paths_D.txt", 800, 600)
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(world.w, world.h)
    glut.glutCreateWindow(b"Entity Visualization")
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glClearColor(*world.bg_color, 1.0)
    def display():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        for entity in world.entities:
            entity.draw_self()
        glut.glutSwapBuffers()
    def idle():
        world.update()
        glut.glutPostRedisplay()
    glut.glutDisplayFunc(display)
    glut.glutIdleFunc(idle)
    glut.glutMainLoop()
if __name__ == "__main__":
    main()
