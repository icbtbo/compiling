#计算状态集T的闭包S并作为函数的返回值，X是转换关系，SE是终止状态集
def closure(X,T,SE,f):
    s = set()
    stack = list()
    for t in T:
        stack.append(t) # 该列表中的值用来求经过‘n'弧（即空弧）后的状态
        s.add(t) # 存储状态集T的闭包
    while stack:
        t = stack.pop()
        if 'n' in X[t]:
           u = X[t]['n']
           for i in u:
               if f == 0 :
                   if i in list(SE):
                        #f=1表示该状态集中有终止集sE中的状态
                        f=1                 
               if i not in s:
                   stack.append(i)
                   s.add(i)
    S = [i for i in s] 
    S.sort()
    #S = np.array(S)
    return S,f 
#获取状态集Si经过一条弧nn后到达的新状态集s0
def gets(X,Si,nn,f):
    s= set()
    # Si = list(Si)
    for t in Si:
        if nn in X[t]:
            u = X[t][nn]
            for i in u:
                if f == 0 :
                   if i in list(SE):
                       f=1
                if i not in s:
                    s.add(i)
    S = [i for i in s]
    S.sort()
    return S , f
#A是字母表，X转移矩阵，S0是初态集合，SE是终态集合
def toDFA(A,X,S0,SE):
    s0,f = closure(X,S0,SE,0)
    s = list()
    # s用来存放所有的状态集，之后用来判断转化后的状态集是否已存在
    s.append(s0) 
    x = list()
    Id = 0
    sE = list()
    while (len(s) > Id): # 判断所有状态集是否已转换完毕
        T = s[Id]
        xi= {}
        for n in A:
            Ti , f = gets(X,T,n,0)
            si,f = closure(X,Ti,SE,f)
            if si not in s and si:
                if f==1:
                    sE.append(si)
                s.append(si)
            xi[n] = si
        x.append(xi)
        Id = Id + 1
    return s , x , s0 , sE  # s是状态集合，x是转化关系

''' dfa转化测试数据'''

A = ['a','b']

# 转换关系数据格式，例如X[0]['n']=[1,7] 表示 状态0经过弧 ’n' 到达 状态0或7
X = [{'n':[1,7],'a':[],'b':[]},
     {'n':[2,4],'a':[],'b':[]},
     {'a':[3],'n':[],'b':[]},
     {'n':[6],'a':[],'b':[]},
     {'b':[5],'n':[],'a':[]},
     {'n':[6],'a':[],'b':[]},
     {'n':[1,7],'a':[],'b':[]},
     {'a':[8],'n':[],'b':[]},
     {'b':[9],'n':[],'a':[]},
     {'b':[10],'n':[],'a':[]},
     {}]
S = [0,1,2,3,4,5,6,7,8,9,10]
S0 = [0]
SE = set()
SE.add(10)
s , x , s0 , sE = toDFA(A,X,S0,SE)
print("转换后形成的DFA")
print ("字母表:")
print (A)
print ("状态集合:")
print (s)
print ("初始状态:")
print (s0)
print ("终结状态集合:")
print (sE)
print ("f:")
print (x)
