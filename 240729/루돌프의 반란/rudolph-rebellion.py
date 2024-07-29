import sys
import copy
from collections import deque


santas = {}
N, M, P, C, D = map(int, input().split())
finalscore = [0] * (P + 1)
ban = [0] * (P + 1)
rouy, roux = map(int, input().split())  # 루돌프 초기위치
rou = deque()
rou.append([rouy - 1, roux - 1])

game = [[0] * N for _ in range(N)]
game[rouy - 1][roux - 1] = P + 1
for _ in range(P):
    snum, sy, sx = map(int, input().split())
    santas.update({snum: [sy - 1, sx - 1]})
    game[sy - 1][sx - 1] = snum

rdy = [1, 0, -1, 0, 1, 1, -1, -1]
rdx = [0, 1, 0, -1, 1, -1, 1, -1]

sdy = [-1,0,1,0]
sdx = [0,1,0,-1]

# 기본설정 완료

def roumove():
    mdis = 1e9
    y, x = rou.popleft()
    a = santas.values()
    game[y][x] = 0

    for i in a:

        sy, sx = i
        dist = ((sy - y) ** 2) + ((sx - x) ** 2)
        if dist < mdis:
            mdis = dist
            aim = (sy, sx)
        elif dist == mdis:
            yy, xx = aim
            if yy < sy:
                aim = (sy, sx)
            elif yy == sy:
                if xx < sx:
                    aim = (sy, sx)

    newy, newx = aim
    newdist = 1e9
    for i in range(8):  # 돌진방향 선택
        ny = y + rdy[i]
        nx = x + rdx[i]
        if 0 <= ny < N and 0 <= nx < N:
            dist = ((newy - ny) ** 2) + ((newx - nx) ** 2)
            if dist < newdist:
                newdist = dist
                next = (ny, nx)
                dirc = i

    yyy, xxx = next
    return yyy, xxx, dirc


def roupush(y,x,dirc):

    rou.append([y,x])
    if game[y][x] == 0:
        game[y][x] = P + 1
    elif game[y][x] != 0:
        num = game[y][x]  # 자리에 위치한 산타 번호
        finalscore[num] += C
        ban[num] = 2
        ny = y + C * rdy[dirc]
        nx = x + C * rdx[dirc] #C만큼 튕겨나감
        game[y][x] = P + 1
        while True:
            if 0 <= ny < N and 0 <= nx < N:
                if game[ny][nx] == 0:
                    game[ny][nx] = num
                    santas.pop(num)
                    santas.update({num: [ny,nx]})
                    break
                else:
                    newnum = game[ny][nx]
                    game[ny][nx] = num
                    santas.pop(num)
                    santas.update({num: [ny,nx]})
                    ny = ny + rdy[dirc]
                    nx = nx + rdx[dirc]
                    num = newnum
            else:
                santas.pop(num) #밀려나가면 탈락
                break
  
#산타 위치 변경 추가
def gamecheck():
    cnt = 0
    for i in range(N):
        for j in range(N):
            if game[i][j] != 0 and game[i][j] != P + 1:
                cnt += 1
    if cnt == 0:
        return False
    else:
        return True

def santapush():
    global santas
    out = []
    ry,rx = rou.popleft()
    rou.append([ry,rx])
    newloc = []
    a = santas.values()

    for i in a:
        y,x = i
        num = game[y][x]
        curr = ((ry - y) ** 2) + ((rx - x) ** 2)
        # print(num)
        # print(santas)
        newy, newx = y, x
        if ban[num] == 0: #벤당한애들 위치 새로 설정해야함
            for j in range(4):  #새로운 위치 구하기
                ny = y + sdy[j]
                nx = x + sdx[j]
                if 0 <= ny < N and 0 <= nx < N and (game[ny][nx] == 0 or game[ny][nx] == P + 1): #체크필요
                    dist = ((ry - ny) ** 2) + ((rx - nx) ** 2)
                    if curr > dist:
                        newy,newx = ny,nx
                        curr = dist
                        dirc = j
            game[y][x] = 0
            y = newy #새로운 위치
            x = newx

            if [y,x] == [ry,rx]:
                finalscore[num] += D #찾은 산타에서 점수 추가
                ban[num] = 2 #기절
                if dirc == 0: #진행방향과 반대로 밀려남
                    dirc = 2
                elif dirc == 1:
                    dirc = 3
                elif dirc == 2:
                    dirc = 0
                elif dirc == 3:
                    dirc = 1

                ny = y + D * sdy[dirc]
                nx = x + D * sdx[dirc]  # D만큼 튕겨나감
                while True:
                    if 0 <= ny < N and 0 <= nx < N:
                        if game[ny][nx] == 0:
                            game[ny][nx] = num
                            newloc.append([ny,nx,num])
                            break
                        else:
                            newnum = game[ny][nx]
                            game[ny][nx] = num
                            newloc.append([ny, nx, num])
                            ny = ny + sdy[dirc]
                            nx = nx + sdx[dirc]
                            num = newnum
                    else:
                        if num in newloc:
                            out.append([ny,nx, num])  # 밀려나가면 탈락
                        break
            else:
                game[y][x] = num
                newloc.append([y,x,num])
        else: #벤당했을때
            newloc.append([y, x, num]) #그대로


    santas.clear()
    for l in newloc:
        y,x,num = l
        santas.update({num: [y,x]})

    for ll in out:
        y,x,num = ll
        santas.pop(num)

def wakeup():
    for i in range(P + 1):
        if ban[i] > 0:
            ban[i] -= 1


def bonus():
    for i in range(N):
        for j in range(N):
            if game[i][j] != 0 and game[i][j] != P + 1:
                num = game[i][j]
                finalscore[num] += 1




for _ in range(M):
    rouy, roux, dirc = roumove()  # 목표 설정및 돌진
    roupush(rouy,roux, dirc) #상호작용 및 루돌프 이동

    valid = gamecheck() #게임 진행여부
    if valid == False:
        break
    santas = dict(sorted(santas.items()))
    santapush() #산타 움직이고 날라감

    valid = gamecheck() #게임 진행여부
    if valid == False:
        break
    wakeup() #벤 한턴씩 까기
    bonus() #점수 추가

for i in finalscore:
    if i > 0:
        print(i, end = " ")