const fs = require('fs')
let input = fs.readFileSync(0).toString().split('\n')

let n = Number(input[0])
let inputArr = []
let visited=[]

for (let i=0;i<n;i++){
    inputArr.push(input[i+1].split(' ').map((n)=> Number(n)))
    visited.push(new Array(n).fill(0))
}

const dx=[0,1,0,-1]
const dy=[1,0,-1,0]

function dfs(x,y){
    let cnt =1 
    visited[x][y] =1
    for (let i=0;i<4;i++){
        let _x = x+dx[i]
        let _y = y+dy[i]
        if (_x< 0 || _y <0 || _x>= n || _y>= n){
            continue
        }
        if (inputArr[_x][_y] == 1 && visited[_x][_y] == 0){
            cnt+=dfs(_x, _y)
        }
    }
    return cnt
}
let answerArr=[]
for (let i=0;i<n;i++){
    for (let j=0;j<n;j++){
        if (inputArr[i][j] == 1 && visited[i][j] == 0){
            let answer = dfs(i,j)
            answerArr.push(answer)
        }
    }
}

answerArr.sort((a,b)=> a-b)
console.log(answerArr.length)
for (let i=0;i<answerArr.length;i++){
    console.log(answerArr[i])
}