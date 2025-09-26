def solution(board, aloc):
    dd = [[-1,0],[1,0],[0,-1],[0,1]]

    for dr, dc in dd:
        r,c = aloc[0] + dr, aloc[1] + dc
        if in_range(r,c) and board[r][c] == 1:
            return 1
    return 0

def in_range(r,c):
    return 0 <= r <= 4 and 0 <= c <= 4

board = list(list(map(int, input().split())) for _ in range(5))
aloc = list(map(int, input().split()))
print(solution(board, aloc))
