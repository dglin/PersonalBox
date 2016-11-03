import os, json

def formTree(path):
	dictionary = {}
	for subdir, dirs, files in os.walk(path):
	    for file in files:
	        dictionary[os.path.join(subdir, file)] = os.path.getmtime(os.path.join(subdir, file))
	return dictionary

def initialize():
	print "Hellow David, you were initialized"
	with open('store.txt') as f:
	    lines = f.readlines()
	serverAddress = lines[0].strip('\n')
	serverPath = lines[1].strip('\n')
	localPath = lines[2].strip('\n')
	username = lines[3].strip('\n')
	password = lines[4].strip('\n')
	oldTree = json.loads(lines[5].strip('\n'))
	newTree = formTree(localPath)
	sftp_list = []
	print newTree
	for key in newTree:
		if oldTree.get(key) is None or newTree[key] > oldTree[key]:
			sftp_list.append(key)
	return serverAddress, serverPath, localPath, username, password, sftp_list