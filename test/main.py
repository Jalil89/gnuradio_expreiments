from child import Child

def makecallback(f):
    f()
    

x = Child()
makecallback(x.callback)