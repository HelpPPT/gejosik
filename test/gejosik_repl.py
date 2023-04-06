import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gejosik import Gejosik

g = Gejosik()

while True:
    t = input()
    print(g.sentence(t))