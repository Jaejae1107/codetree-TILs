import sys
from copy import deepcopy
from collections import deque



# Constants for directions (right, left, down, up)
di, dj = [0, 0, 1, -1], [1, -1, 0, 0]

# Read input
K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
w = list(map(int, input().split()))
walls = deque(w)

# Function to perform BFS for clearing blocks
def bfs(bi, bj, visit, num, b_arr):
    q = deque()
    q.append((bi, bj))
    r = [(bi, bj)]
    while q:
        si, sj = q.popleft()
        for d in range(4):
            ni, nj = si + di[d], sj + dj[d]
            if 0 <= ni < 5 and 0 <= nj < 5 and not visit[ni][nj] and b_arr[ni][nj] == num:
                q.append((ni, nj))
                r.append((ni, nj))
                visit[ni][nj] = True

    if len(r) >= 3:
        return len(r), r
    else:
        return 0, []

# Function to gain score by clearing blocks
def gain_score(g_arr):
    visited = [[False] * 5 for _ in range(5)]
    temp_ans = 0
    temp_r = []
    for gi in range(5):
        for gj in range(5):
            if not visited[gi][gj]:
                visited[gi][gj] = True
                a, r = bfs(gi, gj, visited, g_arr[gi][gj], g_arr)
                if a > 0:
                    temp_r.extend(r)
                    temp_ans += a
    return temp_ans, temp_r

# Function to fill blocks from the wall queue
def fill_block(new_arr, route):
    route.sort(key=lambda x: (x[1], -x[0]))
    for fi, fj in route:
        if walls:
            val = walls.popleft()
            new_arr[fi][fj] = val
    return new_arr

# Function to perform 3x3 sub-grid rotation
def rotate(y, x, pan):
    hey = deepcopy(pan)
    hey[y + 1][x - 1] = pan[y + 1][x + 1]
    hey[y - 1][x - 1] = pan[y + 1][x - 1]
    hey[y - 1][x + 1] = pan[y - 1][x - 1]
    hey[y + 1][x + 1] = pan[y - 1][x + 1]
    hey[y][x + 1] = pan[y - 1][x]
    hey[y + 1][x] = pan[y][x + 1]
    hey[y][x - 1] = pan[y + 1][x]
    hey[y - 1][x] = pan[y][x - 1]
    return hey

# Main explore function to find the best rotation
def explore():
    global arr
    max_cnt = 0
    best_center = (0, 0)
    best_rotate = 3
    best_route = []
    best_arr = []

    for i in range(1, 4):
        for j in range(1, 4):
            temp_arr = deepcopy(arr)
            before_rotate = [row[j-1:j+2] for row in arr[i-1:i+2]]
            for rot in range(4):
                after_rotate = list(map(list, zip(*before_rotate[::-1])))
                before_rotate = deepcopy(after_rotate)
                r = 0
                for ai in range(i-1, i+2):
                    temp_arr[ai][j-1:j+2] = after_rotate[r]
                    r += 1

                cnt, temp_route = gain_score(temp_arr)
                if cnt > max_cnt or (cnt == max_cnt and (rot < best_rotate or (rot == best_rotate and (j < best_center[1] or (j == best_center[1] and i < best_center[0]))))):
                    max_cnt = cnt
                    best_center = (i, j)
                    best_rotate = rot
                    best_route = temp_route
                    best_arr = deepcopy(temp_arr)

    if max_cnt == 0:
        return -1
    else:
        arr = deepcopy(best_arr)
        while True:
            arr = fill_block(arr, best_route)
            cnt, temp_route = gain_score(arr)
            if cnt > 0:
                max_cnt += cnt
                best_route = temp_route
            else:
                break
        return max_cnt

# Main loop for each K turns
realans = []
for _ in range(K):
    score = explore()
    if score == -1:
        break
    else:
        realans.append(score)

print(*realans)