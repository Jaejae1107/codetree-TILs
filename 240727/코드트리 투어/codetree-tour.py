import sys
import copy
from collections import deque
from collections import defaultdict as ha
import heapq





def daik(start): #start 노드에서 다른 노드까지의 최소값을 계산

    visited = ha(lambda: 1e9)
    visited[start] = 0
    heap = [(0,start)]
    while heap:

        c,x = heapq.heappop(heap)
        if c < visited[x]:
            continue
        for nx,cost in G[x]:

            nc = cost + c
            if nc < visited[nx]:
                heapq.heappush(heap, (nc,nx))
                visited[nx] = nc

    return visited




start = 0
poss, impos = [], []
pos_set, imp_set, ban = set(), set(), set()
Q = int(input())
for _ in range(Q):
    order,*info=  list(map(int, input().split()))

    if order == 100: #노드와 엣지 구성 완료
        n, m, *info = info

        # 중복 간선 셀프 간선 처리
        G_temp = ha(lambda : ha(lambda : 1e9))
        for i in range(m):
            v,u,cost = info[3*i:3*i+3]
            G_temp[v][u] = min(G_temp[v][u],cost)
            G_temp[u][v] = min(G_temp[u][v], cost)

        G = ha(list)
        for haha in G_temp:
            G[haha].extend(G_temp[haha].items())
        V = daik(start)


    elif order == 200:
        iid, rev, dest = info
        profit = rev - V[dest]

        if profit >= 0:
            heapq.heappush(poss,(-profit, iid,rev,dest))
            pos_set.add(iid)
        else:
            impos.append((-profit, iid,rev,dest))
            imp_set.add(iid)

    elif order == 300:
        iid = info[0]
        if iid in pos_set or iid in imp_set:
            ban.add(iid)
        pos_set.discard(iid)
        imp_set.discard(iid)

    elif order == 400:
        temp = []
        while poss:
            profit, iid, rev, dest = heapq.heappop(poss)
            if iid in ban:
                continue
            if iid in pos_set:
                print(iid)
                pos_set.discard(iid)
                ban.add(iid)
                break
            else:
                temp.append((profit,iid, rev, dest))

        else:
            print(-1)


        for i in temp:
            heapq.heappush(poss, i)

    elif order == 500:
        start = info[0]
        V = daik(start)
        temp, temp_ban = [], []
        pos_set, imp_set = set(), set()
        for sales in (poss, impos):
            for _, iden, price, dest in sales:
                if iden in ban:
                    continue
                profit = price - V[dest]
                if profit >= 0:  # 도달 가능 / 취소안한상품
                    heapq.heappush(temp, (-profit, iden, price, dest))
                    pos_set.add(iden)
                else:  # 도달 불가능
                    temp_ban.append((-profit, iden, price, dest))
                    imp_set.add(iden)
        poss = temp
        impos = temp_ban