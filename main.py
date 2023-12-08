from PIL import Image
import numpy as np
from collections import deque
import heapq

# Get Pixels next to current pixel
def getAdjacentPixels(shape, pixel):
    x, y = pixel
    AdjacentPixels = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    # Check that x and y are in the range of the image
    return [(x_prime, y_prime) for x_prime, y_prime in AdjacentPixels if 0 <= x_prime < shape[0] and 0 <= y_prime < shape[1]]

# Check if pixel is part of maze or if pixel is a wall
def isFreePixel(I, pixel):
    if all(I[pixel] == [255,255,255,255]):
        return True
    return False

# Mark Shortest Path as red
def mark_path(image, path):
    for pixel in path:
        image[pixel] = [255, 0, 0, 255]

# Mark all visited pixels as green
def mark_visited(image, visited):
    for pixel in visited:
        image[pixel] = [0, 255, 0, 255]

# Breadth-First-Search to find shortest path in the maze
def bfs(I, s, t):
    # get the size of the image in the form [x,y]
    shape = I.shape[:2]

    # Initialize empty set for visited pixels
    visited = set()
    
    # Initialize queue with starting state
    queue = deque([(s, [s])])

    # While queue not empty, search
    while queue:
        current, path = queue.popleft()
        visited.add(current)

        # if we have reached the destniation return the shortest path and all visted pixels
        if current == t:
            return path, visited
        
        # Get the Adjacent Pixels, if valid search
        next = getAdjacentPixels(shape, current)
        for pixel in next:
            if pixel not in visited and isFreePixel(I, pixel):
                queue.append((pixel, path + [pixel]))
                visited.add(pixel)
    
    # No path was found
    return None, None

def BestFirstSearch(I, s, t):
    # get the size of the image in the form [x,y]
    shape = I.shape[:2]

    # Initialize empty set for visited pixels
    visited = set()
    
    # Initialize queue with starting state
    priority_queue = [(0, s, s)]

    # While queue not empty, search
    while priority_queue:
        priority, current, path = heapq.heappop(priority_queue)
        visited.add(current)

        # if we have reached the destniation return the shortest path and all visted pixels
        if current == t:
            return path, visited
        
        # Get the Adjacent Pixels, if valid search
        next = getAdjacentPixels(shape, current)
        for pixel in next:
            if pixel not in visited and isFreePixel(I, pixel):
                # ERROR HERE. Then maybe just maybe...
                heapq.heappush(priority_queue(priority, pixel, path + [pixel]))
                visited.add(pixel)
    
    # No path was found
    return None, None


def main():
    #filename = input("Enter the name of the maze file:")
    
    # x1 = input("Enter an integer to be used as the x coordinate for the starting location: ")
    # y1 = input("Enter an integer to be used as the y coordinate for the starting location: ")
    # s = (int(x1), int(y1))

    # x2 = input("Enter an integer to be used as the x coordinate for the destination: ")
    # y2 = input("Enter an integer to be used as the y coordinate for the destination: ")
    # t = (int(x2), int(y2))
    
    breadth_file = "test_maze.bmp"
    s = (11, 11) # start coords that work for test_maze.bmp and test_maze1.bmp
    t = (395,395) # Goal coords that work for test_maze.bmp and test_maze1.bmp

    best_file = "test_maze.bmp"
    best_s = (11, 11) # start coords that work for test_maze.bmp and test_maze1.bmp
    best_t = (395,395) # Goal coords that work for test_maze.bmp and test_maze1.bmp


    im = Image.open(breadth_file)
    maze = np.array(im)

    if not isFreePixel(maze, s):
        print("Starting Location is not a valid pixel")
        exit(1)
    
    if not isFreePixel(maze, t):
        print("Destination is not a valid pixel")
        exit(1)

    path, visited = bfs(maze, s, t)

    if path:
        mark_visited(maze, visited)
        mark_path(maze, path)
        Image.fromarray(maze.astype(np.uint8)).save("solved_maze.bmp")
    else:
        print("No Path Found")

    # Best First Search
    best_im = Image.open(best_file)
    best_maze = np.array(best_im)
    
    best_path, best_visited = BestFirstSearch(best_maze, best_s, best_t)

    if path:
        mark_visited(best_maze, best_visited)
        mark_path(best_maze, best_path)
        Image.fromarray(best_maze.astype(np.uint8)).save("best_solved.bmp")
    else:
        print("No Path Found")



main()