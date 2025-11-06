def solution(A):
    solve(A,0)

#앞부분 0을 제거한 상태로 출력 위함
def solve(A,B):
    if A != 0:
        if A%10 !=0 or B == 1:
            print(A%10, end='')
            B = 1
        
        solve(A // 10, B)

A = int(input())
solution(A)