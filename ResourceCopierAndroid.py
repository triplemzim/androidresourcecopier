import os
import shutil
from glob import glob


def openFileAtGivenPathForWriting(path):
	if not os.path.exists(os.path.dirname(path)):
		try:
			os.makedirs(os.path.dirname(path))
			return open(path,"w")
		except OSError as exc:  # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def findFile(targetFile, tempPath, savePath):
	for dirname, dirnames, filenames in os.walk(tempPath):
		# print(dirname + ' ' )
		if isValidDir(dirname) == False:
			continue

		# print(dirname)
		for filename in filenames:
			tempName = filename.split('.')[0]
			if(tempName == targetFile):
				print("Found file: " + targetFile + ' ' + dirname)
				try:
					if "hdpi" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable-hdpi\\')
					elif "mdpi" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable-mdpi\\')
					elif "xhdpi" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable-xhdpi\\')
					elif "xxhdpi" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable-xxhdpi\\')
					elif "xxxhdpi" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable-xxxhdpi\\')
					elif "drawable" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\drawable\\')
						if "xml" in filename:
							runMain(dirname + '\\' + filename)
					elif "layout" in dirname:
						shutil.copy2(dirname + '\\' + filename, savePath+ '\\layout\\')
						runMain(dirname + '\\' + filename)
					else:
						shutil.copy2(dirname + '\\' + filename, savePath)
						# runMain(dirname + '\\' + filename)
					# shutil.copy2(dirname + '\\' + filename, savePath)
				except:
					print("May be duplicate files")

		# for subdir in dirnames:
		# 	findFile(targetFile, dirname + "\\" + subdir, savePath)
		# 	print("recursion: " + dirname + ' ' + subdir)


def findXMLFileInJavaFile(sourceLines, savePath):
	xmlFile = ""
	for line in sourceLines:
		# if line.strip().startswith("setContentView"):
		# 	xmlFile = line.strip().replace("setContentView(R.layout.", "").replace(");", "")
		if "R.layout." in line:
			st = line[line.index("R.layout.") + len("R.layout."): len(line)]
			st = st.replace(' ', '')
			st = st.strip()
			st = st.replace(',', '$')
			st = st.replace(')', '$')
			st = st.split('$')[0]
			print("Found xml in java file: " + st + ".xml")
			findFile(st, currentPath ,savePath)



def getFileResourceNameByTagName(sourceLines, tagName, savePath):
	resource = set()
	for line in sourceLines:
		if line.find("@" + tagName) >= 0:
			resource.add(line.strip().split(
				"/")[1].split("\"")[0].replace("\"", "").replace(">", ""))
	for fileName in resource:
		print("finding -> ", fileName)
		findFile(fileName, currentPath, savePath)

def getResourceNameByTagName(data, tagName, savePath):
	resource = set()
	for line in data:
		if "@"+tagName in line:
			resource.add(line.strip().split(
				"/")[1].split("\"")[0].replace("\"", "").replace(">", ""))
		if "R." + tagName +"." in line:
			st = line[line.index("R." + tagName +".") + len("R." + tagName +"."): len(line)]
			st = st.replace(' ', '')
			st = st.strip()
			st = st.replace(',', '$')
			st = st.replace(')', '$')
			st = st.split('$')[0]
			resource.add(st)
			# print("Found xml in java file: " + st + ".xml")
	return resource

def isValidDir(dirname):
	if "build" in dirname or "gradle" in dirname or "." in dirname or "libs" in dirname or "ziftaRes" in dirname: 
		return False
	return True 


def openFileByNameExtension(name, extension, tempPath, savePath):
	# print("opening " + name + extension + tempPath)
	targetFile = name + "." + extension

	for dirname, dirnames, filenames in os.walk(tempPath):
		if isValidDir(dirname) == False:
			continue

		for filename in filenames:
			if dirname.find(savePath) >= 0:
				break
			if(filename == targetFile):
				try:
					return open(dirname + "\\" + targetFile, "r")
				except:
					print("File does not exists most probably")

		# for subdir in dirnames:
		# 	openFileByNameExtension(name, extension, dirname + "\\" + subdir, savePath)


def getResourceData(sourceFile, searckKeys):
	resourceData = set()
	lines = sourceFile.readlines()
	for line in lines:
		for searckKey in searckKeys:
			if "\"" + searckKey + "\"" in line:
				resourceData.add(line.strip())
	sourceFile.seek(0)
	return resourceData


def printToFile(fileName, resData, savePath):
	fileOutput = open(savePath + "\\" + fileName, "w+")
	for st in resData:
		fileOutput.write(st)
		fileOutput.write('\n')
	fileOutput.close()

def getOtherRes(data,savePath):
	color = getResourceNameByTagName(data, "color", savePath)
	print("Colors: " + str(color))

	dimen = getResourceNameByTagName(data, "dimen", savePath)
	print("Dimens: " + str(dimen))

	string = getResourceNameByTagName(data, "string", savePath)
	print("Strings: " + str(string))

	colorFile = openFileByNameExtension("colors", "xml", currentPath, savePath)
	# print(getResourceData(colorFile, color))
	# colorFile.close()

	dimenFile = openFileByNameExtension("dimens", "xml", currentPath, savePath)
	# print(getResourceData(dimenFile, dimen))
	# dimenFile.close()

	stringFile = openFileByNameExtension("strings", "xml", currentPath, savePath)
	# stringData = getResourceData(stringFile, string)
	# stringFile.close()

	print("Writing files...")
	printToFile("dimens.xml", getResourceData(dimenFile, dimen), savePath)
	printToFile("colors.xml", getResourceData(colorFile, color), savePath)
	printToFile("strings.xml", getResourceData(stringFile, string), savePath)

	# dimenOutput = open(savePath + "\\dimens.xml", "w+")
	# tempList = getResourceData(dimenFile, dimen)
	# for st in tempList:
	# 	dimenOutput.write(st)
	# 	dimenOutput.write('\n')
	# dimenOutput.close()
	# dimenOutput.close()

	# outputFilePath = os.getcwd()+"//res//strings.xml"
	# outputFile = openFileAtGivenPathForWriting(outputFilePath)
	# for data in stringData:
	#     outputFile.write(data+"\n")
	# outputFile.close()	




def runMain(SRC):

	srcfile = open(SRC, 'r')

	srcFileName = SRC.split('\\')[len(SRC.split('\\')) -1]

	print("Source file: " + srcFileName)

	savePath = currentPath + '\\ziftaRes\\' + srcFileName 
	print("Saving directory: " + savePath)

	print("Savepath: " + savePath)

	if os.path.exists(savePath) == False:
		os.makedirs(savePath)

	if os.path.exists(savePath + "\\drawable-hdpi") == False:
		os.makedirs(savePath + "\\drawable-hdpi")
	if os.path.exists(savePath + "\\drawable-xhdpi") == False:
		os.makedirs(savePath + "\\drawable-xhdpi")
	if os.path.exists(savePath + "\\drawable-xxhdpi") == False:
		os.makedirs(savePath + "\\drawable-xxhdpi")
	if os.path.exists(savePath + "\\drawable-xxxhdpi") == False:
		os.makedirs(savePath + "\\drawable-xxxhdpi")
	if os.path.exists(savePath + "\\drawable-mdpi") == False:
		os.makedirs(savePath + "\\drawable-mdpi")
	if os.path.exists(savePath + "\\drawable") == False:
		os.makedirs(savePath + "\\drawable")
	if os.path.exists(savePath + "\\layout") == False:
		os.makedirs(savePath + "\\layout")

	data = srcfile.readlines()
	print("Finding drawables...in " + srcFileName)
	getFileResourceNameByTagName(data, "drawable", savePath)

	print("Finding other resources...in " + srcFileName)
	getOtherRes(data, savePath)

	print("Finding layout...in " + srcFileName)
	getFileResourceNameByTagName(data, "layout", savePath)

	if srcFileName.endswith("java"):
		findXMLFileInJavaFile(data, savePath)






# a = "E:\\REVE\\AndroidProjects\\New folder\\gradlew\\bla.xml"
a = input("Please enter the file path: ")
global currentPath
currentPath = os.getcwd()

if os.path.exists(a) == True:
	runMain(a)
