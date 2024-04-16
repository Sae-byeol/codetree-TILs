const fs = require('fs')
let input = fs.readFileSync(0).toString().split("\n");

const [n,m,start_node] = input[0].split(' ').map((i) => Number(i));
let graph = Array.from({length: n+1}, ()=> [])
let visited = new Array(n+1).fill(0)


//그래프 만들기
for (let i=1; i<=m; i++){
    const [node1, node2] = input[i].split(' ').map((n)=> Number(n));
    graph[node1].push(node2);
}
//그래프 각 원소 배열 정렬
for (let i=1; i<=n;i++){
    graph[i].sort((a,b) => a-b);
}

let dfsAnswer = [start_node]
let bfsAnswer = []
function dfs(node){
    visited[node] =1; 
    let nodeArray = graph[node];
    for (let i=0;i< nodeArray.length ; i++){
        if (visited[nodeArray[i]] == 0){
            dfsAnswer.push(nodeArray[i]);
            dfs(nodeArray[i]);
        }
    }
}


function bfs(){
    //dfs에서 건든 visited 초기화
    visited.forEach((v, i) => visited[i] =0)
    let queue =[start_node]
    while (queue.length > 0){
        let cur = queue.shift()
        bfsAnswer.push(cur)
        for (let i=0;i<graph[cur].length ; i++){
            //아직 방문 안했다면(큐에 없다면)
            if (visited[graph[cur][i]] == 0){
                visited[graph[cur][i]] =1
                queue.push(graph[cur][i])
            }
        }
    }
}

dfs(start_node)
bfs()
console.log(dfsAnswer.join(" "))
console.log(bfsAnswer.join(' '))