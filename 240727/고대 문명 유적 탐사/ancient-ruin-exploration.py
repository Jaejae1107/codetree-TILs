import sys
import copy
from collections import deque



K, M = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(5)]
piece = list(map(int, input().split()))

def bfs(i, j):
    global visited, chose
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    q = deque()
    q.append([i, j])
    visited[i][j] = True
    chose.append([i, j])
    cnt = 1
    while q:
        y, x = q.popleft()

        for k in range(4):
            ny = dy[k] + y
            nx = dx[k] + x
            if 0 <= ny < 5 and 0 <= nx < 5 and not visited[ny][nx] and pan[ny][nx] == pan[y][x] and pan[ny][nx] != 0:
                visited[ny][nx] = True
                chose.append([ny, nx])
                q.append([ny, nx])
                cnt += 1

    if cnt < 3:
        for _ in range(cnt):
            y, x = chose.pop()
            visited[y][x] = False


def bbfs(i, j):
    global visited, cchose
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    qqq = deque()
    qqq.append([i, j])
    visited[i][j] = True
    cchose.append([i, j])
    cnt = 1
    while qqq:
        y, x = qqq.popleft()

        for k in range(4):
            ny = dy[k] + y
            nx = dx[k] + x
            if 0 <= ny < 5 and 0 <= nx < 5 and not visited[ny][nx] and fpan[ny][nx] == fpan[y][x]:
                visited[ny][nx] = True
                cchose.append([ny, nx])
                qqq.append([ny, nx])
                cnt += 1

    if cnt < 3:
        for _ in range(cnt):
            y, x = cchose.pop()
            visited[y][x] = False


def rotate(y, x):
    hey = copy.deepcopy(pan)
    hey[y + 1][x - 1] = pan[y + 1][x + 1]
    hey[y - 1][x - 1] = pan[y + 1][x - 1]
    hey[y - 1][x + 1] = pan[y - 1][x - 1]
    hey[y + 1][x + 1] = pan[y - 1][x + 1]
    hey[y][x + 1] = pan[y - 1][x]
    hey[y + 1][x] = pan[y][x + 1]
    hey[y][x - 1] = pan[y + 1][x]
    hey[y - 1][x] = pan[y][x - 1]

    return hey


realans = []
for _ in range(K):
    final = []
    center = (0, 0)
    angle = -1
    ans = 0
    for i in range(1, 4):
        for j in range(1, 4):
            pan = copy.deepcopy(maze)
            for pp in range(3):
                pan = rotate(i, j)
                visited = [[False] * 5 for _ in range(5)]
                chose = []
                for q in range(5):
                    for w in range(5):
                        if not visited[q][w] and pan[q][w] != 0:
                            bfs(q, w)

                if len(chose) > len(final):
                    angle = pp
                    center = (i, j)
                    final = chose
                    fpan = copy.deepcopy(pan)
                elif len(chose) == len(final):
                    if pp < angle:
                        angle = pp
                        center = (i, j)
                        final = chose
                        fpan = copy.deepcopy(pan)
                    elif pp == angle:
                        yy, xx = center
                        if yy > i:
                            angle = pp
                            center = (i, j)
                            final = chose
                            fpan = copy.deepcopy(pan)
                        elif yy == i:
                            yy, xx = center
                            if xx > j:
                                angle = pp
                                center = (i, j)
                                final = chose
                                fpan = copy.deepcopy(pan)

  

    while True:
        ans += len(final)

        for i in final:
            y, x = i
            fpan[y][x] = 0



        for i in range(5):
            for j in range(4, -1, -1):
                if fpan[j][i] == 0:
                    if piece:
                        fpan[j][i] = piece.pop(0)

        visited = [[False] * 5 for _ in range(5)]
        cchose = []

        for q in range(5):
            for w in range(5):
                if not visited[q][w] and fpan[q][w] != 0:
                    bbfs(q, w)

        final = cchose

        if len(cchose) == 0:
            break

    maze = copy.deepcopy(fpan)
    if ans != 0:
        realans.append(ans)
    else:
        break

print(*realans)