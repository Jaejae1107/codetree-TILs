import sys
import copy
from collections import deque


L,N,Q = map(int, input().split())

chess = [list(map(int, input().split())) for _ in range(L)] #0 빈칸, 1함정, 2벽
health = [0] * (3 + N) #용사 체력
knight = [[0] * L for _ in range(L)] # 기사 위치
kloc = dict()
firstk = 3
for _ in range(N): #초기 기사 정보
    r, c, h, w, k = map(int, input().split())
    health[firstk] = k
    kloc.update({firstk: []})
    for i in range(r - 1, r + h - 1):
        for j in range(c - 1, c + w - 1):
            knight[i][j] = firstk
            kloc[firstk].append([i,j])
    firstk += 1

start = copy.deepcopy(health) #기존 체력. 마지막에 빼기로 데미지 계산


def knightmove(kid,dirc):
    global kloc, knight, changel
    q = deque()
    newkloc = []
    move = []
    tmp = copy.deepcopy(kloc)
    a = kloc.pop(kid)
    nocng = 0
    kloc.update({kid: a})
    for sena in a:
        y, x = sena
        knum = knight[y][x] #기사번호
        q.append([y,x,knum])

    while q:

        y,x,knum = q.pop()
        ny = y + dy[dirc]
        nx = x + dx[dirc]
        if 0 > ny or ny >= L or 0 > nx or nx >= L:  # 만약 밖으로 빠져나가면 움직임 취소
            nocng = 1
            newkloc.clear()
            break
        if chess[ny][nx] == 2:  # 만약 벽이라면, 취소
            newkloc.clear()
            nocng = 1
            break
        if (chess[ny][nx] == 0 or chess[ny][nx] == 1) and (knight[ny][nx] == knum or knight[ny][nx] == 0): #아무것도 없다면
            if knum not in move:
                move.append(knum)
            newkloc.append([ny,nx,knum]) #배치 완료
        else:
            nextknum = knight[ny][nx] #기존 기사 밀고
            if knum not in move:
                move.append(knum)
            newkloc.append([ny, nx, knum])


            kekeys = list(kloc.keys())
            if nextknum in kekeys:
                needck = kloc.pop(nextknum)
            for sena in needck:
                y, x = sena
                knum = knight[y][x]  # 기사번호
                q.append([y, x, knum])

    if nocng == 1: # 바뀐게 없다면 원복
        kloc = copy.deepcopy(tmp)

    else:
        a = list(kloc.keys())
        for ja in move:
            if ja in a:
                kloc.pop(ja)
            kloc.update({ja: []})

        for i in newkloc:
            y, x, knum = i
            kloc[knum].append([y,x])
            changel.append(knum)

        knight = [[0] * L for _ in range(L)]  # 기사 위치 업데이트
        keke = kloc.keys()
        for jwa in keke:
            b = kloc[jwa]
            for jjwa in b:
                y,x = jjwa
                knight[y][x] = jwa

    return nocng, changel
def healthcare(movek,changel):
    ban = []
    for i in range(L):
        for j in range(L):
            if chess[i][j] == 1:
                a = knight[i][j]
                if a != movek and a in changel and health[a] > 0:
                    health[a] -= 1
                    if health[a] == 0:
                        ban.append(a)
                        kloc.pop(a)


    for i in range(L):
        for j in range(L):
            aa = knight[i][j]
            if aa in ban:
                knight[i][j] = 0







dx = [0,1,0,-1]
dy = [-1,0,1,0]
for _ in range(Q): #왕명
    changel = []
    i, d = map(int, input().split()) #i번 기사, d로 이동
    i += 2 #기사 내가 쓰는걸로 업뎃
    # print(kloc)
    if health[i] != 0: #기사가 살아있다면

        valid, changel = knightmove(i,d) #기사들의 움직임 끝, 움직임 유무 리턴
        if valid != 1:
            healthcare(i, changel) #움직였다면, 체력 관리
        # print("after healthcare")
        # print(health)

ans = 0
for i in range(1,N + 1):
    if health[i + 2] > 0:
        ans += start[i + 2] - health[i + 2]

print(ans)