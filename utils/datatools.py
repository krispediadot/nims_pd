import numpy as np
import pandas as pd
import os
import re

DATASETPATH = './dataset/'
DATA_CONTROL = os.path.join(DATASETPATH , 'Controls')
DATA_PD = os.path.join(DATASETPATH, 'PD')

def getPatientsTable() -> pd.DataFrame:
    patients = pd.read_csv(os.path.join(DATASETPATH, 'patients.csv'), encoding='utf-8')
    return patients

# 환자별 BW & FW 데이터 위치 확인
def getPatientDataPath(category: str, patient: str, mode="PREP") -> list:
    """
    :param category:
    :param patient:
    :param mode: PREP or STRN
    :return:
    """

    BW = []
    FW = []

    if category == "Controls":
        targetFolder = DATA_CONTROL
    else:
        targetFolder = DATA_PD

    files = os.listdir(targetFolder)

    p = re.compile(patient)
    idxs = list(filter(lambda x: p.search(files[x]) != None and files[x].startswith(mode), range(len(files))))

    for idx in idxs:
        f = files[idx]
        if f.split('_')[2].startswith('FW'):
            FW.append(os.path.join(targetFolder, f))
        else:
            BW.append(os.path.join(targetFolder, f))

    return BW, FW


# 환자별 BW & FW 데이터 가져오기
def getPatientData(category: str, patient: str, mode="PREP") -> pd.DataFrame:
    BW, FW = getPatientDataPath(category, patient, mode)

    BWdata = []
    FWdata = []

    for b in BW:
        df = pd.read_csv(b, encoding='utf-8')
        BWdata.append(df)
    #         print("컬럼 수:", len(df.columns), "위치 포인트 수:", int((len(df.columns)-2)/3))

    for f in FW:
        df = pd.read_csv(f, encoding='utf-8')
        FWdata.append(df)
    #         print("컬럼 수:", len(df.columns), "위치 포인트 수:", int((len(df.columns)-2)/3))

    # df1 = pd.read_csv(FW[0], encoding='utf-8')
    # columns1 = set(x.split('_')[0] for x in list(df1.columns)[2:])
    #
    # df2 = pd.read_csv(FW[2], encoding='utf-8')
    # columns2 = set(x.split('_')[0] for x in list(df2.columns)[2:])

    # print("df1 포인트 수:", len(columns1))
    # print("df2 포인트 수:", len(columns2))
    #
    # print("포인트 수 차이나는 이유:", columns2 - columns1)

    return BWdata, FWdata

if __name__=="__main__":
    CATEGORY = "Controls"
    PATIENT = "BHY"

    BW, FW = getPatientDataPath(CATEGORY, PATIENT)
    BWdata, FWdata = getPatientData(CATEGORY, PATIENT)
