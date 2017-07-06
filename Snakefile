rule all:
    output:
        touch('foo.txt')
    run:
        print('Fooing foo:')


