import sys
import copy
from collections import deque
from collections import defaultdict as ha
import heapq


K,M = map(int, input().split())
maze = [list(map(int, input().split())) for _ in range(5)]
piece = list(map(int, input().split()))

def bfs(i,j): #조각 소거 개수
    global visited, chose
    dx = [1,0,-1,0]
    dy = [0,1,0,-1]
    q = deque()
    q.append([i,j])
    visited[i][j] = True
    chose.append([i,j])
    cnt = 1
    while q:
        y,x = q.popleft()

        for k in range(4):
            ny = dy[k] + y
            nx = dx[k] + x
            if 0 <= ny < 5 and 0 <= nx < 5 and visited[ny][nx] == False and pan[ny][nx] == pan[y][x] and pan[ny][nx] != 0:
                    visited[ny][nx] = True
                    chose.append([ny, nx])
                    q.append([ny,nx])
                    cnt += 1



    if cnt < 3:
        for _ in range(cnt):
            y,x = chose.pop()
            visited[y][x] = False




def bbfs(i,j): #조각 소거 개수
    global visited, cchose
    dx = [1,0,-1,0]
    dy = [0,1,0,-1]
    qqq = deque()
    qqq.append([i,j])
    visited[i][j] = True
    cchose.append([i,j])
    cnt = 1
    while qqq:
        y,x = qqq.popleft()

        for k in range(4):
            ny = dy[k] + y
            nx = dx[k] + x
            if 0 <= ny < 5 and 0 <= nx < 5 and visited[ny][nx] == False and fpan[ny][nx] == fpan[y][x]:
                    visited[ny][nx] = True
                    cchose.append([ny, nx])
                    qqq.append([ny,nx])
                    cnt += 1



    if cnt < 3:
        for _ in range(cnt):
            y,x = cchose.pop()
            visited[y][x] = False

def rotate(y,x):
    hey = copy.deepcopy(pan)
    #엣지 처리
    hey[y + 1][x - 1] = pan[y + 1][x + 1]
    hey[y - 1][x - 1] = pan[y + 1][x - 1]
    hey[y - 1][x + 1] = pan[y - 1][x - 1]
    hey[y + 1][x + 1] = pan[y - 1][x + 1]
    #변 처리
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
    for i in range(1,4):
        for j in range(1,4):
            pan = copy.deepcopy(maze)
            #1-2 회전

            for pp in range(3):
                pan = rotate(i,j)
                # 2-1 1차획득 돌려서 나오는 가장 큰 수, 좌표 저장
                visited = [[False] * 5 for _ in range(5)]
                chose = []
                # print("중점",i,j,pp)
                for q in range(5):
                    for w in range(5):
                        if visited[q][w] == False and pan[q][w] != 0:
                            bfs(q,w)
                # for row in visited:
                #     print(row)
                # print(chose)
                if len(chose) > len(final):
                    angle = pp
                    center = (i,j)
                    final = chose
                    fpan = copy.deepcopy(pan)
                # 2-2 만약 크기가 같다면, 각도 가장 작은 친구로 좌표 저장
                elif len(chose) == len(final):
                    if pp < angle:
                        angle = pp
                        center = (i,j)
                        final = chose
                        fpan = copy.deepcopy(pan)
                    # 2-3 각도가 같다면,열이 가장 작은 구간
                    elif pp == angle:
                        yy,xx = center
                        if yy > i:
                            angle = pp
                            center = (i, j)
                            final = chose
                            fpan = copy.deepcopy(pan)
                        # 2-4 열이 같다면, 행이 가장 작은 구간
                        elif yy == i:
                            yy, xx = center
                            if xx > j:
                                angle = pp
                                center = (i, j)
                                final = chose
                                fpan = copy.deepcopy(pan)


    while True:

        ans += len(final)

        # 3 유물 소거 bfs로 완료
        for i in final:
            y,x = i
            fpan[y][x] = 0

        # 4 조각추가 리스트에 있는거 차례대로 어펜드
        for i in range(5):
            for j in range(4,-1,-1):
                if fpan[j][i] == 0:
                    if piece:
                        fpan[j][i] = piece.pop(0)

        #5 추가 된이후 다시 bfs
        visited = [[False] * 5 for _ in range(5)]
        cchose = []

        for q in range(5):
            for w in range(5):
                if visited[q][w] == False and fpan[q][w] != 0:
                    bbfs(q,w)

        final = cchose

        if len(cchose) == 0:
            break

    maze = copy.deepcopy(fpan)
    if ans != 0:
        realans.append(ans)
    else:
        break


print(*realans)