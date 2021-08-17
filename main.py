import os

def isdir(path):return (1 if os.path.isdir(path) else 0)
def zfill(n):return str(n).zfill(6)

cwd = os.path.dirname(os.path.abspath(__file__))

inf = 200000
meta, name, parent, value = [0]*inf, ['']*inf, [0]*inf, ['']*inf
dirs = []
pathmap = {}

def listup_path(nowpath):
    dirs.append(nowpath)
    if os.path.isdir(nowpath):
        for item in os.listdir(nowpath):
            next_path = '%s/%s'%(nowpath, item)
            listup_path(next_path)

def export(nowPath, parentPath):
    global cwd, meta, name, parent, value
    print(nowPath)
    if cwd == parentPath:
        meta[pathmap[nowPath]] = 1
        parent[pathmap[nowPath]] = 999999
    else:
        meta[pathmap[nowPath]] = isdir(nowPath)
        name[pathmap[nowPath]] = nowPath.split('/')[-1]
        parent[pathmap[nowPath]] = pathmap[parentPath]+1
        value[pathmap[parentPath]] += zfill(pathmap[nowPath]+1)
        

    if os.path.isdir(nowPath):
        for item in sorted(os.listdir(nowPath)):
            export('%s/%s'%(nowPath, item), nowPath)
    else:
        with open(nowPath, 'r', encoding='utf-8') as f:
            value[pathmap[nowPath]] = f.read().replace('\n','')

# 実行

listup_path('%s/fs2_root'%cwd)
pathmap = {dirs[i]:i for i in range(len(dirs))}
export('%s/fs2_root'%cwd, cwd)
output = ['']*len(dirs)
for i in range(len(output)): output[i] = '%s/%s/%s/%s/'%(meta[i], name[i], parent[i], value[i])
with open('%s/output.txt'%cwd,'w',encoding='utf-8') as f:f.write('\n'.join(output))