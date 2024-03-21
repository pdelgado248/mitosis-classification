dataPath = '../../Data/jpg_videos'
from glob import glob as glob
import os
origDir = os.getcwd()

for folder1 in glob(dataPath+'/*'):

    for folder2 in glob(folder1+'/*'):
        os.chdir(folder2)

        print(glob('*'))
        for imName in glob('*'):
            #part = imName.rsplit('-',1)

            #Subtract 1 to the frame number to make them start at 1
            #instead of 0
            #prevNum = part[-1][:-4]
            #newNum=str(int(prevNum)+1)

 
            #os.rename(imName,'im-'+newNum+'.jpg')

        print(glob('*'))

        os.chdir(origDir)
