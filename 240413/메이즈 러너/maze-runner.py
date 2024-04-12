import sys

s=sys.stdin

n,m,k = map(int, s.readline().split())
board = [[0]*(n+1) for _ in range(n+1)]

for i in range(1, n+1):
    board[i]=[0] + list(map(int, s.readline().split()))

#회전에 쓸 배열
next_board = [[0]*(n+1) for _ in range(n+1)]

traveler=[(-1,-1)]+[
    tuple(map(int, s.readline().split()))
    for _ in range(m)
]

exits = tuple(map(int, s.readline().split()))

answer=0

#회전할 최소 정사각형 (좌측 상단 좌표, 한 변 길이)
sx, sy, square_size=0,0,0

#참가자 이동
def move_all_traveler():
    global answer, exits
    for i in range(1, m+1):
        #이미 참가자가 출구에 있는 경우(탈출한 참가자)
        if (traveler[i] == exits):
            continue;
        tx, ty = traveler[i]
        ex, ey = exits

        #상하이동 (상하 먼저, 좌우는 다음)
        if (tx != ex):
            _x, _y = tx,ty
            if ex > tx:
                _x+=1
            else: 
                _x-=1
            #벽이 아닌 경우에만 이동 가능
            if not board[_x][_y] > 0:
                traveler[i] =(_x, _y) #위치 변경
                answer+=1
                continue #다음 참가자로 넘어가기
        if (ty != ey):
            _x, _y = tx, ty
            if (ey > ty):
                _y+=1
            else:
                _y-=1
            #벽이 아닌 경우 이동
            if not board[_x][_y] > 0:
                traveler[i]=(_x, _y)
                answer+=1
                continue

# 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형 찾기
def find_minimum_square():
    global exits, sx, sy, square_size
    ex, ey = exits

    #미로 안에서 가능한 모든 정사각형을 만들어보기(가장 작은 정사각형부터, 좌측 상단부터)
    #한 변의 길이는 2부터 가능
    for size in range(2, n+1):
        #좌측 상단 좌표(x1, y1)
        for x1 in range(1, n-size+2):
            for y1 in range(1, n-size+2):
                #우측 하당 좌표(x2,y2)
                x2, y2= x1+size-1, y1+size-1
                #출구가 포함 안되어있으면 패스
                if ( ex < x1 or ex > x2 or ey <y1 or ey > y2 ):
                    continue
                #참가자가 한명이라도 포함되어있어야함
                is_traveler_in = False
                for traveler_index in range(1, m+1):
                    tx, ty = traveler[traveler_index]
                    if (tx >= x1 and tx <=x2 and ty >= y1 and ty <=y2):
                        if not (tx == ex and ty == ey):
                            #출구에 서있는 애들은 탈출한거니까 고려하지 않음
                            is_traveler_in= True
                
                    if is_traveler_in:
                        #찾음 => 더이상 찾을 필요 없음, 함수 종료
                        sx, sy=x1, y1
                        square_size=size
                        return;
# 벽 회전
def rotate_square():
    #벽 내구도 감소
    for x in range(sx, sx+square_size):
        for y in range(sy, sy+square_size):
            if (board[x][y] > 0):
                board[x][y]-=1
    
    #시계방향으로 90도 회전
    for x in range(sx, sx+square_size):
        for y in range(sy, sy+square_size):
            #1. (sx, sy)를 (0,0)으로 옮겨주는 변환
            ox, oy = x-sx, y-sy
            #2. 회전 후 (rx, ry) = (oy, square_size-ox-1)
            rx , ry = oy, square_size-ox-1
            #3. 0,0으로 밀었을때의 회전 후 좌표가 rx,ry이므로 다시 밀어주기
            # 변환도중에 board 변경하면 안되니까 next_board 사용
            next_board[rx+sx][ry+sy] = board[x][y]
    #회전 끝난 후 board에 적용
    for x in range(sx, sx+square_size):
        for y in range(sy, sy+square_size):
            board[x][y] = next_board[x][y]
    
# 벽 안에 있던 사람들, 출구 회전
def rotate_traveler_and_exit():
    global exits
    #정사각형 안에 들어있는 사람들 찾기
    for i in range(1, m+1):
        tx, ty = traveler[i]
        if (tx >= sx and tx < sx+square_size and ty >=sy and ty < sy+square_size):
            #회전 대상
            #1. (0,0)으로 이동
            ox, oy = tx-sx, ty-sy
            #2. 이동시킨 상황에서 회전한다고 가정
            rx, ry = oy, square_size - ox -1
            #3. 다시 sx, sy 만큼 밀기
            traveler[i]=(rx + sx, ry+sy)
    #출구 회전
    ex, ey = exits
    if (ex >= sx and ex < sx+square_size and ey >= sy and ey < sy+square_size):
        #1. (0,0)으로 이동
        ox, oy = ex-sx, ey - sy
        #2. 회전
        rx, ry = oy, square_size-ox-1
        #3. 밀기
        exits=(rx+sx, ry+sy)


#게임 시간동안 반복
for _ in range(k):
    move_all_traveler()
    #모든 사람이 출구로 탈출했는지 판단합니다.
    #다 탈출했다면(travler의 좌표값이 출구 좌표값) 종료
    exits_num =0
    for i in range(1, m+1):
        if (traveler[i] == exits):
            exits_num+=1
    if (exits_num == m):
        #다 탈출
        break

    find_minimum_square()

    rotate_square()
    rotate_traveler_and_exit()


print(answer)
ex, ey =exits
print(ex, ey)