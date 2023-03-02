import gurobipy as gp
from gurobipy import GRB
import time

L = 999996666111333

# 数据结构
I = [1, 2]  # product
M = [1, 2, 3, 4, 5]  # machine
P = [1, 2, 3, 4, 5]  # pallet
F = [1, 2, 3]  # fixture
E_f = {1: 1, 2: 2, 3: 3}  # fixture load unload time
O_ij = {1: [1, 2], 2: [1, 2, 3]}  # 工件_工序
F_ij = {(1, 1): [1, 2], (1, 2): [3], (2, 1): [1, 2, 3], (2, 2): [2], (2, 3): [1, 3]}  # 每道工序的可用夹具
M_ij = {(1, 1): [1, 2, 3, 4, 5], (1, 2): [2, 4], (2, 1): [1, 3, 5], (2, 2): [1, 2, 3],
        (2, 3): [2, 3, 4, 5], }  # 每道工具的可选机器
T_ijm = {(1, 1, 1): 2, (1, 1, 2): 6, (1, 1, 3): 5, (1, 1, 4): 3, (1, 1, 5): 4,
         (1, 2, 2): 8, (1, 2, 4): 4,
         (2, 1, 1): 3, (2, 1, 3): 6, (2, 1, 5): 5,
         (2, 2, 1): 4, (2, 2, 2): 6, (2, 2, 3): 5,
         (2, 3, 2): 7, (2, 3, 3): 11, (2, 3, 4): 5, (2, 3, 5): 8}  # 每道工序在可选机器上的加工时间

# 如果工序O_ij可以用夹具f夹持，则D_ijf=1，否则D_ijf=0
B_ijf = {}
for i in I:
    for j in O_ij[i]:
        for f in F:
            if f in F_ij[(i, j)]:
                B_ijf[(i, j, f)] = 1
            else:
                B_ijf[(i, j, f)] = 0

print(B_ijf)

# 如果工序O_ij可以在机器m上加工，则W_ijm=1，否则W_ijm=0
W_ijm = {}
for i in I:
    for j in O_ij[i]:
        for m in M:
            if m in M_ij[(i, j)]:
                W_ijm[(i, j, m)] = 1
            else:
                W_ijm[(i, j, m)] = 0

# 同一台机器上的两道工序先后顺序
Y_ijgk = {}
Y_ijgkm = []
for i in I:
    for j in O_ij[i]:
        for g in I:
            if i < g:
                for k in O_ij[g]:
                    __interSet = set(M_ij[(i, j)]).intersection(set(M_ij[(g, k)]))
                    if len(__interSet) > 0:
                        Y_ijgk[(i, j, g, k)] = list(__interSet)
                        for m in Y_ijgk[(i, j, g, k)]:
                            Y_ijgkm.append((i, j, g, k, m))
            # 同一个工件
            elif i == g:
                for k in O_ij[g]:
                    if j < k:
                        __interSet = set(M_ij[(i, j)]).intersection(set(M_ij[(g, k)]))
                        if len(__interSet) > 0:
                            Y_ijgk[(i, j, g, k)] = list(__interSet)
                            for m in Y_ijgk[(i, j, g, k)]:
                                Y_ijgkm.append((i, j, g, k, m))
Y_ijgkm = gp.tuplelist(Y_ijgkm)
# 用同一个夹具的两道工序的先后顺序
Z_ijgk = {}
Z_ijgkf = []
for i in I:
    for j in O_ij[i]:
        for g in I:
            if i < g:
                for k in O_ij[g]:
                    __interSet = set(F_ij[(i, j)]).intersection(set(F_ij[(g, k)]))
                    if len(__interSet) > 0:
                        Z_ijgk[(i, j, g, k)] = list(__interSet)
                        for f in Z_ijgk[(i, j, g, k)]:
                            Z_ijgkf.append((i, j, g, k, f))
            # 同一个工件
            elif i == g:
                for k in O_ij[g]:
                    if j < k:
                        __interSet = set(F_ij[(i, j)]).intersection(set(F_ij[(g, k)]))
                        if len(__interSet) > 0:
                            Z_ijgk[(i, j, g, k)] = list(__interSet)
                            for f in Z_ijgk[(i, j, g, k)]:
                                Z_ijgkf.append((i, j, g, k, f))
Z_ijgkf = gp.tuplelist(Z_ijgkf)
# 定义变量X_ijm
X_ijm = []
for i in I:
    for j in O_ij[i]:
        for m in M_ij[(i, j)]:
            X_ijm.append((i, j, m))
X_ijm = gp.tuplelist(X_ijm)
# 定义变量A_ijf
A_ijf = []
for i in I:
    for j in O_ij[i]:
        for f in F:
            A_ijf.append((i, j, f))
A_ijf = gp.tuplelist(A_ijf)

# 模型建立
Model = gp.Model("DRFJSP_2")

# 定义变量
X_ijm = Model.addVars(X_ijm, vtype=GRB.BINARY, name="X_ijm")
Y_ijgkm = Model.addVars(Y_ijgkm, vtype=GRB.BINARY, name="Y_ijgkm")
A_ijf = Model.addVars(A_ijf, vtype=GRB.BINARY, name="A_ijf")
Z_ijgkf = Model.addVars(Z_ijgkf, vtype=GRB.BINARY, name="Z_ijgkf")
C_i = Model.addVars(I, vtype=GRB.CONTINUOUS, name="C_i", lb=0.0)
s_ij = Model.addVars(M_ij.keys(), vtype=GRB.CONTINUOUS, name="start_time", lb=0.0)
c_ij = Model.addVars(M_ij.keys(), vtype=GRB.CONTINUOUS, name="complete_time", lb=0.0)
FT_ij = Model.addVars(M_ij.keys(), vtype=GRB.CONTINUOUS, name="load and unload time", lb=0.0)
C_max = Model.addVar(vtype=GRB.CONTINUOUS, name="max_complete_time", lb=0.0)

# （1） 同一时刻，某道工序只能被其可选设备集中的一个机器加工。
Model.addConstrs((X_ijm.sum(i, j, "*") == 1 for (i, j) in M_ij.keys()))

# （2） 同一时刻，一道工序只能使用一个夹具。
Model.addConstrs((A_ijf.sum(i, j, "*") == 1 for (i, j) in F_ij.keys()))

for i in I:
    for j in O_ij[i]:
        for f in F:
            if f not in F_ij[i, j]:
                A_ijf[(i, j, f)] = 0
# （3） 某道工序夹具装卸时间
for i in I:
    for j in O_ij[i]:
        for f in F:
            if 1 < j < len(O_ij[i]):
                Model.addConstr(gp.quicksum(E_f[f] * (1 - A_ijf[i, j, f] * A_ijf[i, (j - 1), f]) for f in F) +
                                gp.quicksum(E_f[f] * (1 - A_ijf[i, j, f] * A_ijf[i, (j + 1), f]) for f in F) == FT_ij[
                                    (i, j)])
            if j == 1:
                Model.addConstr(
                    gp.quicksum(E_f[f] * (2 - A_ijf[i, j, f] * A_ijf[i, (j + 1), f]) for f in F) == FT_ij[(i, j)])
            if j == len(O_ij[i]):
                Model.addConstr(
                    gp.quicksum(E_f[f] * (2 - A_ijf[i, j, f] * A_ijf[i, (j - 1), f]) for f in F) == FT_ij[(i, j)])

# （4） 同一时刻，同一夹具只能夹持一个工件。
for i in I:
    for j in O_ij[i]:
        for g in I:
            if i <= g:  # 不同工件
                for k in O_ij[g]:
                    __interSet = set(F_ij[(i, j)]).intersection(set(F_ij[(g, k)]))
                    if (len(__interSet) > 0) and ((i, j, g, k) in Z_ijgk.keys()):
                        for f in Z_ijgk[(i, j, g, k)]:
                            Model.addConstr(s_ij[i, j] + FT_ij[(i, j)] + gp.quicksum(
                                T_ijm[i, j, m] * X_ijm[i, j, m] for m in M_ij[(i, j)]) <= s_ij[(g, k)] + (
                                                        2 - A_ijf[(i, j, f)] - A_ijf[(g, k, f)]) * L + (
                                                        1 - Z_ijgkf[(i, j, g, k, f)]) * L)

# （5） 同一时刻，同一台机器上只允许有一个工件的某道工序在加工。
for i in I:
    for j in O_ij[i]:
        for g in I:
            if i <= g:
                for k in O_ij[g]:
                    __interSet = set(M_ij[(i, j)]).intersection(set(M_ij[(g, k)]))
                    if len(__interSet) > 0 and ((i, j, g, k) in Z_ijgk.keys()):
                        for m in Y_ijgk[(i, j, g, k)]:
                            Model.addConstr(s_ij[i, j] + FT_ij[(i, j)] + gp.quicksum(
                                T_ijm[i, j, m] * X_ijm[i, j, m] for m in M_ij[(i, j)]) <= (
                                                        s_ij[(g, k)] + (2 - X_ijm[(i, j, m)] - X_ijm[(g, k, m)]) * L + (
                                                            1 - Y_ijgkm[(i, j, g, k, m)]) * L))
                            Model.addConstr(X_ijm[(i, j, m)] + X_ijm[(g, k, m)] - 1 <= Y_ijgkm[(i, j, g, k, m)])
                            Model.addConstr(Y_ijgkm[(i, j, g, k, m)] <= X_ijm[(i, j, m)])
                            Model.addConstr(Y_ijgkm[(i, j, g, k, m)] <= X_ijm[(g, k, m)])

# （6） 某道工序开始加工的时间与在对应机器上加工时间的和不超过完成加工的时间
for i in I:
    for j in O_ij[i]:
        for m in M_ij[(i, j)]:
            Model.addConstr(
                s_ij[(i, j)] + FT_ij[(i, j)] + gp.quicksum(T_ijm[i, j, m] * X_ijm[i, j, m] for m in M_ij[i, j]) <= c_ij[
                    (i, j)])

# （7） 同个工件的两道工序之间有先后顺序。
for i in I:
    q_i = len(O_ij[i])
    for j in O_ij[i]:
        if (j + 1) <= q_i:
            Model.addConstr(c_ij[i, j] <= s_ij[i, (j + 1)])

# （7） 决策变量之间的关系
for i in I:
    for j in O_ij[i]:
        for f in F_ij[(i, j)]:
            Model.addConstr(A_ijf[(i, j, f)] <= B_ijf[(i, j, f)])
for i in I:
    for j in O_ij[i]:
        for m in M_ij[(i, j)]:
            Model.addConstr(X_ijm[(i, j, m)] <= W_ijm[(i, j, m)])

for i in I:
    for j in O_ij[i]:
        for g in I:
            if i <= g:  # 不同工件或相同工件
                for k in O_ij[g]:
                    __interSet = set(F_ij[(i, j)]).intersection(set(F_ij[(g, k)]))
                    if len(__interSet) > 0 and ((i, j, g, k) in Z_ijgk.keys()):
                        for f in Z_ijgk[(i, j, g, k)]:
                            Model.addConstr(A_ijf[i, j, f] + A_ijf[g, k, f] - 1 <= Z_ijgkf[(i, j, g, k, f)])
                            Model.addConstr(Z_ijgkf[i, j, g, k, f] <= A_ijf[(i, j, f)])
                            Model.addConstr(Z_ijgkf[i, j, g, k, f] <= A_ijf[(g, k, f)])

# （8） 每个工件最后一道工序的完工时间不超过该工件的完工时间。
for i in I:
    q_i = len(O_ij[i])
    Model.addConstr(c_ij[(i, q_i)] <= C_i[i])
    Model.addConstr(C_max >= C_i[i])
# 目标函数
Model.setObjective(C_max, gp.GRB.MINIMIZE)

# start_time = time.time()
# Model.Params.LogToConsole = True
# Model.Params.TimeLimit = 300
Model.update()
Model.optimize()

print("Optimal Objective Value", Model.objVal)
# 查看变量取值
for var in Model.getVars():
    print(f"{var.varName}: {round(var.X, 3)}")
