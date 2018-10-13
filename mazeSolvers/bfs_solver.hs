-- @Author: ariesduanmu


maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 2, 2, 2, 2, 2, 2, 2, 0], 
        [0, 2, 0, 0, 0, 0, 0, 0, 0], 
        [0, 2, 2, 2, 0, 2, 2, 2, 0], 
        [0, 0, 0, 2, 0, 2, 0, 2, 0], 
        [0, 2, 2, 2, 0, 2, 0, 2, 0], 
        [0, 2, 0, 0, 0, 2, 0, 2, 0], 
        [0, 2, 2, 2, 2, 2, 0, 2, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
start = (7, 7)
end = (1, 7)

validPosition x y maze = (x >= 0) && (y >= 0) && (length maze) > y && (length (maze !! 0)) > x
getNode x y = if (validPosition x y maze) then Just ((maze !! y) !! x) else Nothing
getNeighborNode x y closed = filter (\(i, j) -> (getNode i j) == (Just 2) && (elem (i,j) closed) == False) [(x+a, y+b) | (a,b) <- [(0,-1),(0,1),(1,0),(-1,0)]]


bfsSolver ((i,j):xs) closed meta
    | ((i,j) /= end) = (bfsSolver (xs++neighbors) (closed++[(i,j)]) (meta++[((a,b), (i,j)) | (a,b)<-neighbors]))
    | otherwise = (constructPath (i,j) meta [])
    where neighbors = (getNeighborNode i j closed)


constructPath (i,j) meta route
    | (length points) > 0 = (constructPath (head points) meta (route++[(i,j)]))
    | otherwise = route++[(i,j)]
    where points = [(x,y) | ((a,b),(x,y)) <- meta, (a,b) == (i,j)]

-- bfsSolver [start] [] []