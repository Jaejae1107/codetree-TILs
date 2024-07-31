import sys
import copy
from collections import deque

q =  deque()
N, M, K = map(int, input().split())
game = [list(map(int, input().split())) for _ in range(N)]
ppl = [[[] for _ in range(N)] for _ in range(N)]
for _ in range(M):
    y,x = map(int, input().split())
    q.append([y - 1, x - 1])
exy, exx = map(int, input().split())
exit = (exy - 1, exx - 1)



def move():
    global movee,ppl
    dy = [-1,1,0,0]
    dx = [0,0,1,-1]
    ey,ex = exit

    newq = []
    while q:
        y,x = q.popleft() #이동
        ny = y
        nx = x
        curdist = abs(ex - x) + abs(ey - y) #이동전 거리

        for i in range(4):
            nny = dy[i] + y
            nnx = dx[i] + x
            if 0 <= nny < N and 0 <= nnx < N and game[nny][nnx] == 0:
                newdist =  abs(ex - nnx) + abs(ey - nny)

                if curdist > newdist:
                    curdist = newdist
                    ny = nny
                    nx = nnx


        if (ny,nx) != (y, x):
            movee += 1

        if (ny, nx) == (ey,ex):
            ppl[ny][nx] = []
        else:
            newq.append([ny,nx])

    ppl = [[[] for _ in range(N)] for _ in range(N)]

    for k in newq:
        y,x = k
        ppl[y][x].append(10)
    ppl[ey][ex] = [20]
    return ppl


def rotatepoint():
    ey,ex = exit

    for size in range(1, N + 1):
        for y1 in range(N - size):
            for x1 in range(N - size):
                y2, x2 = y1 + size, x1 + size #맨 끝

                if not (x1 <= ex and ex <= x2 and y1 <= ey and ey <= y2):
                    continue

                runner = False
                for i in range(y1, y2 + 1):
                    for j in range(x1, x2 + 1):
                        if ppl[i][j] != [] and ppl[i][j] != [20]:
                            runner = True


                if runner == True:
                    maxy = y2
                    maxx = x2
                    minx = x1
                    miny = y1
                    return maxy, maxx, miny, minx



def rotate(maxy, maxx, miny, minx):
    global exit,ppl
    len = maxy - miny + 1

    for i in range(miny, maxy + 1):
        for j in range(minx, maxx + 1):
            if game[i][j] != 0:
                game[i][j] -= 1



    for p in range(len // 2):
        we1 = [] #게임판용
        arae1 = []
        when1 = []
        oh1 = []

        we2 = [] #인구용
        arae2 = []
        when2 = []
        oh2 = []

        #기존 좌표

        for i in range(minx, maxx + 1):
            we1.append(game[miny][i])
            we2.append(ppl[miny][i])

        for i in range(maxx, minx - 1, -1):
            arae1.append(game[maxy][i])
            arae2.append(ppl[maxy][i])


        for i in range(maxy, miny - 1, - 1):
            when1.append(game[i][minx])
            when2.append(ppl[i][minx])



        for i in range(miny, maxy + 1):
            oh1.append(game[i][maxx])
            oh2.append(ppl[i][maxx])




        h = miny
        for i in we1:
            game[h][maxx] = i
            h += 1
        h = maxy
        for i in arae1:
            game[h][minx] = i
            h -= 1
        h = maxx
        for i in oh1:
            game[maxy][h] = i
            h -= 1
        h = minx
        for i in when1:
            game[miny][h] = i
            h += 1

        h = miny
        for i in we2:
            ppl[h][maxx] = i
            h += 1
        h = maxy
        for i in arae2:
            ppl[h][minx] = i
            h -= 1
        h = maxx
        for i in oh2:
            ppl[maxy][h] = i
            h -= 1
        h = minx
        for i in when2:
            ppl[miny][h] = i
            h += 1

        maxy -= 1
        maxx -= 1
        minx += 1
        miny += 1




    for i in range(N):
        for j in range(N):

            if ppl[i][j] == [20]:
                exit = (i,j)
            elif ppl[i][j] != [] and ppl[i][j] != [20]:
                for k in ppl[i][j]:
                    q.append([i,j])



def check():
    for i in range(N):
        for j in range(N):
            if len(ppl[i][j]) > 0  and ppl[i][j] != [20]:
                return True

    return False




movee = 0
for _ in range(K): #k번 반복
    ppl = move() #다 같이 이동

    valid = check()
    if not valid:
        break
    maxy, maxx, miny, minx = rotatepoint()
    # print(maxy, maxx, miny, minx, "모든 값들")
    rotate(maxy, maxx, miny, minx) #다 돌고
    valid = check()
    if not valid:
        break

print(movee)
y,x = exit
print(y + 1, x + 1)