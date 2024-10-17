import sys, os

current_file= __file__
filedir = os.path.join(os.getcwd(), "Temp")
filename =sys.argv[0]
filepath = os.path.join(filedir, filename)
print(current_file, filepath, filedir)
vboxuser
changeme