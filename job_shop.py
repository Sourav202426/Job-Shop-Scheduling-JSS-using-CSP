def domain(jobs):
    time=0
    for j in jobs:
        for t in j:
            time+=t[1]
    domain={}
    for i in range(len(jobs)):
        j=jobs[i]
        for t in range(len(j)):
            domain[(i, t)]=set(range(time))
    return domain

def variables(jobs):
    vars=[]
    for j in range(len(jobs)):
        for t in range(len(jobs[j])):
            vars.append((j, t))
    return vars

def constraints(schedule,task,start,jobs):
    j,t=task
    m,d=jobs[j][t]
    if t>0:
        p_end=schedule.get((j,t-1))
        if p_end is not None:
            p_end += jobs[j][t-1][1]
            if start<p_end:
                return False
    for otask in schedule:
        s=schedule[otask]
        if s is None:
            continue
        oj,ot=otask
        om,od=jobs[oj][ot]
        if om==m:
            oend=s+od
            if not (start>=oend or start+d<=s):
                return False
    return True

def backtracking(schedule,vars,jobs,dom):
    if len(vars)==0:
        return schedule
    task=vars.pop(0)
    for s in dom[task]:
        if constraints(schedule,task,s,jobs):
            schedule[task]=s
            r=backtracking(schedule,vars,jobs,dom)
            #valid schedule has been found
            if r is not None:
                return r
            schedule[task]=None
    return None

def solve(jobs):
    v=variables(jobs)
    schedule={}
    for i in range(len(v)):
        schedule[v[i]]=None
    d=domain(jobs)
    solution=backtracking(schedule,v,jobs,d)
    return solution

jobs = [[(0,3),(1,2),(2,2)],
        [(0,2),(2,1),(1,4)],
        [(1,4),(2,3)]]

solution = solve(jobs)

if solution:
    print("Optimal Schedule:")
    for task,start in sorted(solution.items()):
        j,t=task
        m,d=jobs[j][t]
        end=start+d
        print(f"Job {task[0]}, Task {task[1]} on Machine {m} starts at {start} and ends at {end}.")
else:
    print("No solution found.")
