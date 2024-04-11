import sys
s=sys.stdin

n,m,p,c,d = map(int, s.readline().split())
game_table =[[0] * (n+1) for _ in range(n+1)]

input_x,input_y = map(int, s.readline().split())
game_table[input_x][input_y] =-1 #사슴은 -1로 표시
deer_index =[input_x,input_y]
score=[0 for _ in range(p+1)]
shocked_santa=[0 for _ in range(p+1)]
fail_santa=[]

for i in range(p):
    santa_n, x, y = map(int,s.readline().split())
    game_table[x][y] = santa_n

def is_out_range(x,y):
    return not (x>0 and y>0 and x<=n and y<=n)

#루돌프 이동
def move_deer():
    global deer_index
    dx=[0,1,0,-1,1,1,-1,-1]
    dy=[-1,0,1,0,1,-1,1,-1]
    #현재 루돌프의 위치
    deer_x, deer_y =0,0
    for i in range(1, n+1):
        for j in range(1, n+1):
            if (game_table[i][j] == -1):
                deer_x = i
                deer_y = j
    #가장 가까운 산타 찾기
    min_distance=100
    min_x, min_y =0,0
    for i in range(1, n+1):
        for j in range(1, n+1):
            if (game_table[i][j] > 0):
                #산타 발견 => 거리 측정
                distance = (deer_x-i)**2 + (deer_y - j)**2
                if(distance <= min_distance):
                    min_distance= distance
                    min_x = i
                    min_y = j
    #가장 가까운 산타에게 이동 => 8방향 중 가장 가까워질 수 있는 방향 선택
    min_move=100
    min_move_x, min_move_y=0,0
    move_direction=-1
    for i in range(8):
        _x = deer_x+dx[i]
        _y = deer_y+dy[i]
        if (is_out_range(_x, _y)):
            continue
        num = (_x - min_x)**2 + (_y-min_y)**2
        if (num < min_move):
            #이동 
            min_move= num
            min_move_x=_x
            min_move_y=_y
            move_direction=i
    #루돌프 이동
    game_table[deer_x][deer_y] =0
    #충돌 여부 (산타가 그 자리에 있다면)
    if (game_table[min_move_x][min_move_y] > 0):
        santa_num = game_table[min_move_x][min_move_y]
        score[santa_num] +=c
        #산타 기절
        shocked_santa[santa_num] = 2;
        #산타는 루돌프가 온 방향으로 c칸 이동
        game_table[min_move_x][min_move_y]=0
        _x = min_move_x+ (dx[move_direction]*c)
        _y = min_move_y+ (dy[move_direction]*c)
        if (is_out_range(_x, _y)):
            fail_santa.append(santa_num)
        if(not is_out_range(_x, _y)): 
        #탈락이 아니라면. 탈락이면 game_table에 기록 안함.
        #산타가 밀려났는데 그 자리에 산타가 있었다면 ? 상호작용
            if ( game_table[_x][_y] >0):
            #상호작용 발생 
                interact(santa_num, _x, _y, dx[move_direction], dy[move_direction])
            game_table[_x][_y] = santa_num
    #루돌프 이동
    game_table[min_move_x][min_move_y]=-1
    deer_index=[min_move_x, min_move_y]

def interact(santa_num, x,y, direction_x, direction_y):
    #원래 있던 애를 한칸 밀기
    prev_santa=game_table[x][y]
    _x=x+direction_x
    _y=y+direction_y

    if (not is_out_range(_x, _y) and game_table[_x][_y] >0):
        #미는 곳에도 산타가 있다면
        interact(prev_santa, _x, _y, direction_x, direction_y)
    if(is_out_range(_x, _y)):
        game_table[x][y] = santa_num
        return;
    else:
        game_table[_x][_y] = prev_santa
        game_table[x][y] = santa_num
        return;


#산타 이동
def move_santa(cur_p):
    #루돌프 위치
    deer_x = deer_index[0]
    deer_y = deer_index[1]
    dx=[-1,0,1,0]
    dy=[0,1,0,-1]
    for i in range(1, n+1):
        for j in range(1, n+1):
            min_distance_x, min_distance_y=0,0
            if (game_table[i][j] == cur_p):
                #p번 산타 (1부터 순서대로)
                #루돌프와의 원래 거리
                now_distance = (deer_x-i)**2 + (deer_y -j) **2
                min_distance=now_distance
                move_direction=-1
                for direction_index in range(4): #상, 우, 하, 좌
                    _x=i+dx[direction_index]
                    _y=j+dy[direction_index]
                    if (is_out_range(_x, _y)):
                        continue
                    if (game_table[_x][_y] > 0):
                        continue
                    #루돌프에게 가장 가까워질 수 있는 방향 찾아서 그리로 이동
                    #기존 보다 더 멀어지는 경우만 있을 땐 그냥 이동 안함 
                    num = (deer_x - _x)**2 + (deer_y - _y)**2
                    if (num < min_distance):
                        min_distance= num
                        min_distance_x = _x
                        min_distance_y = _y
                        move_direction=direction_index
                #이동할 수 있으면 이동
                if (min_distance_x > 0 and min_distance_y >0):
                    game_table[i][j]=0;
                    #충돌 여부
                    if (game_table[min_distance_x][min_distance_y] == -1):
                        #루돌프가 있던 자리라 충돌함 => 산타 이동
                        score[cur_p]+=d
                        #산타 기절
                        shocked_santa[cur_p] = 2
                        #이동해온 반대 방향으로 산타 다시 D칸 이동
                        if (move_direction<=1):
                            crash_move_x = min_distance_x + (dx[move_direction+2] * d)
                            crash_move_y = min_distance_y + (dy[move_direction+2] * d)
                        if (move_direction >= 2):
                            crash_move_x = min_distance_x + (dx[move_direction-2] * d)
                            crash_move_y = min_distance_y + (dy[move_direction-2] * d)
                        if (is_out_range(crash_move_x, crash_move_y)):
                            fail_santa.append(cur_p)
                        if (not is_out_range(crash_move_x, crash_move_y)):    
                            #탈락 아닌경우. 탈락이면 game_table에 기입 안함
                            if (game_table[crash_move_x][crash_move_y] >0):
                                #상호작용
                                if (move_direction<=1): 
                                    interact(cur_p, crash_move_x, crash_move_y,dx[move_direction+2], dy[move_direction+2] )
                                if(move_direction >= 2):
                                    interact(cur_p, crash_move_x, crash_move_y,dx[move_direction-2], dy[move_direction-2] )
                            else: 
                                game_table[crash_move_x][crash_move_y] = cur_p
                    else:
                        game_table[min_distance_x][min_distance_y] = cur_p
                #해당 산타 찾아서 이동했으면 그 산타는 탐색 끝
                return;


#산타 1부터 순서대로 이동 작업 수행 (기절한 산타는 제외)
def all_santa():
    for i in range(1, p+1):
        if (shocked_santa[i] == 0):
            move_santa(i)
    #중간에 게임 종료되는 조건
    if(len(fail_santa) == p):
        return
    #탈락하지 않고 남은 산타들 +1점
    for i in range(1, n+1):
        for j in range(1, n+1):
            if (game_table[i][j] > 0):
                score[game_table[i][j]]+=1

for i in range(m):
    #중간에 게임 종료되는 조건
    if(len(fail_santa) == p):
        break
    #기절한 산타 1 줄여주기
    for s in range(1, p+1):
        if (shocked_santa[s] > 0):
            shocked_santa[s] -=1
    move_deer()
    all_santa()
    
print(*score[1:])