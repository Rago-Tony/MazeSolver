from PIL import Image
import numpy as np
from collections import deque
from queue import PriorityQueue

# Get Pixels next to current pixel
def getAdjacentPixels(shape, pixel):
    x, y = pixel
    AdjacentPixels = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    # Check that x and y are in the range of the image
    return [(x_prime, y_prime) for x_prime, y_prime in AdjacentPixels if 0 <= x_prime < shape[0] and 0 <= y_prime < shape[1]]

# Check if pixel is part of maze or if pixel is a wall
def isFreePixel(I, pixel):
    if all(I[pixel] >= [200,200,200,200]):
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

def determinePriority(current, target):
    return abs(current[0] - target[0]) + abs(current[1] - target[1])

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
    
    # Initialize priority queue with starting state
    queue = PriorityQueue()
    queue.put((0, s, [s]))  # (priority, current, path)

    # While queue not empty, search
    while not queue.empty():
        priority, current, path = queue.get()
        visited.add(current)

        # if we have reached the destination return the shortest path and all visited pixels
        if current == t:
            return path, visited
        
        # Get the Adjacent Pixels, if valid search
        adjacent_pixels = getAdjacentPixels(shape, current)
        for pixel in adjacent_pixels:
            if pixel not in visited and isFreePixel(I, pixel):
                priority = determinePriority(pixel, t)  # Replace with your heuristic function
                queue.put((priority, pixel, path + [pixel]))
                visited.add(pixel)
    
    # No path was found
    return None, None

def main():
    filename = input("Enter the name of the maze file(i.e: maze.bmp):\n")
    print()

    breadth_file = filename
    best_file = filename

    s = input("Enter the starting coordinates (Enter the x and y values seperated by a comma i.e: 8,8):\n")
    print()
    s = tuple(int(x) for x in s.split(","))
    
    t = input("Enter the destination coordinates (Enter the x and y values seperated by a comma i.e: 190,202):\n")
    print()
    t = tuple(int(x) for x in t.split(","))

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
        Image.fromarray(maze.astype(np.uint8)).save("breadth_solved.bmp")
    else:
        print("Breadth First: No Path Found")
        exit(1)

    
    # Best First Search
    best_im = Image.open(best_file)
    best_maze = np.array(best_im)
    
    best_path, best_visited = BestFirstSearch(best_maze, s, t)

    if path:
        mark_visited(best_maze, best_visited)
        mark_path(best_maze, best_path)
        Image.fromarray(best_maze.astype(np.uint8)).save("best_solved.bmp")
    else:
        print("Best First: No Path Found")
        exit(1)
    
    print()
    print("Breadth First Output file: breadth_solved.bmp")
    print("Best First Output file: best_solved.bmp\n")


main()