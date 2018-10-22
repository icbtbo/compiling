import re  
 
class Token(object):
 
    #初始化
    def __init__(this): 
        #行号，用于最后输出
        this.lineno = 1
 
        # 正则表达式
        #保留字
        Keyword = r'(?P<Keyword>(auto){1}|(double){1}|(int){1}|(if){1}|' \
		          r'(#include){1}|(return){1}|(char){1}|(stdio\.h){1}|(const){1}|(then){1}|(else){1}|(repeat){1}|(until){1})'\
                  r'(write){1}|(read){1}'
        #运算符
        Operator = r'(?P<Operator>\+\+|\+=|\+|--|-=|-|\*=|/=|/|%=|%)'
 
         #分隔符/界符
        Separator = r'(?P<Separator>[,:\{}:)(<>])'
        
         #数字: 例如：1 1.9
        Number = r'(?P<Number>\d+[.]?\d+)'
 
         #变量名 不能使用关键字命名
        ID = r'(?P<ID>[a-zA-Z_][a-zA-Z_0-9]*)'
 
         #方法名 {1} 重复n次
        Method = r'(?P<Method>(main){1}|(printf){1})'
 
         #错误  
        Error = r'\"(?P<Error>.*)\"'
 
         #注释  ^匹配行的开始 .匹配换行符以外的任意字符 \r回车符 \n换行符
        Annotation = r'(?P<Annotation>/\*(.|[\r\n])*/|//[^\n]*)'
 
         #进行组装，将上述正则表达式以逻辑的方式进行拼接, 按照一定的逻辑顺序
         # compile函数用于编译正则表达式，生成一个正则表达式对象
        this.patterns = re.compile('|'.join([Annotation, Keyword, Method, ID, Number, Separator, Operator, Error])) 
 
    #with后面的代码块全部被执行完之后将自动关闭所获得的文件权柄
    #读文件
    def read_file(this, filename):
         with open(filename, "r") as f_input: # “r”表示以只读方式打开文件
               return [line.strip() for line in f_input]
 
    #结果写入文件
    def write_file(this, lines, filename = 'D:/results.txt'):
        with open(filename, "a") as f_output: # "a"表示打开一个文件用于追加。若文件已存在，文件指针将会放在文件的结尾，否则创建一个新文件
                for line in lines:
                    if line:
                        f_output.write(line)
                    else:
                        continue
 
    def get_token(this, line):
 
        #finditer : 在字符串中找到正则表达式所匹配的所有字串， 并把他们作为一个迭代器返回
        for match in re.finditer(this.patterns, line):
 
            #group()：匹配的整个表达式的字符 # yield 关键字：类似return ，返回的是一个生成器，generator
            yield (match.lastgroup, match.group())
 
    def run(this, line, flag=True):
        for token in this.get_token(line):
            if flag:
                print ("line %3d :" % this.lineno, token)

if __name__=='__main__':
         token = Token()
         filepath = "C:\\Users\\icbtbo\\Desktop\\test.c" #要分析的代码所在的文件路径
 
         lines = token.read_file(filepath)
 
         for line in lines:
             token.run(line, True)
 
             #写入指定文件中,选择此方式时(flag=False)不在终端中打印
             #token.write_file(token.run(line, False), "D:/results.txt")
             token.lineno += 1

