def night_move(oi, od):
    r1, c1, h1, w1, k1 = night_info[oi]
    if k1 <= 0: return False,[],[]
    visited = [[False for _ in range(l)] for _ in range(l)]
    queue = deque()
    can_go = []
    move_number = []
    move_number.append(oi)
    for i1 in range(r1, r1 + h1):
        for j1 in range(c1, c1 + w1):
            visited[i1][j1] = True
            queue.append((i1, j1))
            can_go.append((oi, i1, j1))
    while queue:
        x, y = queue.popleft()
        nx, ny = x + dx[od], y + dy[od]
        if in_range(nx, ny) and visited[nx][ny] == False and n_board[nx][ny] == oi:
            queue.append((nx, ny))
            can_go.append((nx, ny))
            visited[nx][ny] = True
        elif in_range(nx, ny) and visited[nx][ny] == False and board[nx][ny] == 2:
            return False, [], []
        elif in_range(nx, ny) and visited[nx][ny] == False and n_board[nx][ny] != oi:
            if n_board[nx][ny] != 0:  # 빈공간이 아니라면
                r1, c1, h1, w1, k1 = night_info[n_board[nx][ny]]
                move_number.append(n_board[nx][ny])
                for k1 in range(r1, r1 + h1):
                    for k2 in range(c1, c1 + w1):
                        queue.append((k1, k2))
                        visited[k1][k2] = True
                        can_go.append((n_board[nx][ny], k1, k2))
        elif not in_range(nx, ny):
            return False, [], []

    return True, can_go, move_number


import sys
from collections import deque



dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
l, n, q = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(l)]
night_info = [0]
n_board = [[0 for _ in range(l)] for _ in range(l)]
damage = 0
damaged_night= [ 0 for _ in range(n+1)]
for nights in range(1, n + 1):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    night_info.append((r, c, h, w, k))
    for i in range(r, r + h):
        for j in range(c, c + w):
            n_board[i][j] = nights


def in_range(x, y):
    return 0 <= x < l and 0 <= y < l


def night_move(oi, od):
    r1, c1, h1, w1, k1 = night_info[oi]
    if k1 <= 0: return False,[],[]
    visited = [[False for _ in range(l)] for _ in range(l)]
    queue = deque()
    can_go = []
    move_number = []
    move_number.append(oi)
    for i1 in range(r1, r1 + h1):
        for j1 in range(c1, c1 + w1):
            visited[i1][j1] = True
            queue.append((i1, j1))
            can_go.append((oi, i1, j1))
    while queue:
        x, y = queue.popleft()
        nx, ny = x + dx[od], y + dy[od]
        if in_range(nx, ny) and visited[nx][ny] == False and n_board[nx][ny] == oi:
            queue.append((nx, ny))
            can_go.append((nx, ny))
            visited[nx][ny] = True
        elif in_range(nx, ny) and visited[nx][ny] == False and board[nx][ny] == 2:
            return False, [], []
        elif in_range(nx, ny) and visited[nx][ny] == False and n_board[nx][ny] != oi:
            if n_board[nx][ny] != 0:  # 빈공간이 아니라면
                r1, c1, h1, w1, k1 = night_info[n_board[nx][ny]]
                move_number.append(n_board[nx][ny])
                for k1 in range(r1, r1 + h1):
                    for k2 in range(c1, c1 + w1):
                        queue.append((k1, k2))
                        visited[k1][k2] = True
                        can_go.append((n_board[nx][ny], k1, k2))
        elif not in_range(nx, ny):
            return False, [], []

    return True, can_go, move_number


def moving_night(arr, marr, oi, od):
    global n_board
    # arr안에있는녀석들을 od방향으로 밀어줘야한다.
    t_nboard = [[0 for _ in range(l)] for _ in range(l)]

    for i in range(l):
        for j in range(l):
            if not n_board[i][j] in marr:
                t_nboard[i][j] = n_board[i][j]

    for number, x, y in arr:
        nx, ny = x + dx[od], y + dy[od]
        t_nboard[nx][ny] = number

    n_board = [[t_nboard[i][j] for j in range(l)] for i in range(l)]
    return



def damaged(m_arr, oi):
    for i in range(l):
        for j in range(l):
            if n_board[i][j] == oi: continue
            if n_board[i][j] == 0 : continue
            if not n_board[i][j] in m_arr: continue
            if board[i][j] == 1 :
                r1, c1, h1, w1, k1 = night_info[n_board[i][j]]
                k1 -= 1
                damaged_night[n_board[i][j]] += 1
                night_info[n_board[i][j]] = r1, c1, h1, w1, k1
                if k1 <= 0 : # 맵 밀어줘야한다.
                    for i1 in range(r1,r1+h1):
                        for j1 in range(c1,c1+w1):
                            n_board[i1][j1] = 0
    return

def update_night_info():
    checked = []
    for i in range(l):
        for j in range(l):
            if n_board[i][j] == 0 : continue
            if not n_board[i][j] in checked:
                checked.append(n_board[i][j])
                r1, c1, h1, w1, k1 = night_info[n_board[i][j]]
                night_info[n_board[i][j]] = i, j, h1, w1, k1
    return


def all_live_night_damaged():
    count = 0
    for night_num in range(1,n+1):
        r1, c1, h1, w1, k1 = night_info[night_num]
        if k1 > 0 :
            count += damaged_night[night_num]
    return count


for order in range(q):
    oi, od = map(int, input().split())
    possible, can_arr, m_arr = night_move(oi, od)
    if possible:
        moving_night(can_arr, m_arr, oi, od)  # 움직일수있는애들 반영하기.
        update_night_info()
        damaged(m_arr, oi)

print(all_live_night_damaged())