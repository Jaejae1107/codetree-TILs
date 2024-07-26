import sys
import copy
from collections import deque


R,C,K =  map(int, input().split())

pan = [[0] * C for _ in range(R)]


def inside(y,x): #박스 안인지 체크.
    if 0 <= y < R and 0 <= x < C:
        return True
    return False
def check(y,x):
    if not inside(y,x): #앞으로 갈 수 있는지 체크
        if y < R and 0 <= x < C:
            return True
    else:
        if pan[y][x] == 0:
            return True
        else:
            return False
def move(c,d,non): # 골렘 이동
    y,x = -2, c
    while True: #아래로 최대한 움직임
        if check(y + 2, x) and check(y + 1, x - 1) and check(y + 1, x + 1):
            y += 1
        elif check(y, x - 2) and check(y + 1, x - 1) and check(y - 1, x - 1) and check(y + 2, x - 1) and check(y + 1, x - 2):
            y += 1
            x -= 1
            d = (d - 1) % 4
        elif check(y, x + 2) and check(y + 1, x + 1) and check(y - 1, x + 1) and check(y + 1, x + 2) and check(y + 2, x + 1):
            y += 1
            x += 1
            d = (d + 1) % 4
        else:
            break

    if not inside(y, x - 1) or not inside(y, x + 1) or not inside(y + 1, x) or not inside(y - 1, x):
        return [False, -1, -1]
    else:
        pan[y][x - 1] = non
        pan[y][x + 1] = non
        pan[y + 1][x] = non
        pan[y - 1][x] = non
        pan[y][x] = non
        if d == 0: #출구 설정
            pan[y - 1][x] = -non
        elif d == 1:
            pan[y][x + 1] = -non
        elif d == 2:
            pan[y + 1][x] = -non
        elif d == 3:
            pan[y][x - 1] = -non

        return True, y, x #정령 좌표


def bfs(i,j):
    dx = [-1,0 ,1,0]
    dy = [0,-1,0, 1]
    visited = [[False] * C for _ in range(R)]
    q = deque()
    q.append([i, j])
    visited[i][j] = True
    came = []
    while q:
        y,x = q.popleft()
        for i in range(4):
            ny = y + dy[i]
            nx = x + dx[i]
            if not inside(ny, nx) or visited[ny][nx] or pan[ny][nx] == 0:
                continue

            if abs(pan[ny][nx]) == abs(pan[y][x]) or (pan[y][x] < 0 and abs(pan[y][x]) != abs(pan[ny][nx])):
                visited[ny][nx] = True
                came.append(ny)
                q.append([ny, nx])

    came = sorted(came, reverse= True)
    haha = came[0]
    return haha + 1




score = 0
for non in range(1, K + 1):

    c, d = map(int, input().split())
    c -= 1
    res = move(c,d, non) #답 받아오기
    atwood , y, x = res #판이 꽉 찾는지 확인


    if atwood: #끝나지 않았을때
       sc = bfs(y,x)
       score += sc
    else:
        pan = [[0] * C for _ in range(R)]


print(score)