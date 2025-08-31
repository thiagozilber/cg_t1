import OpenGL.GL as gl
import OpenGL.GLUT as glut

class Entity:
    def __init__(self, id):
        self.id = id
        self.frame_info = []
        self.x = 0
        self.y = 0
        self.color = (1.0, 1.0, 1.0)
        self.radius = 1.0
        
    def update_entity(self):
        x, y = self.get_next_frame()
        self.x = x
        self.y = y
        self.handle_proximity(self.calculate_proximity())
        
    def draw_self(self):
        gl.push_matrix()
        gl.translatef(self.x, self.y, 0)
        gl.color3f(*self.color)
        glut.solid_sphere(self.radius, 20, 20)
        gl.pop_matrix()


def read_dataset(filename):
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
                    entity = Entity(len(entities))
                    entity.frame_info.append((x, y, frame_num))
                    entities.append(entity)
    return entities

def main():
    dataset = read_dataset("dataset.txt")
    for entity in dataset:
        print(f"Entity {entity.id}:")
        for frame in entity.frame_info:
            print(f"  Frame {frame[2]}: Position ({frame[0]}, {frame[1]})")
