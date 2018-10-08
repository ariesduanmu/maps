-- I am noy quite understand this question...
-- So I will just do a maze as what I thought to be
-- so my maze will like this

-- Node (Position_row, Position_column) 0 => Rock
--                                      1 => Not Rock


-- type Node = ((Int, Int), Int)
type Node = Int
type Maze = [[Node]]

validPosition x y maze = (x >= 0) && (y >= 0) && (length maze) > y && (length (maze !! 0)) > x

getNode x y maze = if (validPosition x y maze) then Just ((maze !! y) !! x) else Nothing

-- fuck this '()' in getNode (x+a) (y+b) maze
getNeighborNode x y maze = filter (Nothing /=) [getNode (x+a) (y+b) maze | (a,b) <- [(0,-1),(0,1),(1,0),(-1,0)]]

