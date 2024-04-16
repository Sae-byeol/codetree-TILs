const fs = require('fs')
let input = fs.readFileSync(0).toString().split("\n");

[n,m] = input[0].split(' ').map((i) => Number(i))
let inputArr = Array.from(Array(n), ()=> Array(m+1).fill(0))
for (let i=1;i<=n;i++){
    inputArr[i] = [0, ...input[i].split(' ').map((n) => Number(n))]
}

function isOutRange(x,y){
    if (x <0 || y <0 || x > n || y > m){
        return true
    }
    return false
}
dx=[0,1,0,-1]
dy=[1,0,-1,0]

function bfs(){
    let queue=[]
    queue.push([[1,1], 1]);
    while(queue.length > 0){
        let [[cur_x, cur_y], cur_cnt] = queue.shift()
        if (cur_x == n && cur_y == m ){
            return cur_cnt
        }
        for (let i=0;i<4;i++){
            _x = cur_x+dx[i]
            _y = cur_y+dy[i]
            if (!isOutRange(_x, _y)){
                if (inputArr[_x][_y] == 1){
                    queue.push([[_x, _y], cur_cnt+1])
                }
            }
        }
    }
}
console.log(bfs())