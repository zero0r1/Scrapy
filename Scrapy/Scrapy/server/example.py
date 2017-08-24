import threading
from dbhelp.DBEngine import DBEngine


mylist = [1,2,3,4,5,6]

def simple_generator_function():
    for i in mylist:
        yield i

def work(aa,vv):
    print next(vv)

def test():
    i = simple_generator_function()
    for x in range(3):
        lock = threading.Lock()
        thread = threading.Thread(target=work, args=(lock,i,))
        #self.outputLog("thread start...")
        #是否设置是后台线程
        #thread.setDaemon(True)
        thread.start()

#test()
def FindAndModify(colName,type):
    """
    插入数据capture cargo data
    """
    return DBEngine.findAndModify(colName,type,'w')

aa = []
aa = FindAndModify('capture_queue','001')
print 'done'