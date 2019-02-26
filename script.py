from random import randint

def build_maze(m, n, swag):
  grid = [['wall' for column in range(n)] for row in range(m)]

  start_i = randint(0, m-1)
  start_j = randint(0, n-1)

  grid[start_i][start_j] = "start"
  mow(grid, start_i, start_j)
  explore_maze(grid, start_i, start_j, swag)
  return grid

def print_maze(grid):
  for row in grid:
    printable_row = ""
    for cell in row:
      if cell == 'wall':
        char = '|'
      elif cell == 'start':
        char = 'x'
      elif cell == 'empty':
        char = ' '
      else:
        char = cell[0]
      printable_row += char
    print(printable_row)

def mow(grid, i, j):
  directions = ["U","D","L","R"]
  while directions:
    directions_index = randint(0, len(directions)-1)
    direction = directions.pop(directions_index)
    if direction == 'U':
      if i - 2 < 0:
        continue
      elif grid[i - 2][j] == 'wall':
        grid[i - 2][j] = 'empty'
        grid[i - 1][j] = 'empty'
        mow(grid, i - 2, j)
    elif direction == 'D':
      if i + 2 >= len(grid):
        continue
      elif grid[i + 2][j] == 'wall':
        grid[i + 2][j] = 'empty'
        grid[i + 1][j] = 'empty'
        mow(grid, i + 2, j)
    elif direction == 'L':
      if j - 2 < 0:
        continue
      elif grid[i][j-2] == 'wall':
        grid[i][j-2] = 'empty'
        grid[i][j-1] = 'empty'
        mow(grid, i, j - 2)
    else:
      if j + 2 >= len(grid[0]):
        continue
      elif grid[i][j+2] == 'wall':
        grid[i][j+2] = 'empty'
        grid[i][j+1] = 'empty'
        mow(grid, i, j + 2)

def explore_maze(grid, start_i, start_j, swag):
  grid_copy = [row[:] for row in grid]
  bfs_queue = [[start_i, start_j]]
  directions = ["U","D","L","R"]
  while bfs_queue:
    i, j = bfs_queue.pop(0)
    if grid[i][j] != 'start' and randint(1, 10) == 1:
      grid[i][j] = swag[randint(0,len(swag) - 1)]
    grid_copy[i][j] = 'visited'

    for direction in directions:
      explore_i = i
      explore_j = j
      if direction == "U":
        explore_i = i - 1
      elif direction == "D":
        explore_i = i + 1
      elif direction == "L":
        explore_j = j - 1
      else:
        explore_j = j + 1

      if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
        continue
      elif grid[explore_i][explore_j] != 'wall' and grid_copy[explore_i][explore_j] != 'visited':
        bfs_queue.append([explore_i, explore_j])
  grid[i][j] = "end"

#own Capstone project code starts here
def solve_maze(grid):
  graph = make_graph(grid)
  path = bfs(graph[0], graph[1], graph[2])
  swag = track_and_pickup(path, grid)[0]
  print_maze(track_and_pickup(path,grid)[1])
  print(swag)

#Function for extracting a graph from the maze
def make_graph(grid):
  #Grid overlay for naming each cell of the original grid
  numbered_grid = []
  tracker = 0
  for row in grid:
    lst = []
    for cell in row:
      lst.append(tracker)
      tracker += 1
    numbered_grid.append(lst)

  #finding the start and end point of the maze
  i = 0
  for row in grid:
    j = 0
    for cell in row:
      if cell == 'start':
        start = numbered_grid[i][j]
      if cell == 'end':
        end = numbered_grid[i][j]
      j += 1
    i += 1

  #making a graph represantation of the maze
  graph = {node_label: [] for (node_label) in range(len(grid) * len(grid[0]))}
  node_label = 0
  i = 0
  for row in grid:
    j = 0
    for cell in row:
      if cell != "wall":
        if i - 1 >= 0:
          if grid[i-1][j] != 'wall':
              graph[node_label].append(numbered_grid[i-1][j])
        if i + 1 <= len(grid) - 1:
          if grid[i+1][j] != 'wall':
              graph[node_label].append(numbered_grid[i+1][j])
        if j - 1 >= 0:
          if grid[i][j-1] != 'wall':
              graph[node_label].append(numbered_grid[i][j-1])
        if j + 1 <= len(grid[0]) - 1:
          if grid[i][j+1] != 'wall':
              graph[node_label].append(numbered_grid[i][j+1])

      j += 1
      node_label += 1
    i += 1
  return graph, start, end

#BFS implementation
def bfs(graph, start_vertex, target_value):
  path = [start_vertex]
  vertex_and_path = [start_vertex, path]
  bfs_queue = [vertex_and_path]
  visited = set()
  while bfs_queue:
    current_vertex, path = bfs_queue.pop(0)
    visited.add(current_vertex)
    for neighbor in graph[current_vertex]:
      if neighbor not in visited:
        if neighbor is target_value:
          return path + [neighbor]
        else:
          bfs_queue.append([neighbor, path + [neighbor]])

#Function for preparing a visual representation of the solution and collect the swag items
def track_and_pickup(path, grid):
    #Yep. The numbered grid again...
    numbered_grid = []
    tracker = 0
    for row in grid:
      lst = []
      for cell in row:
        lst.append(tracker)
        tracker += 1
      numbered_grid.append(lst)

    #Collecting swag and 'dotting' our path
    swag_list = []
    i = 0
    for row in grid:
      j = 0
      for cell in row:
        if cell != 'wall' and cell != 'empty' and cell != 'start' and cell != 'end' and numbered_grid[i][j] in path:
          swag_list.append(grid[i][j])
        if cell != 'wall' and cell != 'start' and cell != 'end' and numbered_grid[i][j] in path:
          grid[i][j] = '.'
        j += 1
      i += 1
    return(swag_list, grid)




amazing_maze = build_maze(25,25, swag=['candy corn', 'werewolf', 'pumpkin'])
print("You'll never escape, He-Man!")
print_maze(amazing_maze)
print('Ha, Skeletor! I escaped. I made a map for all your future victims to use. I also looted your dungeon. Here is a list, so you can check your inventory. Best, He-man \nP.S.: Computer skills ARE the super power of the 21st century.')
solve_maze(amazing_maze)
