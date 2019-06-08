import sys
import os
import subprocess

target='char-practice-body.tex'
if os.path.exists(target):
    os.rename(target, target +".orig")

f = open(target, 'w')

iline, chars = 0, []
for line in open(sys.argv[1], 'r').readlines():
    line = line.strip()
    if not line: continue
    for i,w in enumerate(line.split()):
        if w in chars: continue
        if i == 0:
            # if iline > 0:
            #     f.write("\\clearpage\n\\newpage\n")
            f.write("\n\n{\\Large %s}\n\n" % w)
        else:
            # f.write("\\miline{%s}\n" % w)
            f.write("\\milinelvb{%s}\n" % w)
    iline += 1
f.close()


for i in range(2):
    subprocess.check_call("xelatex char-practice.tex", shell=True)

basename, ext = os.path.splitext(sys.argv[1])
newpdf = "{}.pdf".format(basename)
if os.path.exists(newpdf):
    os.rename(newpdf, "{}.orig.pdf".format(basename))
os.rename("char-practice.pdf", newpdf)
