from lexical_analyzer import getwords
# results = []
# # 从文件中读取字符串并将它转换成列表
# with open("test.txt","r") as f_input:
#     for line in f_input:
#         results.extend([i for i in line.strip()])
# print(results)


n = 0
flagerror = 0
words = getwords()


def match(ch):
    global n, words,flagerror
    if words[n][1] == ch:
        pass
        # print("OK")
    else:
        flagerror = 1
        return
    n = n + 1

def program():
    global flagerror
    print("program-->block")
    block()
    if flagerror == 1:
        print("出现错误，停止分析！\n")
        return

def block():
    global flagerror
    if flagerror == 1:
        return
    print("block-->{stmts}")
    match("{")
    stmts()
    match("}")

def stmts():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][1] == "}":
        print("stmts-->null")
        return
    print("stmts-->stmt stmts")
    stmt()
    stmts()

def stmt():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][0] == "ID":
        print("stmt-->id=expr;")
        match(words[n][1])
        match("=")
        expr()
        match(";")
    elif words[n][1] == "if":
        match("if")
        match("{")
        Bool()
        match("}")
        stmt()
        stmt1()
        # if words[n][1] == "else":
        #     print("stmt-->if(bool) stmt else stmt")
        #     match("else")
        #     stmt()
        # else:
        #     print("smt-->if(bool) stmt")
    elif words[n][1] == "while":
        print("stmt-->while(bool) stmt")
        match("while")
        match("(")
        Bool()
        match(")")
        stmt()
    elif words[n][1] == "do":
        print("stmt-->do stmt while(bool)")
        match("do")
        stmt()
        match("while")
        match("(")
        Bool()
        match(")")
    elif words[n][1] == "break":
        print("stmt-->break")
        match("break")
    else:
        print("stmt-->block")
        block()

def stmt1():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][1] == "else":
        print("stmt-->if(bool) stmt else stmt")
        match("else")
        stmt()
    else:
        print("smt-->if(bool) stmt")

def Bool():
    global flagerror,words,n
    if flagerror == 1:
        return
    # expr()
    if words[n+1][1] == "<":
        print("bool-->expr < expr")
        expr()
        match("<")
        expr()
    elif words[n+1][1] == "<=":
        print("bool-->expr <= expr")
        expr()
        match("<=")
        expr()
    elif words[n+1][1] == ">":
        print("bool-->expr > expr")
        expr()
        match(">")
        expr()
    elif words[n+1][1] == ">=":
        print("bool-->expr >= expr")
        expr()
        match(">=")
        expr()
    else:
        print("bool-->expr")
        expr()

def expr():
    global flagerror,words,n
    if flagerror == 1:
        return
    print("expr-->term expr0")
    term()
    expr0()

def expr0():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][1] == "+":
        print("expr0-->+ term expr0")
        match("+")
        term()
        expr0()
    elif words[n][1] == "-":
        print("expr0-->- term expr0")
        match("-")
        term()
        expr0()
    else:
        print("expr0-->null")

def term():
    global flagerror,words,n
    if flagerror == 1:
        return
    print("term-->factor term0")
    factor()
    term0()

def term0():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][1] == "*":
        print("term0-->*factor term0")
        match("*")
        factor()
        term0()
    elif words[n][1] == "/":
        print("term0-->/factor term0")
        match("/")
        factor()
        term0()
    else:
        print("term0-->null")
        return

def factor():
    global flagerror,words,n
    if flagerror == 1:
        return
    if words[n][1] == "(":
        print("factor-->(expr)")
        match("(")
        expr()
        match(")")
    elif words[n][0] == "ID":
        print("factor-->id")
        match(words[n][1])
    elif words[n][0] == "Number":
        print("factor-->num")
        match(words[n][1])
    else:
        flagerror = 1

if __name__ == "__main__":
    program()

# 参照书上代码，发现顺序并不完全正确,所以稍微改了下，经检验顺序正确