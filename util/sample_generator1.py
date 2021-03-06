# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
# import sys
# sys.path.append("../adventure")
# from models import Room
import random 

class Room:

    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
        self.num_connects=0

    def __repr__(self):
        #if self.e_to is not None:
        #    return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        #return f"({self.x}, {self.y})"
        # Above commented lines are the reference repr
        base = "ID:{}".format(self.id)
        if self.e_to is not None:
            base += ",E({},{})".format(self.e_to.x, self.e_to.y)
        if self.w_to is not None:
            base += ",W({},{})".format(self.w_to.x, self.w_to.y)
        if self.n_to is not None:
            base += ",N({},{})".format(self.n_to.x, self.n_to.y)
        if self.s_to is not None:
            base += ",S({},{})".format(self.s_to.x, self.s_to.y)
        base += " "
        return base

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
        self.num_connects += 1
        connecting_room.num_connects += 1
        print("Room id {}, connection: {}".format(self.id, connecting_room))
        print("room id:{} now has {} connections".format(self.id,self.num_connects))

    # delete a connection in a specific direction
    # deletes connection for both this and connected room
    # also decrements number of connections for both
    def delete_connection(self, direction):
        '''
        Delete a connection in a particular direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}

        connected_room = self.get_room_in_direction(direction)
        setattr(self, f"{direction}_to", None)
        self.num_connects -= 1
        #print("Room id: {}, deleted connection in direction {}, number of connections: {}".format(self.id, direction, self.num_connects))
        reverse_dir = reverse_dirs[direction]
        setattr(connected_room, f"{reverse_dir}_to", None)
        connected_room.num_connects -= 1
        #print("Room id: {}, deleted connection in direction {}, number of connections: {}".format(connected_room.id, reverse_dir, connected_room.num_connects))



    # Prune the connections for one room - 2nd implementation
    # pick one random direction in which to keep the connection
    # delete the rest
    # wont delete connection if room on other side has just one
    # since this would make room on other side an orphan (no connections)
    def prune_connections2(self):



    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:

    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1

            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                # if not single_connect or not room.num_connects:
                previous_room.connect_rooms(room, room_direction)
                room_below = self.grid[y - 1][x]
                #if room_below and room_below.x % 2 == 0:
                if room_below and random.randint(1,10) % 2 == 0:
                    room_below.connect_rooms(room, 'n')


            # Update iteration variables
            previous_room = room

            room_count += 1
            print(f'room count:{room_count}, previous_room: {previous_room}')

        if (room_count == num_rooms-1):
            previous_room.connect_rooms(room, room_direction)
            print(f'room count:{room_count}, previous_room: {previous_room}')            


    # Randomly pick rooms from grid
    # and restrict to just one connection
    def refine_rooms(self):
        print("Pruning room connections...")
        for i in range(0,self.height):
            for j in range(0,self.width):
                if random.randint(0,5) == 1:
                    self.grid[j][i].prune_connections2()


    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
w.print_rooms()
w.refine_rooms()
print("\n")
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
