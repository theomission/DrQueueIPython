#
# THIS IS A PYTHON SCRIPT FILE
# 
# Default configuration for Maya script generator
# 
# Python variables
# SCENE, RENDERDIR, PROJECTDIR, RF_OWNER, FFORMAT, RESX, RESY, CAMERA, DRQUEUE_IMAGE,
# RENDERER, DRQUEUE_POST, DRQUEUE_PRE
# 
# shell variables
# DRQUEUE_BIN, DRQUEUE_ETC, DRQUEUE_OS, DRQUEUE_FRAME, DRQUEUE_ENDFRAME, DRQUEUE_BLOCKSIZE
#

#
# For platform dependend environment setting a form like this
# can be used :
#
# if DRQUEUE_OS == "LINUX":
#    # Environment for Linux
# elsif DRQUEUE_OS == "IRIX":
#    # Environment for Irix
# else
#    # Some error messages
#

import os,signal,subprocess,sys

os.umask(0)

# fetch DrQueue environment
DRQUEUE_ETC = os.getenv("DRQUEUE_ETC")
DRQUEUE_BIN = os.getenv("DRQUEUE_BIN")
DRQUEUE_OS = os.getenv("DRQUEUE_OS")
DRQUEUE_FRAME = os.getenv("DRQUEUE_FRAME")
DRQUEUE_ENDFRAME = os.getenv("DRQUEUE_ENDFRAME")
DRQUEUE_BLOCKSIZE = os.getenv("DRQUEUE_BLOCKSIZE")


if DRQUEUE_OS == "WINDOWS":
	# convert to windows path with drive letter
	SCENE = subprocess.Popen(["cygpath.exe", "-w "+SCENE], stdout=subprocess.PIPE).communicate()[0]
	RENDERDIR = subprocess.Popen(["cygpath.exe", "-w "+RENDERDIR], stdout=subprocess.PIPE).communicate()[0]
	PROJECTDIR = subprocess.Popen(["cygpath.exe", "-w "+PROJECTDIR], stdout=subprocess.PIPE).communicate()[0]
	

BLOCK = DRQUEUE_FRAME + DRQUEUE_BLOCKSIZE - 1

if BLOCK > DRQUEUE_ENDFRAME:
	BLOCK = DRQUEUE_ENDFRAME


if DRQUEUE_IMAGE != "":
	image_args="-im "+DRQUEUE_IMAGE
else:
	image_args=""

if CAMERA != "":
	camera_args="-cam "+CAMERA
else:
	camera_args=""

if (RESX != -1) && (RESY != -1):
	res_args="-x "+RESX+" -y "+RESY
else:
	res_args=""

if FFORMAT != "":
	format_args="-of "+FFORMAT
else:
	format_args=""

if RENDERER == "mr":
	## number of processors/cores to use
	#proc_args="-rt 2"

	## use Maya's automatic detection
	proc_args="-art"
else:
	## number of processors/cores to use
	#proc_args="-n 2"

	## use Maya's automatic detection
	proc_args="-n 0"

if DRQUEUE_PRE != "":
	pre_args="-preRender \""+DRQUEUE_PRE+"\""
else:
	pre_args=""
	
if DRQUEUE_POST != "":
	post_args="-postRender \""+DRQUEUE_POST+"\""
else:
	post_args=""


ENGINE_PATH="Render"

command = ENGINE_PATH+" "+pre_args+" "+post_args+" "+proc_args+" -s "+DRQUEUE_FRAME+" -e "+BLOCK+" "+res_args+" "+format_args+" -rd "+RENDERDIR+" -proj "+PROJECTDIR+" -r "+RENDERER+" "+image_args+" "+camera_args+" "+SCENE


print command
sys.stdout.flush()

p = subprocess.Popen(command, shell=True)
sts = os.waitpid(p.pid, 0)

# This should requeue the frame if failed
if sts[1] != 0:
	print "Requeueing frame..."
	os.kill(os.getppid(), signal.SIGINT)
	exit(1)
else:
	#if DRQUEUE_OS != "WINDOWS" then:
	# The frame was rendered properly
	# We don't know the output image name. If we knew we could set this correctly
	# chown_block RF_OWNER RD/IMAGE DRQUEUE_FRAME BLOCK 

	# change userid and groupid
	#chown 1002:1004 $SCENE:h/*
	print "Finished."
#
# Notice that the exit code of the last command is received by DrQueue
#
