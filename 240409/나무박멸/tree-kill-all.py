import sys
import copy

input = sys.stdin.readline

n,m,k,c = map(int, input().split())
tree = [[0] * (n + 1)]
for _ in range(n):
    tree.append([0] + list(map(int, input().split())))

answer=0

dx=[-1,0,1,0]
dy=[0,-1,0,1]
rx=[-1,1,1,-1]
ry=[-1,-1,1,1]

#번식에서 사용할 배열
add_tree = [
    [0] * (n + 1)
    for _ in range(n + 1)
]
#제초제 남은 년수 기록하기 위한 배열
herb = [
    [0] * (n + 1)
    for _ in range(n + 1)
]

def is_out_range(x,y):
    return not (1 <= x and x <= n and 1 <= y and y <= n)

# 1. 성장
def step_one():
    for i in range(1, n+1):
        for j in range(1, n+1):
            #나무가 있는 경우
            if (tree[i][j] >0):
                cnt =0
                for num in range(4):
                    _x = i+dx[num]
                    _y = j+dy[num]
                    if (is_out_range(_x, _y)):
                        continue
                    if (tree[_x][_y] >0):
                        cnt+=1
                tree[i][j]+=cnt

#2. 번식
def step_two():
    global add_tree
    #이전 회차에서 사용한 add_tree 초기화
    for i in range(1, n + 1):
        for j in range(1, n + 1): 
            add_tree[i][j] = 0

    for i in range(1, n+1):
        for j in range(1, n+1):
            if (tree[i][j] > 0):
                #주변 빈 공간 개수 찾기
                cnt =0;
                for num in range(4):
                    _x = i+dx[num]
                    _y = j+dy[num]
                    if(is_out_range(_x, _y)):
                        continue
                    if (herb[_x][_y] >0):
                        continue
                    if (tree[_x][_y] == 0):
                        cnt+=1
                for num in range(4):
                    _x = i+dx[num]
                    _y = j+dy[num]
                    if(is_out_range(_x, _y)):
                        continue
                    if (herb[_x][_y] >0):
                        continue
                    if (tree[_x][_y] == 0):
                        #tree가 아닌 add_tree에 번식
                        add_tree[_x][_y]+=tree[i][j] // cnt         
    #add_tree와 tree 합치기
    for i in range(1, n+1):
        for j in range(1, n+1):
            tree[i][j] += add_tree[i][j]

#3. 제초제 위치 선정 및 뿌리기
def step_three():
    global answer

    maximum=0
    max_x, max_y =1,1

    for i in range(1, n+1):
        for j in range(1, n+1):
            if (tree[i][j] > 0):
                cnt = tree[i][j]
                for _n in range(4):
                    for _m in range(1, k+1):
                        nx = i+(rx[_n]*_m)
                        ny = j+(ry[_n]*_m)
                        if is_out_range(nx, ny): 
                            break
                        if tree[nx][ny] <= 0: 
                            break
                        cnt += tree[nx][ny]
                if (maximum < cnt):
                    maximum = cnt
                    max_x = i
                    max_y = j

    #박멸한 나무 수 (answer) 갱신
    answer+=maximum
    
    #찾은 위치에 제초제 뿌리기
    if(tree[max_x][max_y] > 0):
        tree[max_x][max_y] = 0
        herb[max_x][max_y] = c                
        for _n in range(4):
            for _m in range(1, k+1):
                nx = max_x+(rx[_n]*_m)
                ny = max_y+(ry[_n]*_m)
                if is_out_range(nx, ny): 
                    break
                if tree[nx][ny] < 0: 
                    break
                if tree[nx][ny] == 0:
                    herb[nx][ny] = c
                    break
                #나무 박멸 및 제초제 년수 기록
                tree[nx][ny]=0
                herb[nx][ny]=c

# 제초제 1년 감소
def delete_herb():
    for i in range(1, n+1):
        for j in range(1, n+1):
            if (herb[i][j] > 0):
                herb[i][j]-=1

#실전 , 몇년동안 
for i in range(m):
    step_one()
    step_two()
    delete_herb()
    step_three()

print(answer)