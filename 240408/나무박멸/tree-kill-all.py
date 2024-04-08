import sys
import copy

input = sys.stdin.readline

n,m,k,c = map(int, input().split())
input_arr =[[0] * n for _ in range(n)]
for i in range(n):
    input_arr[i]=list(map(int, input().split()))
for i in range(n):
    for j in range(n):
        if(input_arr[i][j] == -1):
            input_arr[i][j] =-11

answer=0
dx=[0,1,0,-1]
dy=[1,0,-1,0]

nx=[-1,-1,1,1]
ny=[-1,1,-1,1]

#1. 성장
def grow():
    global input_arr
    #동서남북 나무 있는지 탐색
    for i in range(n):
        for j in range(n):
            cur=input_arr[i][j]
            num=0;
            if (cur >0):
                for _n in range(4):
                    _x = i+dx[_n]
                    _y = j+dy[_n]
                    if (_x >=0 and _y >= 0 and _x <n and _y < n):
                        if (input_arr[_x][_y] >0):
                            num+=1;
                input_arr[i][j]+=num;

#번식 
def breed():
    global input_arr
    breed_arr=copy.deepcopy(input_arr)
    #동서남북 빈자리 탐색
    for i in range(n):
        for j in range(n):
            cur= breed_arr[i][j]
            cnt=0
            if (cur>0):
                for _n in range(4):
                    _x = i+dx[_n]
                    _y = j+dy[_n]
                    if (_x >=0 and _y >= 0 and _x <n and _y < n):
                        if (breed_arr[_x][_y] == 0):
                            cnt+=1
                if (cnt!=0):
                    num = cur // cnt
                for _n in range(4):
                    _x = i+dx[_n]
                    _y = j+dy[_n]
                    if (_x >=0 and _y >= 0 and _x <n and _y < n):
                        if (breed_arr[_x][_y] == 0):
                            input_arr[_x][_y] += num

#제초제 위치 선정
def decision():
    global answer
    max_num=-1;
    max_index=[0,0]
    for i in range(n):
        for j in range(n):
            cur = input_arr[i][j]
            num=cur
            if (cur < 0):
                #제초제 있는 자리 : 1년 지났으니 +해주기
                input_arr[i][j]+=1
            if (cur > 0):
                #제초제 퍼지는 범위 고려
                block_m=[]
                for _n in range(1, k+1):
                    for m in range(4):
                        _x = i+(nx[m]*_n)
                        _y = j+(ny[m]*_n)
                        if(m in block_m):
                            continue;
                        if (_x >=0 and _y >= 0 and _x <n and _y < n):
                            if(input_arr[_x][_y] <= 0):
                                #막힘 -> 전파되지 않음
                                block_m.append(m)
                            if(input_arr[_x][_y] >0):
                                num+=input_arr[_x][_y]

            if (num > max_num):
                max_num = num
                max_index=[i,j]
    answer+=max_num
    return max_index

#제초제 뿌림
def sprinkle(x,y):
    global answer
    #answer+=input_arr[x][y]
    input_arr[x][y]=-c
    for _n in range(1, k+1):
        for _m in range(4):
            _x = x+(nx[_m]*_n)
            _y = y+(ny[_m]*_n)
            if (_x >=0 and _y >= 0 and _x <n and _y < n and input_arr[_x][_y] >=0):
                #answer+=input_arr[_x][_y]
                input_arr[_x][_y] =-c

for _ in range(m):
    grow()
    breed()
    [x,y] = decision()
    sprinkle(x,y)
print(answer)