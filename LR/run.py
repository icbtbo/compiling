from LALR1_maker import make_table 

class Stack:
    # 栈初始化
    def __init__(self,lst):
        self.items = lst

    # 返回一个包含栈中所有值的迭代器
    def iter(self):
        for i in range(len(self.items)):
            yield self.items[i]
    
    # 返回栈中所有元素组成的字符串
    def getstr(self):
        return "".join(list(self.iter()))

    def isEmpty(self):
        return len(self.items) == 0

    def get_top(self):
        if self.isEmpty():
            raise KeyError("The stack is empty")
        
        return self.items[len(self.items)-1]

    def push(self,item):
        self.items.append(item)

    def pop(self):
        if self.isEmpty():
            raise KeyError("The stack is empty")
        
        return self.items.pop()



# 获得分析表，符号表，以及rule表
table,index_char,rule = make_table()
## LR(1)分析表,12代表acc
# table = [
#     [5,-1,-1,4,-1,-1,1,2,3],
#     [-1,6,-1,-1,-1,12,-1,-1,-1],
#     [-1,22,7,-1,22,22,-1,-1,-1],
#     [-1,24,24,-1,24,24,-1,-1,-1],
#     [5,-1,-1,4,-1,-1,8,2,3],
#     [-1,26,26,-1,26,26,-1,-1,-1],
#     [5,-1,-1,4,-1,-1,-1,9,3],
#     [5,-1,-1,4,-1,-1,-1,-1,10],
#     [-1,6,-1,-1,11,-1,-1,-1,-1],
#     [-1,21,7,-1,21,21,-1,-1,-1],
#     [-1,23,23,-1,23,23,-1,-1,-1],
#     [-1,25,25,-1,25,25,-1,-1,-1]
# ]
# # 符号表
# index_char = ["i","+","*","(",")","#","E","T","F"]

# # 记录各产生式应出栈的元素个数及归约后的非终结符
# rule = [
#     ["E",3],["E",1],["T",3],["T",1],["F",3],["F",1]
# ]

def get_index_char(x):
    for i in range(len(index_char)):
        if index_char[i] == x:
            return i
    
    return -1

# 根据分析表获取下一步的动作
def goto_char(status,instr):
    x = instr.get_top()
    y = int(status.get_top())
    z = get_index_char(x)
    # print(y,"herey")
    # print(z,"herez")
    return table[y][z]

def action(status,symbol,instr):
    i = goto_char(status,instr)

    if(i == -1):
        raise KeyError("归约出错！")
    if(i == 100):
        print("归约成功！")
    if(0<=i<=99):
        status.push(str(i))
        a = instr.pop()
        symbol.push(a)
        print('{:<15}{:<15}{:<15}'.format(status.getstr(),symbol.getstr(),instr.getstr()[::-1]))
        # print(status.getstr()+"\t",symbol.getstr()+"\t",instr.getstr()[::-1])
        action(status,symbol,instr)
    if(101<=i):
        x = rule[i-101][1]
        for j in range(x):
            status.pop()
            symbol.pop()
        symbol.push(rule[i-101][0])
        a = status.get_top()
        b = get_index_char(symbol.get_top())
        n = table[int(a)][b]
        status.push(str(n))
        print('{:<15}{:<15}{:<15}'.format(status.getstr(),symbol.getstr(),instr.getstr()[::-1]))
        # print(status.getstr()+"\t",symbol.getstr()+"\t",instr.getstr()[::-1])
        action(status,symbol,instr)


def main():
    status = Stack(["0"])
    symbol = Stack(["#"])

    inputstr = input("请输入要归约的输入串，以‘#’字符结束！")
    instr = Stack(list(inputstr)[::-1])

    print("======================================")
    print('{:<12}{:<12}{:<12}'.format("状态栈","符号栈","输入串"))
    print('{:<15}{:<15}{:<15}'.format(status.getstr(),symbol.getstr(),instr.getstr()[::-1]))
    # print(status.getstr()+"\t",symbol.getstr()+"\t",instr.getstr()[::-1])
    action(status,symbol,instr)




if __name__ == "__main__":
    # s=Stack(["1","2","3"])
    # print(s.getstr())
    main()