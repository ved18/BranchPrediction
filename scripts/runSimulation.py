import os
import shutil
import subprocess

def removeBuild():
    build_dir = gem5Dir + "/build/X86/"
    print("Removing build/X86......")
    try:
        shutil.rmtree(build_dir)
        print("Removed build/X86")
    except Exception as e:
        print("Error!! Cannot removed build/X86")
        print(e)

def compileGem5():

    print("#####################################")
    removeBuild()
    try:
        os.chdir(gem5Dir)
        print("Building Gem5.......")
        os.system("scons build/X86/gem5.opt >> temp_exec.txt")
        # subprocess.call(["scons", "/build/X86/gem5.opt"],
        #             stdout=subprocess.STDOUT,
        #             stderr=subprocess.STDOUT,
        #             shell=True)
        print("Successfully built gem5!!!")
        print("#####################################\n")

    except Exception as e:
        print("Error Builing gem5!!!!")
        print(e)
        exit()

def updateBaseSimpleCpu(branchPredictorType):
    
    target = gem5Dir + "/src/cpu/simple/BaseSimpleCPU.py"

    if branchPredictorType == "BiModeBP":
        origin = tempDir + "/BaseSimpleCpu/BaseSimpleCPUBMBP.py"
    elif branchPredictorType == "LocalBP":
        origin = tempDir + "/BaseSimpleCpu/BaseSimpleCPULBP.py"
    elif branchPredictorType == "TournamentBP":
        origin = tempDir + "/BaseSimpleCpu/BaseSimpleCPUTBP.py"
    os.chdir(gem5Dir)
    try:
        shutil.copy(origin, target)
        print("BaseSimpleCPU changed successfully.")
    except Exception as e:
        print("Error!!!! Cannot change BaseSimpleCPU")
        print(e)
        exit()

def updateBTBandLocalPred(BTBSize, LocalSize):
    
    predFile = "BranchPredictor.py"
    replace_text_1 = "    BTBEntries = Param.Unsigned(" + str(BTBSize) + ", \"Number of BTB entries\")\n"
    replace_text_2 = "    localPredictorSize = Param.Unsigned(" + str(LocalSize) + ", \"Size of local predictor\")\n"

    os.chdir(predFileDir)

    with open(predFile, "r") as input:
        with open("temp.py", "w") as output:
            # iterate all lines from file
            for line in input:
                if line.strip("\n").__contains__("BTBEntries = Param.Unsigned("):
                    output.write(replace_text_1)
                elif line.strip("\n").__contains__("localPredictorSize = Param.Unsigned(") and LocalSize != None:
                    output.write(replace_text_2)
                else:
                    output.write(line)
        os.remove(predFile)
        os.rename("temp.py", predFile)

def updateGlobalPred(globalSize):
    predFile = "BranchPredictor.py"
    replace_text = "    globalPredictorSize = Param.Unsigned(" + str(globalSize) + ", \"Size of global predictor\")\n"

    os.chdir(predFileDir)

    with open(predFile, "r") as input:
        with open("temp.py", "w") as output:
            # iterate all lines from file
            for line in input:
                if line.strip("\n").__contains__("globalPredictorSize = Param.Unsigned("):
                    output.write(replace_text)
                else:
                    output.write(line)
        os.remove(predFile)
        os.rename("temp.py", predFile)

def updateChoicePred(choiceSize):
    predFile = "BranchPredictor.py"
    replace_text = "    choicePredictorSize = Param.Unsigned(" + str(choiceSize) + ", \"Size of choice predictor\")\n"

    os.chdir(predFileDir)

    with open(predFile, "r") as input:
        with open("temp.py", "w") as output:
            # iterate all lines from file
            for line in input:
                if line.strip("\n").__contains__("choicePredictorSize = Param.Unsigned("):
                    output.write(replace_text)
                else:
                    output.write(line)
        os.remove(predFile)
        os.rename("temp.py", predFile)

def setUpSimulation(simulation):
    updateBaseSimpleCpu(simulation[0])
    updateBTBandLocalPred(simulation[1], simulation[2])
    if simulation[3] != None:
        updateGlobalPred(simulation[3])
    if simulation[4] != None:
        updateChoicePred(simulation[4])
    compileGem5()

def runSimulation(benchmarkDir, output, pred):
    os.chdir(benchmarkDir)
    print("#####################################")
    print("Running simulation on " + benchmarkDir)
    
    subprocess.call(["bash", "runGem5.sh", pred + "_sim" + str(output)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

    print("Simulation Done")
    print("#####################################\n")

def main():
    global baseDir
    global gem5Dir
    global tempDir 
    global predFileDir
    global benchmarkDir_401
    global benchmarkDir_429
    
    baseDir = "/home/013/v/va/vak190002/CompArch/py3"
    gem5Dir = baseDir + "/gem5"
    tempDir = baseDir + "/scripts/temp"
    predFileDir = gem5Dir + "/src/cpu/pred/"
    benchmarkDir_401 = baseDir + "/Project1_SPEC/401.bzip2"
    benchmarkDir_429 = baseDir + "/Project1_SPEC/429.mcf"
    
    simulations = [ #[Pred Name, BTB, Local, Global, Choice],
                    ["LocalBP", 2048, 1024, None, None],
                    ["TournamentBP",2048, 2048, 2048, 2048],
                    ["BiModeBP", 2048, 2048, 2048, None],
                ]
    for index, simulation in enumerate(simulations):
        setUpSimulation(simulation)
        runSimulation(benchmarkDir_401, index, simulation[0])
        runSimulation(benchmarkDir_429, index, simulation[0])
    
    print("Done Simulations")

if __name__ == "__main__":
    main()