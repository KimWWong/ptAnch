import os
import pandas as pd
import numpy as np
from typing import List
from file_utils import PathUtils, FileUtils
from msg_utils import Msg
from analysis_utils import AnalysisUtils as au

# from badPNos import robPNos


def main():

    folderName = PathUtils.get_curr_path() + "/06122024_asianfem_revist_instr/"

    debriefType = "none"  ## seq or none, if there is extended debrief or not
    trialScreenCriteria = "2SDentiredataset"  ## 2SDentiredataset, 2SDindividual, boths
    attnScreenCriteria = False  ## some integer 1-100 self-report attention value
    accScreenCriteria = False  ## some float 0.00-1.00 acc percentage minimum
    rtSDScreenCriteria = False  ## usually 2 or 2.5, the SDs away to rem pNos
    trialSDfilter = 2.0  ## usually 2 or 2.5, the SDs away to rem trials in pNo
    ptAnchNum = True  ## make this true if you're doing anything where there needed to be anchoring to a number

    headerInit = ["age", "gender", "6_final"]
    headerSeq = ["debrief_rememberAny", "debrief_tableNumGuess", "debrief_confidence"]

    pNoList = PathUtils.extract_all_files_with(
        prefix=folderName, suffix="answerfiltered_data.csv"
    )
    print(f"Total initial list of participants: {len(pNoList)}")

    # ## exclude a list of PNos that was imported at start. No need to do so in current batch.
    # pNoList = au.removeFromList(pNoList, robPNos)

    ## creating first datafiles with raw data
    # print(raw_anlys["debrief"].items())
    raw_anlys = createAnalysisDic(
        pNoList, headerInit, headerSeq, ptAnchNum, folderName, "raw"
    )
    initialDebrief = au.compileDebrief(**raw_anlys["debrief"])
    au.compileAnswers(**raw_anlys["answer"])
    if debriefType == "seq":
        au.addSeqDebrief(**raw_anlys["debrief_seq"])

    ## dealing with low attention participants
    lowAttnPNos = au.findLowAttn(initialDebrief, attnScreenCriteria)
    print(f"Length of low attention pnos is {len(lowAttnPNos)}")
    if len(lowAttnPNos) > 1:
        lowAttn_anlys = createAnalysisDic(
            lowAttnPNos, headerInit, headerSeq, ptAnchNum, folderName, "lowAttn"
        )
        au.compileDebrief(**lowAttn_anlys["debrief"])
        au.compileAnswers(**lowAttn_anlys["answer"])
        if debriefType == "seq":
            au.addSeqDebrief(**lowAttn_anlys["debrief_seq"])

    ## dealing with the remaining high attention praticipants
    pNoList_lowAttnRem = au.removeFromList(pNoList, lowAttnPNos)
    lowAttnRem_anlys = createAnalysisDic(
        pNoList_lowAttnRem, headerInit, headerSeq, ptAnchNum, folderName, "lowAttnRem"
    )
    au.compileDebrief(**lowAttnRem_anlys["debrief"])
    cumudflowAttnRem = au.compileAnswers(**lowAttnRem_anlys["answer"])
    if debriefType == "seq":
        au.addSeqDebrief(**lowAttnRem_anlys["debrief_seq"])

    ## now filter participants based off of the ir trial performance
    accRTGoodPNo, accRTBadPNo, accBadPNo, RTBadPNo = au.filterParticipantsByPerformance(
        cumudf=cumudflowAttnRem,
        AccFilter=accScreenCriteria,
        RTFilter=rtSDScreenCriteria,
    )

    ## bad accTrial performance participants
    if accScreenCriteria:
        accBadPNo_anlys = createAnalysisDic(
            accBadPNo, headerInit, headerSeq, ptAnchNum, folderName, "badOverallAcc"
        )
        au.compileDebrief(**accBadPNo_anlys["debrief"])
        au.compileAnswers(**accBadPNo_anlys["answer"])
        if debriefType == "seq":
            au.addSeqDebrief(**accBadPNo_anlys["debrief_seq"])

    ## bad rt Trial performance participants
    if rtSDScreenCriteria:
        RTBadPNo_anlys = createAnalysisDic(
            RTBadPNo, headerInit, headerSeq, ptAnchNum, folderName, "badOverallRT"
        )
        au.compileDebrief(**RTBadPNo_anlys["debrief"])
        au.compileAnswers(**RTBadPNo_anlys["answer"])
        if debriefType == "seq":
            au.addSeqDebrief(**RTBadPNo_anlys["debrief_seq"])

    ## Participant-level filtering done, onto the trial level filters
    goodData_anlys = createAnalysisDic(
        accRTGoodPNo,
        headerInit,
        headerSeq,
        ptAnchNum,
        folderName,
        "GOODDATA",
        trialSDfilter,
        trialScreenCriteria,
    )
    au.compileDebrief(**goodData_anlys["debrief"])
    au.compileAnswers(**goodData_anlys["answer"])
    if debriefType == "seq":
        au.addSeqDebrief(**goodData_anlys["debrief_seq"])
    if (trialScreenCriteria == "2SDentiredataset") or (trialScreenCriteria == "both"):
        au.compileAnswers(**goodData_anlys["answer-2SDentiredataset"])
    if (trialScreenCriteria == "2SDindividual") or (trialScreenCriteria == "both"):
        au.compileAnswers(**goodData_anlys["answer-2SDindividual"])
    #
    # au.compileDebrief(
    #     pNoList=accRTGoodPNo,
    #     headerInit=headerInit,
    #     folderName=folderName,
    #     outputDocName="DebriefQs-GOODDATA",
    # )
    #
    # au.compileAnswers(
    #     pNoList=accRTGoodPNo,
    #     folderName=folderName,
    #     trialScreenCriteria="noScreening",
    #     outputDocName="cumuAns-GOODDATA-noTrialFilter",
    #     trialSDfilter=0,
    #     ptAnch=ptAnch,
    # )
    # au.compileAnswers(
    #     pNoList=accRTGoodPNo,
    #     folderName=folderName,
    #     trialScreenCriteria=trialScreenCriteria,
    #     outputDocName="cumuAns-GOODDATA-filtered",
    #     trialSDfilter=trialSDfilter,
    #     ptAnch=ptAnch,
    # )
    # if debriefType == "seq":
    #     au.addSeqDebrief(
    #         pNoList=accRTGoodPNo,
    #         headerSeq=headerSeq,
    #         folderName=folderName,
    #         inputDocName="DebriefQs-GOODDATA",
    #         outputDocName="DebriefQs-FULLSEQ-GOODDATA",
    #     )

    # for _, values in raw_anlys["debrief"].items():
    #     au.compileDebrief(*values)

    # analysis_to_run = {"noScreening": {"pNoList": accRTGoodPNo}, "screening": {}}
    # for _, values in analysis_to_run.items():
    #     compileAnswers(**values)


# main ends here
def createAnalysisDic(
    pNoList,
    headerInit,
    headerSeq,
    ptAnchNum,
    folderName,
    dictionaryType,
    trialSDfilter=0,
    trialScreenCriteria="none",
):
    analysis_dic = {
        "debrief": {
            "pNoList": pNoList,
            "headerInit": headerInit,
            "folderName": folderName,
            "outputDocName": "DebriefQs-" + dictionaryType,
        },
        "debrief_seq": {
            "pNoList": pNoList,
            "headerSeq": headerSeq,
            "folderName": folderName,
            "inputDocName": "DebriefQs-" + dictionaryType,
            "outDocName": "DebriefQs-FULLSEQ-" + dictionaryType,
        },
        "answer": {
            "pNoList": pNoList,
            "folderName": folderName,
            "trialScreenCriteria": "noScreening",
            "outputDocName": "cumuAns-" + dictionaryType + "-noTrialFilter",
            "trialSDfilter": 0,
            "ptAnchNum": ptAnchNum,
        },
    }
    if dictionaryType == "GOODDATA":
        if (trialScreenCriteria == "2SDentiredataset") or (
            trialScreenCriteria == "both"
        ):
            analysis_dic["answer-2SDentiredataset"] = {
                "pNoList": pNoList,
                "folderName": folderName,
                "trialScreenCriteria": "2SDentiredataset",
                "outputDocName": "cumuAns-GOODDATA-filtered",
                "trialSDfilter": trialSDfilter,
                "ptAnchNum": ptAnchNum,
            }
        if (trialScreenCriteria == "2SDindividual") or (trialScreenCriteria == "both"):
            analysis_dic["answer-2SDindividual"] = {
                "pNoList": pNoList,
                "folderName": folderName,
                "trialScreenCriteria": "2SDindividual",
                "outputDocName": "cumuAns-GOODDATA-filtered",
                "trialSDfilter": trialSDfilter,
                "ptAnchNum": ptAnchNum,
            }

    return analysis_dic


if __name__ == "__main__":
    main()
