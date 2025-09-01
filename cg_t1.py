import OpenGL.GL as gl
import OpenGL.GLUT as glut
class World:
    class Entity:
        def __init__(self, id):
            self.id = id
            self.frame_info = []
            self.index = 0
            self.x = 0
            self.y = 0
            self.color = (1.0, 1.0, 1.0)
            self.radius = 1.0
            
        def update_entity(self):
            x, y = self.get_next_frame()
            self.x = x
            self.y = y
            
        def draw_self(self):
            gl.push_matrix()
            gl.translatef(self.x, self.y, 0)
            gl.color3f(*self.color)
            glut.solid_sphere(self.radius, 20, 20)
            gl.pop_matrix()
            
        def get_next_frame(self):
            if self.index < len(self.frame_info):
                self.x, self.y = self.frame_info[self.index]
                self.index += 1
                return self.x, self.y
            return -1, -1
    
    def __init__(self, filename):
        self.entities = self.read_dataset(filename)
        self.frame = 0
        self.w, self.h = 800, 600
        self.bg_color = (0.0, 0.0, 0.0)

    def read_dataset(self, filename):
    #This function will create n entities = to the number of newlines in the text file and then populate each entity's self.frame_info with the (x, y, frame_num) data
        entities = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and line[0] != '[':
                    parts = line.split(',')
                    if len(parts) >= 3:
                        x = float(parts[0])
                        y = float(parts[1])
                        frame_num = int(parts[2])
                        entity = self.Entity(len(entities))
                        entity.frame_info.append((x, y, frame_num))
                        entities.append(entity)
        return entities
    
    def calculate_proximity(self, entity):
        closest = None
        for other in self.entities:
            if other.id != entity.id:
                dist = ((entity.x - other.x) ** 2 + (entity.y - other.y) ** 2) ** 0.5
                if closest is None or dist < closest[1]:
                    closest = (other.id, dist)
        return closest
    
    def handle_proximity(self, entity, closest):
        

def main():
    
