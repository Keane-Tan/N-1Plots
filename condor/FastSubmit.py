import os
import time

os.system("tar -zcvf N1Analysis.tgz N1Analysis")
os.system("xrdcp -f N1Analysis.tgz root://cmseos.fnal.gov//store/user/keanet/CondorOutput/N1Analysis.tgz")

ffile = open('fileIDList.txt','r+')
fileIDList = ffile.readlines()


for i in range(len(fileIDList)):
	rfile = open('submit.jdl','r+')
	f1 = rfile.readlines()

	fileID = fileIDList[i]

	f1[10] = list(f1[10])[:-1]    
	f1[10] = f1[10][:12] + list(fileID)

	f1[10] = ''.join(f1[10])

	print f1[10]
	rfile.seek(0)
	rfile.writelines(f1)
	rfile.truncate()
	rfile.close()

	time.sleep(3)
	os.system("condor_submit submit.jdl")

	time.sleep(10)

ffile.close()
