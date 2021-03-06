# This script attempts to download the libRoadrunner (binary) libraries and
# headers for your particular operating system. It installs them in 
# the appropriate /addons directory which the Makefile can find.
#
# Author: Randy Heiland

import platform
import urllib.request
import os
import sys
import tarfile
import zipfile

if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "addons", "libRoadrunner", "roadrunner")):
    print('\nlibroadrunner already installed.\n')

else:
    print('\nThis model requires the libRoadrunner libraries which will now be downloaded.')
    os_type = platform.system()
    print('(for your ',os_type, ' operating system)')

    # Assume Windows
    rr_file = ""
    url = ""

    if os_type.lower() == 'darwin':
        if "ARM64" in platform.uname().version:
            print('... for the arm64 processor.')
        # if False:
            # pass
            url = "https://github.com/PhysiCell-Tools/intracellular_libs/raw/main/ode/libs/macos12_arm64/libroadrunner_c_api.dylib"
        else:
            rr_file = "roadrunner-osx-10.9-cp36m.tar.gz"
            url = "https://sourceforge.net/projects/libroadrunner/files/libroadrunner-1.4.18/" + rr_file + "/download"
            url = "https://raw.github.com/PhysiCell-Tools/intracellular_libs/blob/main/ode/libs/macos/roadrunner-osx-10.9-cp36m.tar.gz"

            rr_file = "roadrunner-osx-10.9-cp36m.tar.gz"
            url = "https://github.com/PhysiCell-Tools/intracellular_libs/raw/main/ode/libs/macos/roadrunner-osx-10.9-cp36m.tar.gz"
    elif os_type.lower().startswith("win"):
        rr_file = "roadrunner-win64-vs14-cp35m.zip"
        url = "https://sourceforge.net/projects/libroadrunner/files/libroadrunner-1.4.18/" + rr_file + "/download"
    elif os_type.lower().startswith("linux"):
        rr_file = "cpplibroadrunner-1.3.0-linux_x86_64.tar.gz"
        url = "https://sourceforge.net/projects/libroadrunner/files/libroadrunner-1.3/" + rr_file + "/download"
    else:
        print("Your operating system seems to be unsupported. Please submit a ticket at https://sourceforge.net/p/physicell/tickets/ ")
        sys.exit(1)

    # fname = url.split('/')[-2]
    fname = url.split('/')[-1]
    print("fname = ",fname)

    # home = os.path.expanduser("~")
    print('libRoadRunner will now be installed into this location:')
    # dir_name = os.path.join(home, 'libroadrunner')
    dir_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'addons', 'libRoadrunner')
    print(dir_name + '\n')
    # print('   - Press ENTER to confirm the location')
    # print('   - Press CTL-C to abort the installation')
    # print('   - Or specify a different location below\n')
    prompt_str = '[' + dir_name + '] >>> '
    try:
        # response = input(prompt_str)
        # if (response == ""):
        if (True):
            # print('got Enter')
            if not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name)
                except:
                    print('Error trying to create directory: ',dir_name)
                    exit(1)
        # else:
        #     print(type(response))
        #     dir_name = os.path.expanduser(response)
        #     if not os.path.exists(dir_name):
        #         try:
        #             os.makedirs(dir_name)
        #         except:
        #             print('Error trying to create directory: ',dir_name)
        #             exit(1)
    except:
        print('  installation canceled\n')
        exit(1)

    print('Beginning download of libroadrunner into ' + dir_name + ' ...')
    print(url)

    my_file = os.path.join(dir_name, fname)
    print('my_file = ',my_file)

    if os_type.lower().startswith("win"):
        rrlib_dir = my_file[:-4]
    else:  # darwin or linux
        rrlib_dir = my_file[:-7]
        rrlib_dir = my_file[:-6]
    print('rrlib_dir = ',rrlib_dir)

    def download_cb(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize: # near the end
                sys.stderr.write("\n")
        else: # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))

    urllib.request.urlretrieve(url, my_file, download_cb)

    sys.exit(-1)

    new_dir_name = "roadrunner"
    os.chdir(dir_name)
    print('installing (uncompressing) the file...')
    if os_type.lower().startswith("win"):
        try:
            with zipfile.ZipFile(rr_file) as zf:
                zf.extractall('.')
            os.rename("roadrunner-win64-vs14-cp35m", new_dir_name)
        except:
            print('error unzipping the file')
            exit(1)
    else:  # Darwin or Linux
        try:
            print("-- attempt to extract from the tar file...", rr_file)
            tar = tarfile.open(rr_file)
            tar.extractall()
            tar.close()
            if 'darwin' in os_type.lower():
                if "ARM64" in platform.uname().version:
                    print("--- TODO: rename ARM64 lib dir")
                    sys.exit(-1)
                    # os.rename("roadrunner-osx-10.9-cp36m", new_dir_name)
                else:
                    os.rename("roadrunner-osx-10.9-cp36m", new_dir_name)
            else:
                os.rename("libroadrunner", new_dir_name)
        except:
            print('error untarring the file')
            exit(1)

    print('Done.\n')

    # # LIBRR_DIR := /Users/heiland/libroadrunner/roadrunner-osx-10.9-cp36m
    # print("Replace the following variables in your PhysiCell Makefile with these:\n")
    # #print("LIBRR_DIR := /Users/heiland/libroadrunner/roadrunner-osx-10.9-cp36m")
    # print("LIBRR_DIR := " + rrlib_dir)
    # if os_type == 'Windows':
    #     print("LIBRR_LIBS := " + rrlib_dir + "/bin\n")
    # else:
    #     print("LIBRR_LIBS := " + rrlib_dir + "/lib\n")
