# This File here will handle the "anaylze request" from the Django Framework
# The file must be able to handle the configuration items that have been sent from the analyze request.


import os
from .scripts import plotting as plot

#basicconfig = 'b'
#windowsize = '1000'

'''
Function Name: ScriptProcessor
Description: Compiles all of Stefan's old script to turn a single pcap file into a csv of either benford or zipf
Input: filepath with the name/extension and configuration item (assumed to be strings)
Output: Returns a HTTPResponse that will contain the graph from plotting.py to be displayed to the front end.
'''


def ScriptProcessor(basicconfig, windowsize):

    file_name = 'dump2077'

    path = 'pcaps/' + file_name
    print(path)

    if arguments_valid(path, basicconfig, windowsize):

        #os_command = 'ls'
        os_command = 'bash -c "tcpdump -nnr ' + path + ' >> ' + path + '.tcpd"'
        print(os_command)
        os.system(os_command)

        pcapconvertcommand = 'bash -c "python3 hyprfire_app/old_scripts/PcapToN2DConverter.py ' + path + '.tcpd"'
        print(pcapconvertcommand)
        os.system(pcapconvertcommand)

        if basicconfig == 'Benford':

            newbasiccommand = 'bash -c "python3 hyprfire_app/old_scripts/NewBasics3.py --win ' + windowsize + ' ' + path + '.tcpd.n2d +b +t"'
            print(newbasiccommand)
            file_type = 'benf_time'
            os.system(newbasiccommand)

        elif basicconfig == 'z':

            newbasiccommand = 'bash -c "python3 hyprfire_app/old_scripts/NewBasics3.py --win ' + windowsize + ' ' + path + '.tcpd.n2d +z +t"'
            print(newbasiccommand)
            file_type = 'zipf_time'
            os.system(newbasiccommand)

        else:
            print("Enter a proper configuration item, please")

        print("SCRIPT PROCESSOR is DONE!")

        csv_file = path + '.tcpd.n2d' + '_' + file_type + '.csv'

        response = plot.get_plot(csv_file)

        return response

    else:
        print("Error Processing")


'''
Function Name: arguments_valid
Description: This function checks if the configuration items sent from the front end are valid
Input: filename, configuration item +b/+z and window size (1000/2000)
Output: returns a boolean
'''


def arguments_valid(name, config, size):
    if check_filename(name) and check_config(config) and check_size(size):
        check = True
    else:
        check = False

    return check


'''
Function Name: check_filename
Description: Checks if a file name exists or if it is a valid file/directory
Input: a filepath - currently been set to the project's pcaps folder
Output: A boolean
'''


def check_filename(name):
    # results = True
    results = os.path.exists(name)
    # print(results)
    print(results)
    return results


'''
Function Name: check_config
Description: Checks the configuration item that has been entered, either if its a benford or zipf
Input: A character to determine what configuration to use
Output: A boolean
'''


def check_config(config):
    results = False

    if config == 'Benford':
        results = True
    elif config == 'z':
        results = True

    return results


'''
Function Name: check_size
Description: Checks if the windows size entered in the configuration is valid
Input: A string that is able to be type casted to be an integer
Output: A boolean
'''


def check_size(size):
    int_size = int(size)
    results = False

    if int_size == 1000:
        results = True
    elif int_size == 2000:
        results = True

    return results
