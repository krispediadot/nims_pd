import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import seaborn as sns

import os
import pandas as pd
import numpy as np

def getGraphArea(patient, idx, data, shift, TARGET_CATE, SAVEPATH, isSave=True):
    LH = data.iloc[0:-shift]["LHEE_Z"].values
    RH = data.iloc[shift:]["RHEE_Z"].values
    LH_DIFF = data.iloc[0:-shift]["LHEE_Z_DIFF"].values
    RH_DIFF = data.iloc[shift:]["RHEE_Z_DIFF"].values
    
    result = np.array([np.sum(LH), np.sum(RH), np.sum(LH_DIFF), np.sum(RH_DIFF)])
    
    if isSave: np.save(os.path.join(os.path.join(SAVEPATH, TARGET_CATE), f"{patient}-FW{idx+1}-AREA.npy"), result)
    
    # LH, RH, LH_DIFF, RH_DIFF
    return result

def plotPatientLRZDiff(patient, FWdata, TARGET_CATE, SAVEPATH, isGetArea=True, isSave=True):
    """ patient's left heel & right heel Z-axis balance visualization """
    for idx, data in enumerate(FWdata):
        
        # PHASE 1 시작하는 지점 찾기 -- 이전 인덱스와 5 이상 차이나는 경우 선택
        start = [np.where(data["PHASE"] == 1)[0][0]] + [ x for idx, x in enumerate(np.where(data["PHASE"] == 1)[0][1:]) if x -np.where(data["PHASE"] == 1)[0][idx] > 5 ]

        fig, axes = plt.subplots(2, 2, figsize=(20,10), tight_layout=True)
        fig.suptitle(f"{patient} - FW{idx+1}", fontsize=15)

        sns.lineplot(ax=axes[0][0], data=data[["LHEE_Z", "RHEE_Z"]])
        axes[0][0].set_title("Left-Right HEE Z-aixs")

        sns.lineplot(ax=axes[0][1], data=data[["LHEE_Z_DIFF", "RHEE_Z_DIFF"]])
        axes[0][1].set_title("Left-Right HEE Diff")

        # phase 1 중 LHEE_Z_DIFF > RHEE_Z_DIFF 인 경우를 shift 기준으로 사용
        shift = start[1]
        if data.iloc[shift]["LHEE_Z_DIFF"] < data.iloc[shift]["RHEE_Z_DIFF"]: shift = start[2]
        
        # 면적 계산이 필요하다면
        if isGetArea: getGraphArea(patient, idx, data, shift, TARGET_CATE, SAVEPATH)

        sns.lineplot(ax=axes[1][0], data=pd.DataFrame({
                    "LHEE_Z" : data.iloc[0:-shift]["LHEE_Z"].values,
                    "RHEE_Z" : data.iloc[shift:]["RHEE_Z"].values})
                    )
        axes[1][0].set_title("Left-Right HEE Z-axis sync")

        sns.lineplot(ax=axes[1][1], data=pd.DataFrame({
                    "LHEE_Z_DIFF" : data.iloc[0:-shift]["LHEE_Z_DIFF"].values,
                    "RHEE_Z_DIFF" : data.iloc[shift:]["RHEE_Z_DIFF"].values})
                    )
        axes[1][1].set_title("Left-Right HEE Diff sync")
        
        fig.savefig(os.path.join(os.path.join(SAVEPATH, TARGET_CATE), f"{patient}-FW{idx+1}.jpg"))
    plt.show()
    
    
# 여러 환자 데이터에 적용
def plotCategoryLRZDiff(category:str, CONTROL:pd.DataFrame, PD:pd.DataFrame, DATAPATH, SAVEPATH):
    targetList = PD
    if category == "Controls": targetList = CONTROL
    
    for patient, cntFW in zip(targetList["Patient"], targetList["cntFW"]):

        print("Category:", category)
        print("Patient :", patient)

        FWdata = []

        for idx in range(1, cntFW+1):
            if os.path.exists(os.path.join(DATAPATH, f"LHEE_{patient}_FW{idx}.csv")):
                FWdata.append(pd.read_csv(os.path.join(DATAPATH, f"LHEE_{patient}_FW{idx}.csv")))

        plotPatientLRZDiff(patient, FWdata, category, SAVEPATH)
    
    
if __name__=="__main__":
    STDPATH = "LHEE 기준 STD 완료한 데이터셋 위치" # 변경필요
    CONTROL_PATH = os.path.join(STDPATH, "Controls")
    PD_PATH = os.path.join(STDPATH, "PD")
    SAVEPATH =  "VIZ 결과 저장할 위치" # 변경필요
    
    SAVE_CONTROL = os.path.join(SAVEPATH, "Controls")
    SAVE_PD = os.path.join(SAVEPATH, "PD")
    
    if os.path.exists(FIGPATH) == False: os.mkdir(FIGPATH)
    if os.path.exists(FIG_CONTROL) == False: os.mkdir(FIG_CONTROL)
    if os.path.exists(FIG_PD) == False: os.mkdir(FIG_PD)
    
    patient = "환자 이니셜" # 변경필요
    
    FWdata = [
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름1")), #변경필요
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름2")), #변경필요
        pd.read_csv(os.path.join(CONTROL_PATH, f"파일이름3"))  #변경필요
    ]
    
    plotPatientLRZDiff(patient, FWdata)
    
    TARGET_CATE="Controls"
    plotCategoryLRZDiff(TARGET_CATE, CONTROL, PD, CONTROL_PATH, FIGPATH)
