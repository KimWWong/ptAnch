import os
import pandas as pd
import numpy as np
import re
import json
from msg_utils import Msg


class AnalysisUtils:
    @staticmethod
    def removeFromList(mainList, removalList):
        for remove in removalList:
            if remove in mainList:
                mainList.remove(removalList)
                print(f"{remove} removed")
            # else:
            #     print(f"{remove} was either already removed or does not exist")
            #
        return mainList

    @staticmethod
    def findLowAttn(debriefdf, attnScreenCriteria):
        if attnScreenCriteria > 0:
            debriefdf["attention"] = debriefdf["attention"].astype("int")
            badAttndf = debriefdf.query("(attention < @attnScreenCriteria)")
            lowAttnPNos = badAttndf["id_code"]
        else:
            lowAttnPNos = []

        return list(lowAttnPNos)

    @staticmethod
    def filterParticipantsByPerformance(cumudf, AccFilter, RTFilter):
        groupedcumudf = cumudf.groupby(["pNo"]).mean(numeric_only=True).reset_index()

        if AccFilter:
            badPNoAcc = groupedcumudf.query("(thisAcc < @AccFilter)", inplace=False)[
                "pNo"
            ].unique()
            goodPNoAcc = groupedcumudf.query("(thisAcc >= @AccFilter)", inplace=False)[
                "pNo"
            ].unique()
            # print(badPNoAcc)
            # print(goodPNoAcc)
            print(f"here's the length of badPNoAcc {len(badPNoAcc)}")
            print(f"here's the length of goodPNoAcc {len(goodPNoAcc)}")
            goodcumudf = cumudf.query("pNo in @goodPNoAcc", inplace=False)
        else:
            goodcumudf = cumudf.copy()
            badPNoAcc = []
            goodPNoAcc = groupedcumudf["pNo"].unique()

        if RTFilter:
            meanRT_values = (
                goodcumudf.groupby(["pNo"]).mean(numeric_only=True).reset_index()["rt"]
            )
            stdRT_values = (
                goodcumudf.groupby(["pNo"]).std(numeric_only=True).reset_index()["rt"]
            )

            overallMean = meanRT_values.mean(numeric_only=True)
            overallStd = meanRT_values.std(numeric_only=True)
            upperLimit = float(overallMean + RTFilter * overallStd)
            lowerLimit = float(overallMean - RTFilter * overallStd)

            groupdgoodcumudf = (
                goodcumudf.groupby(["pNo"]).mean(numeric_only=True).reset_index()
            )
            goodPNoRT = groupdgoodcumudf.query(
                "(rt >= @lowerLimit) and (rt <= @upperLimit)", inplace=False
            )["pNo"].unique()
            badPNoRT = groupdgoodcumudf.query(
                "(rt < @lowerLimit) or (rt > @upperLimit)", inplace=False
            )["pNo"].unique()
            # goodPNoRT = goodcumudf.query('(rt < @upperLimit) and (rt > @lowerLimit)', inplace = False)['pNo']
            goodcumudf.query("pNo in @goodPNoRT", inplace=True)

        else:
            badPNoRT = []
            goodPNoRT = groupedcumudf["pNo"].unique()

        allbadPNo = list(badPNoAcc) + list(badPNoRT)
        allgoodPNo = list(
            goodPNoRT
        )  ## because it was sequential in nature, RT should contain all of the good pNos.

        print(f"here's the length of allbadPNo {len(allbadPNo)}")
        print(f"here's the length of allgoodPNo {len(allgoodPNo)}")

        # return goodcumudf, allbadPNo, allgoodPNo
        return allgoodPNo, allbadPNo, badPNoAcc, badPNoRT

    @staticmethod
    def compileDebrief(
        pNoList=list[str],
        headerInit=list[str],
        folderName=str,
        outputDocName=str,
    ):
        """Takes the list of participants and automatically accesses their full datafile,
        extracts debrief questions, and outputs debrief questions to a new csv document.

        Returns list of participants who do not pass the attnScreenCriteria

        pNoList -- list of pNo names
        headerInit -- initial list of debrief questions not including seq
        folderName -- folder to read from and also output to. (currently the same folder)
        outputDocName -- the name of the new DebriefQ csv document
        """

        # headerInit = ['age','gender','2_strategies',"3_experiment",'6_final','attention']
        # headerInit = ["age", "gender", "6_final"]
        # headerInit = ['age', 'gender', '6_final', '7_monitorsetup']
        headerID = ["id_code"]
        header = headerInit + headerID

        extractInfoFromAns = False
        if extractInfoFromAns:
            headerAdd = ["confidence"]
            header = headerInit + headerAdd + headerID

        listofindex = np.arange(1, 2 * len(header) + 1)[::2]

        allAnsList = []
        alldfEntries = []
        additionalInfoList = []

        if extractInfoFromAns == True:
            confidenceList = []

        for pNo in pNoList:
            if os.path.exists(folderName + pNo + "full_data.csv"):
                print(pNo)
                thisdf = pd.read_csv(folderName + pNo + "full_data.csv")
                debriefAns = thisdf[thisdf["trial_category"] == "debrief_original"][
                    "responses"
                ]  # for pre 7.0 jspsych
                # debriefAns = thisdf[thisdf['trial_category']=='debrief']['responses'] #for post 7.0 jspsych
                allAnsList.append(debriefAns.values[0])

                if extractInfoFromAns:
                    additionalInfo = ["confidence"]
                    for addition in additionalInfo:
                        additionalInfoList.append(
                            thisdf[thisdf["trial_category"] == addition].reset_index()[
                                "response"
                            ][0]
                        )
                        # additionalInfoList.append(thisdf[thisdf['trial_category']==addition].reset_index()['responses'][0])

            else:
                pNoList.remove(pNo)
                print(
                    f"{pNo} is missing full_data, make sure to separate them from the others or  your code will break"
                )

        for p in np.arange(len(allAnsList)):
            singleEntry = []
            # print(allAnsList[p])

            pAns = allAnsList[p][
                1:-2
            ]  # removing the brackets from an individual's reponses
            sepAns = re.split(
                '":"|","', pAns
            )  # separating out each of an individuals answers to each question

            for l in np.arange(len(headerInit)):
                singleEntry.append(sepAns[listofindex[l]])

            if extractInfoFromAns:
                for a in np.arange(len(additionalInfoList)):
                    thisAdditional = additionalInfoList[a]
                    singleEntry.append(thisAdditional)

            # print(pNoList)
            singleEntry.append(
                pNoList[p]
            )  # adding on the id_code to the end of the debrief

            alldfEntries.append(singleEntry)

        debriefdf = pd.DataFrame(alldfEntries, columns=header)
        if os.path.exists(folderName + outputDocName + ".csv"):
            print("Warning, this debrief output file exists already. Overlaying.")

        debriefdf.to_csv(r"" + folderName + outputDocName + ".csv", index=False)
        return debriefdf

    @staticmethod
    def addSeqDebrief(
        pNoList=list[str],
        headerSeq=list[str],
        folderName=str,
        inputDocName=str,
        outputDocName=str,
    ):

        # headerSeq = ['gabor_confidence', 'debrief_rememberAny', 'debrief_tableNumGuess', 'debrief_confidence']
        # headerSeq = [
        #     "debrief_rememberAny",
        #     "debrief_tableNumGuess",
        #     "debrief_confidence",
        # ]

        inputDeb = pd.read_csv(folderName + inputDocName + ".csv")
        gaborConfAnsList = []
        debriefRemAnyList = []
        debriefTabNumList = []
        debConfidenceList = []

        for pNo in pNoList:

            if os.path.exists(folderName + pNo + "full_data.csv"):
                thisdf = pd.read_csv(folderName + pNo + "full_data.csv")

                gaborConfAns = thisdf[thisdf["trial_category"] == "confidence"][
                    "responses"
                ]
                debriefSeq1 = thisdf[thisdf["trial_category"] == "debrief_rememberAny"][
                    "responses"
                ]
                debriefSeq2 = thisdf[thisdf["trial_category"] == "debrief_confidence"][
                    "responses"
                ]
                print(debriefSeq1.iloc[0])

                for i in np.arange(len(headerSeq)):
                    # print(str(debriefSeqAns.iloc[count]))
                    if headerSeq[i] == "gabor_confidence":
                        gaborConfAnsList.append(
                            json.loads(gaborConfAns.iloc[0])["gabor_confidence"]
                        )
                    elif headerSeq[i] == "debrief_rememberAny":
                        # debriefRemAnyList.append(json.loads(debriefSeq1.iloc[0])["debrief_rememberAny"])
                        debriefRemAnyList.append(json.loads(debriefSeq1.iloc[0])["Q0"])
                    elif headerSeq[i] == "debrief_tableNumGuess":
                        debriefTabNumList.append(
                            json.loads(debriefSeq2.iloc[0])["tableNumGuess"]
                        )
                    elif headerSeq[i] == "debrief_confidence":
                        debConfidenceList.append(
                            json.loads(debriefSeq2.iloc[0])["confidence"]
                        )
                    else:
                        print("THIS IS BROKEN")

        # listOfLists = [gaborConfAnsList,debriefRemAnyList,debriefTabNumList,debConfidenceList]
        listOfLists = [debriefRemAnyList, debriefTabNumList, debConfidenceList]

        for i in np.arange(len(listOfLists)):
            inputDeb[headerSeq[i]] = listOfLists[i]

        inputDeb.to_csv(r"" + folderName + outputDocName + ".csv", index=False)

        return

    @staticmethod
    def compileAnswers(
        pNoList: list[str],
        folderName: str,
        trialScreenCriteria: float,
        outputDocName: str,
        trialSDfilter: float = 2,
        ptAnchNum: bool = False,
    ):
        """Takes some list of participants and accesses their answer files, allowing for different
        filter options on trials.

        pNoList -- list of pNo names
        folderName -- folder to read from and also output to. (currently the same folder)
        trialScreenCriteria -- will take 'noScreening', '2SDindividual', or '2SDentiredataset'
        trialSDfilter -- only used when trialScreenCriteria != 'noScreening'
        outputDocName -- string. the name of the new cumuAns csv document, no ".csv" necessary

        """

        # print(pNoList)
        for pNo in pNoList:
            print(pNo)
            thisdf = pd.read_csv(folderName + pNo + "answerfiltered_data.csv")
            length = len(thisdf["rt"])
            pNoDup = np.repeat(pNo, length)
            thisdf.insert(0, "pNo", pNoDup)
            # print(thisdf)
            if ptAnchNum == True:
                responseParse = json.loads(thisdf["responses"][0])
                responseDup = np.repeat(responseParse["response"], length)
                thisdf.insert(1, "responseINT", responseDup)
                # print(thisdf)

            if pNo == pNoList[0]:
                cumudf = thisdf.copy()
            else:
                cumudf = pd.concat([cumudf, thisdf])

        if trialScreenCriteria == "noScreening":
            append = ""
            validDF = cumudf.copy()
            groupedcumudf = (
                cumudf.groupby(["pNo"]).mean(numeric_only=True).reset_index()
            )
            allgoodPNo = groupedcumudf["pNo"].unique()

        else:
            if trialScreenCriteria == "2SDindividual":
                append = "individual"
                mean_values = cumudf.groupby(["pNo"]).mean(numeric_only=True)["rt"]
                mean_values = mean_values.reset_index()
                # print(mean_values)
                std_values = cumudf.groupby(["pNo"]).std()["rt"]
                std_values = std_values.reset_index()

                for value in np.arange(len(mean_values["pNo"])):
                    thisPNo = mean_values["pNo"][value]
                    thisRTmean = mean_values["rt"][value]
                    thisRTstd = std_values["rt"][value]
                    thisUpper = thisRTmean + trialSDfilter * thisRTstd
                    thisLower = thisRTmean - trialSDfilter * thisRTstd
                    thisPNoDF = cumudf.query(
                        "(pNo == @thisPNo) and (rt < @thisUpper) and (rt > @thisLower)",
                        inplace=False,
                    )
                    # print(value)
                    # print(thisRTmean, thisRTstd, thisUpper, thisLower)
                    # print(thisPNoDF)
                    if value == 0:
                        validDF = thisPNoDF.copy()
                    elif value > 0:
                        validDF = validDF.append(thisPNoDF)

            elif trialScreenCriteria == "2SDentiredataset":
                append = "entire"
                mean_value = cumudf.mean(numeric_only=True)["rt"]
                std_value = cumudf.std(numeric_only=True)["rt"]
                # print(mean_value,std_value)
                thisUpper = mean_value + trialSDfilter * std_value
                thisLower = mean_value - trialSDfilter * std_value
                validDF = cumudf.query(
                    "(rt < @thisUpper) and (rt > @thisLower)", inplace=False
                )

            else:
                Msg.print_error("SCREENING CRITERIA NOT VALID. ERROR")
        # print(validDF)
        # validDF.query('thisAcc == 1', inplace = True)
        outputValid = outputDocName + append + ".csv"
        validDF.to_csv(r"" + folderName + outputValid, index=False)
        return cumudf
