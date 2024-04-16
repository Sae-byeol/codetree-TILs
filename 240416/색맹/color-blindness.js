const fs = require('fs')
let input = fs.readFileSync(0).toString().split("\n");
let n = Number(input[0])
let nonBlindArr=[]
let blindArr=Array.from({length: n}, ()=> new Array(n))

let nonBlind=0
let blind=0

for (let i=1;i<=n;i++){
    nonBlindArr.push(input[i].split(''))
}

// 색맹용 배열
for (let i=0;i<n;i++){
    for (let j=0;j<n;j++){
        if (nonBlindArr[i][j] == 'G'){
            blindArr[i][j] = 'R'
        }
        else{
            blindArr[i][j] = nonBlindArr[i][j]
        }
    }
}

const dx=[0,1,0,-1]
const dy=[1,0,-1,0]

function isOutRange(x, y){
    if (x <0 || y <0 || x >= n || y >= n){
        return true
    }
    return false
}
let queue=[]

//같은 색상 찾아 뻗어나가기 위한 함수
function bfs(color, arr){
    while (queue.length >0){
        curIndex = queue.shift()
        for (let i=0;i<4;i++){
            _x = curIndex[0]+dx[i]
            _y = curIndex[1]+dy[i]
            if (!isOutRange(_x, _y)){
                if (arr[_x][_y] == color){
                    arr[_x][_y] = -1 // 방문처리
                    queue.push([_x, _y])
                }
            }
        }
    }
}

let nonBlindAnswer =0
let blindAnswer=0

//방문여부 배열 따로 두지 않고 색상배열에서 -1로 변경하는 것으로 함

//1. 일반인
for (let i=0;i<n;i++){
    for (let j=0;j<n;j++){
        if (nonBlindArr[i][j] != -1){
            //방문 전이라면
            color = nonBlindArr[i][j]
            nonBlindArr[i][j] = -1 
            queue.push([i,j])
            bfs(color, nonBlindArr) //시작
            //bfs 한번 다녀오면 cnt +1 
            nonBlindAnswer++;
        }
    }
} //모든점에 대해 탐색

//2. 색맹
for (let i=0;i<n;i++){
    for (let j=0;j<n;j++){
        if (blindArr[i][j] != -1){
            //방문 전이라면
            color = blindArr[i][j]
            blindArr[i][j] = -1 
            queue.push([i,j])
            bfs(color, blindArr) //시작
            //bfs 한번 다녀오면 cnt +1 
            blindAnswer++;
        }
    }
}

console.log(nonBlindAnswer+' '+ blindAnswer)