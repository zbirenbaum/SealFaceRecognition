import os

def compile(net):
    fname = 'final_results_{}.txt'.format(net)
    if os.path.exists(fname):
        os.remove(fname)

    with open(fname, 'a+') as f: 
        for i in range(10):
            curr = open('log/result_{}_{}.txt'.format(net, i+1))
            lines = curr.read()
            f.write(lines)
            f.write('\n')


def main():
    compile('prim')
    compile('seal') 

if __name__=='__main__':
    main()
