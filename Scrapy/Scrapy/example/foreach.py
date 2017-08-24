def foreach():
    print 'iteration:'
    m1 = (x1 ** 2 for x1 in range(10))
    print sorted(m1)

    print '\r\n dictionary iteration:'
    m2 = {x2:x2 ** 2 for x2 in range(10)}
    print m2

    print '\r\nprint 11 to 16'
    print range(11, 17)

def useYield():
    for x in range(10):
        yield x

foreach()

i = useYield()
print next(i)
print next(i)
print next(i)
print next(i)
print next(i)