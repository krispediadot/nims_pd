import pandas as pd
import os
import argparse

DEBUG = False

DATASETPATH = './dataset/'
DATA_CONTROL = os.path.join(DATASETPATH , 'Controls')
DATA_PD = os.path.join(DATASETPATH, 'PD')

if os.path.exists(DATASETPATH) == False:
    os.mkdir(DATASETPATH)

def prepData(target_path, target_file, ptype):
    if DEBUG: print("[ * ] prepData:", target_file)
    # 1. 2줄 제외하고 읽기
    dff = pd.read_csv(target_path, skiprows=2, encoding='utf-8')

    # 2. 전체 none인 컬럼 제외
    while dff[list(dff.columns)[-1]].isna().all():
        dff.drop(list(dff.columns)[-1], axis=1, inplace=True)

    # 3. 단위가 mm인 데이터만 추출
    target = [0, 1]
    target += list(filter(lambda x: list(dff.iloc[1] == 'mm')[x], range(len(list(dff.iloc[1])))))
    dff = dff.iloc[:, target]
    dff.drop(dff.index[1], inplace=True)

    # 4. 컬럼 이름 변경하기

    pList = dff.columns
    colList = dff.iloc[0]

    NAME = None

    pNames = []
    for p in pList:
        if not p.startswith('Unnamed'):
            if NAME == None: NAME = p.split(':')[0]
            pNames.append(p.split(':')[1])

    columns = []
    columns.append(colList[0])
    columns.append(colList[1])
    for idx, col in enumerate(colList[2:]):
        i = int(idx / 3)
        eachColName = pNames[i] + '_' + col
        columns.append(eachColName)

    assert len(columns) == len(list(dff.columns))

    dff.drop(dff.index[0], inplace=True)
    dff.reset_index(drop=True, inplace=True)

    dff.columns = columns

    if os.path.exists(DATASETPATH + ptype) == False:
        os.mkdir(DATASETPATH + ptype)

    dff.to_csv(os.path.join(os.path.join(DATASETPATH, ptype), 'PREP_' + target_file), encoding='utf-8', index=False)

def runPrepData(rawdatapath):
    if DEBUG: print("[ * ] runPrepData")

    for f in os.listdir(rawdatapath):
        if f.endswith('.csv'):
            prepData(os.path.join(rawdatapath, f), f, rawdatapath.split('/')[-1])

def generatePatientsTable():
    if DEBUG: print("[ * ] generatePatientsTable")

    patient = []
    category = []
    cntFW = []
    cntBW = []
    pathFW = []
    pathBW = []


    # Controls
    files = os.listdir(DATA_CONTROL)
    files.sort()

    prevName = files[0].split('_')[1]
    idx = 0

    while idx < len(files):
        if files[idx].endswith('.csv'):
            files[idx].replace('.csv', '')
            _, pName, bwfw = files[idx].split('_')
            bw = 0
            fw = 0
            pFW = []
            pBW = []
            while pName == prevName:
                if bwfw.startswith('BW'):
                    bw += 1
                    pBW.append(os.path.join(DATA_CONTROL, files[idx]))
                else:
                    fw += 1
                    pFW.append(os.path.join(DATA_CONTROL, files[idx]))
                #             print(f.split('_')[1], f.split('_')[2].split('.csv')[0])
                idx += 1
                if idx == len(files): break
                _, pName, bwfw = files[idx].split('_')

            patient.append(prevName)
            category.append('Controls')
            cntFW.append(fw)
            cntBW.append(bw)
            pathFW.append(pFW)
            pathBW.append(pBW)

            prevName = pName

    # PD
    files = os.listdir(DATA_PD)
    files.sort()

    prevName = files[0].split('_')[1]
    idx = 0

    while idx < len(files):
        if files[idx].endswith('.csv'):
            files[idx].replace('.csv', '')
            if len(files[idx].split('_')) == 3:
                _, pName, bwfw = files[idx].split('_')
            else:
                _, pName, bwfw, _ = files[idx].split('_')
            bw = 0
            fw = 0
            pFW = []
            pBW = []
            while pName == prevName:
                if bwfw.startswith('BW'):
                    bw += 1
                    pBW.append(os.path.join(DATA_CONTROL, files[idx]))
                else:
                    fw += 1
                    pFW.append(os.path.join(DATA_CONTROL, files[idx]))
                #             print(f.split('_')[1], f.split('_')[2].split('.csv')[0])
                idx += 1
                if idx == len(files): break
                #             print(files[idx])
                if len(files[idx].split('_')) == 3:
                    _, pName, bwfw = files[idx].split('_')
                else:
                    _, pName, bwfw, _ = files[idx].split('_')

            patient.append(prevName)
            category.append('PD')
            cntFW.append(fw)
            cntBW.append(bw)

            prevName = pName

            df = pd.DataFrame()
            df['Patient'] = patient
            df['Category'] = category
            df['cntFW'] = cntFW
            df['cntBW'] = cntBW
            # df['pathFW'] = pathFW
            # df['pathBW'] = pathBW

            df.to_csv(os.path.join(DATASETPATH, 'patients.csv'), encoding='utf-8', index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="debug mode")
    args = parser.parse_args()
    if args.debug == "true":
        DEBUG = True

    runPrepData('./FW&BW_Rawdata/PD')
    runPrepData('./FW&BW_Rawdata/Controls')
    runPrepData('./FW&BW_Rawdata/Controls(추가)')

    generatePatientsTable()

