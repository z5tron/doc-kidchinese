import sys
import os
import subprocess

chars = []
for line in open(sys.argv[1], 'r').readlines():
    for w in line.strip().split():
        if w in chars: continue
        chars.append(w)
target='char-practice-body.tex'
if os.path.exists(target):
    os.rename(target, target +".orig")

with open(target, 'w') as f:
    for w in chars:
        # f.write("\\miline{%s}\n" % w)
        f.write("\\milinelvb{%s}\n" % w)

subprocess.check_call("xelatex char-practice.tex", shell=True)
