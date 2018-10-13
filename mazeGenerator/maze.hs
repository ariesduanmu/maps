import Data.Random


validPosition x y maze = (x >= 0) && (y >= 0) && (length maze) > y && (length (maze !! 0)) > x

getNode x y maze = if (validPosition x y maze) then Just ((maze !! y) !! x) else Nothing

validNeigborDirections x y maze = filter (\(i,j) -> (getNode (x+i) (y+j) maze) == (Just 1)) [(a, b) | (a,b)<-[(0,2),(0,-2),(2,0),(-2,0)]]

starts board = [(i,j) | i<-[1, (length board)-2], j<-[1, (length (board!!0))-2], ((board!!i)!!j)==1]

initboard (r,c) = [[if ((mod i 2) == 1) && ((mod j 2) == 1) then 1 else 0 | j<-[0..c-1]] | i<-[0..r-1]]


updateBoard (dx,dy) x y v board = [[if (matchCondition i j) then v else (board!!i)!!j | j <- [0..(length (board!!0))-1]] | i <- [0..(length board)-1]]
    where matchCondition i j =  ((x+dx,y+dy) == (i,j) || (x+(quot dx 2),y+(quot dy 2)) == (i,j))


generateMaze board route
    | ((length route) == 0) = board
    | otherwise = generateMaze next_board next_route
    where
        (x, y) = route!!((length route) - 1)
        available_direction = (validNeigborDirections x y board)
        (dx, dy) = head available_direction
        popedRoute = [route!!a | a <- [0..(length route)-2]]
        next_board = if (length available_direction) > 0 then (updateBoard (dx,dy) x y 2 board) else board
        next_route = if (length available_direction) > 0 then (popedRoute++[((x+dx), (y+dy))]) else popedRoute

maze 0 0 = []
maze h w = generateMaze board [head (starts board)]
    where board = initboard (h,w)

