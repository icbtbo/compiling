from collections import namedtuple

# rule 是要分析的文法的产生式
rule = namedtuple('rule',['name','list'])
# item 是项目集中每一个项目的一部分（不包括向前搜索符）left 为产生式中点左边的部分，right 是右边
item = namedtuple('item',['name','left','right'])  

class  LR0(object):
    def __init__(self,vt=None,vn=None,rl=None):
        self.rules = rl if rl else []
        self.Vt = vt if vt else []
        self.Vn = vn if vn else []
        self.V = self.Vt + self.Vn

    def First(self,x):
        'Return a list of First'
        if x in self.Vt:
            return [x,]
        first = []
        for i in [repl[0] for name,repl in self.rules if name == x and name != repl[0]]:
            first.extend(self.First(i))
        return list(set(first))
    
    def Follow(self,x):
        pass

    def Closure(self,I):
        pass

class LALR1(LR0):
    'Create a LALR1 class extends LR0'
    def Closure(self,I):
        n = 0
        while n < len(I):
            g,h,n = I[n][0],I[n][1],n+1 # g 是每个LALR1项目的左半部分（产生式），h 是向前搜索符
            if g.right and g.right[0] in self.Vn:
                for name,repl in self.rules:
                    if name == g.right[0]:
                        x=item(name,[],repl)
                        for u in I:
                            if u[0] == x:
                                u[1] = list(set(u[1] + (self.First(g.right[1]) if len(g.right) > 1 else h)))
                                break
                        else:
                            I.append([x,self.First(g.right[1]) if len(g.right) > 1 else h])
        return I
    
    def Goto(self,I,X):
        J = []
        for g,h in I:
            if g.right and g.right[0] == X:
                J.append([item(g.name,g.left + g.right[:1],g.right[1:]),h])
        return self.Closure(J)

def make_table():
    'Return table, index_char, rule'
    # 将文法的产生式及终结符、非终结符等信息传给lr对象，实现初始化
    lr = LALR1(
        ['i','+','*','(',')'],
        ['E','T','F'],
        [
            rule('E1',['E',]),
            rule('E',['E','+','T']),
            rule('E',['T',]),
            rule('T',['T','*','F']),
            rule('T',['F',]),
            rule('F',['(','E',')']),
            rule('F',['i',])
        ]
    )

    # 构造分析表
    # 分析表初始化
    table=[[-1 for i in range(len(lr.V)+1)]]

    # 创建初始项目集 I0
    I0 = lr.Closure([[item('E1',[],['E']),['#']]])
 
    i = 0
    L = [I0,]  # 初始化项目集
    while i < len(L):
        I = L[i]
        for t,x in enumerate(lr.V):
            J = lr.Goto(I,x)
            for j in range(len(L)):
                if L[j] == J:
                    if x in lr.Vt:
                        table[i][t] = j
                    else:
                        table[i][t+1] = j
                    break
            else:
                L.append(J)
                table.append([-1 for v in range(len(lr.V)+1)])
                # n = lr.V.index(x)
                if x in lr.Vt:
                    table[i][t] = j+1
                else:
                    table[i][t+1] = j+1
        i += 1

    temp = lr.Vt[:]  # 获得lr.Vt 这个列表的一个副本，使其不会影响原列表
    temp.append('#')
    for i,I in enumerate(L):
        for x,y in I:
            if not x.right:
                if x.name == 'E1':
                    table[i][len(lr.Vt)] = 100 # 即acc
                else:
                    for j,t in enumerate(lr.rules): 
                        if x.name == t.name and x.left == t.list:
                            # y = lr.V.index(y)
                            # table[i][y+1]   # 加1是因为在table列中插入了‘#’所对应的内容
                            for k,z in enumerate(temp):
                                if z in y:
                                    # print(k)
                                    table[i][k] = 101 + j -1  # 减一是因为文法经过了拓展

    # 构造符号列表(包括“#”)
    index_char = temp+lr.Vn

    # 构造 rule 表，以此记录每个产生式规约时符号栈需弹出的符号个数
    r = [
        [name,len(repl)] for name,repl in lr.rules if name != "E1"
    ]

    print(index_char,r)
    return table,index_char,r




if __name__ == "__main__":
    make_table()



    

