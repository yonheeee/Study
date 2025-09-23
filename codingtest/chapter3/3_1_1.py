def solution(n, m, A, B):
    answer=[]

    for k in B:
        cnt = 0
        for a in A:
            if a>k:
                cnt+=1
        answer.append(cnt)
    return answer

n,m = map(int,input().split())
A = list(map(int, input().split()) for _ in range(n))  
B = list(int(input()) for _ in range(m)) 
C= solution(n, m, A, B)
for c in C:
    print(c)