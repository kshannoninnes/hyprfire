# This File here will handle the "anaylze request" from the Django Framework
# The file must be able to handle the configuration items that have been sent from the analyze request.

import os
from .scripts import plotting as plot


def ScriptProcessor(file_name, algorithm_type, windowsize):
    """
     ScriptProcessor
     Compiles all of Stefan Prandl's old scripts to turn a single pcap file into a csv of either benford or zipf

     Parameters
     filename: the base pcap file (found in the hyprfire/pcaps directory)
     algorithm_type: whether to use benfords or zipf algorithm
     windowsize: the window size of the pcap analysis done in NewBasics3.py script

     Returns
     HTML/JavaScript to display a plotly generated graph based on the data from the pcap
     """

    pcaptoN2D = os.path.abspath("hyprfire_app/old_scripts/PcapToN2DConverter.py")
    newbasics = os.path.abspath("hyprfire_app/old_scripts/NewBasics3.py")

    # Checks if arguments being passed through is valid
    if arguments_valid(file_name, algorithm_type, windowsize):

        # This section is temporary, new scripts will be replacing this messy section

        os_command = 'bash -c "tcpdump -nnr ' + file_name + ' >> ' + file_name + '.tcpd"'
        print(os_command)
        os.system(os_command)

        pcapconvertcommand = 'bash -c "python3 ' + pcaptoN2D + ' ' + file_name + '.tcpd"'
        print(pcapconvertcommand)
        os.system(pcapconvertcommand)

        mv_tcpd = 'bash -c "rm ' + file_name + '.tcpd"'
        print(mv_tcpd)
        os.system(mv_tcpd)

        # Checks what type of alrgorithm to use

        if algorithm_type == 'Benford':

            newbasiccommand = 'bash -c "python3 ' + newbasics + ' ' + '--win ' + windowsize + ' ' + file_name + '.tcpd.n2d +b +t"'
            print(newbasiccommand)
            file_type = 'benf_time'
            os.system(newbasiccommand)

        elif algorithm_type == 'Zipf':

            newbasiccommand = 'bash -c "python3 ' + newbasics + ' ' + '--win ' + windowsize + ' ' + file_name + '.tcpd.n2d +z +t"'
            print(newbasiccommand)
            file_type = 'zipf_time'
            os.system(newbasiccommand)

        else:
            print("Enter a proper configuration item, please")

        # This is just moving the csv file to a temporary file for now, will be removed when new scripts come in

        mv_n2d = 'bash -c "rm ' + file_name + '.tcpd.n2d"'
        print(mv_n2d)
        os.system(mv_n2d)

        csv_file = file_name + '.tcpd.n2d' + '_' + file_type + '.csv'

        # Get the plotly graph to return to the views.py
        response = plot.get_plot(csv_file)

        temp = os.path.abspath("temp")
        mv_csv = 'bash -c "mv ' + csv_file + ' ' + temp + '"'
        print(mv_csv)
        os.system(mv_csv)

        print("SCRIPT PROCESSOR is DONE!")

        return response

    else:
        raise ValueError("Error in Processing Arguments: filenames, algorithm, windowsize")


def arguments_valid(name, algorithm, size):
    """
    Function Name: arguments_valid
    This function checks if the configuration items sent from the front end are valid

    :param name: the name of the file (path included)
    :param algorithm: the type of algorithm being used.
    :param size: the window size for the amount of pcaps to analyze
    :return: True if all checks passes, False if at least one fails
    """

    if check_filename(name) and check_config(algorithm) and check_size(size):
        check = True
    else:
        check = False

    return check


def check_filename(name):
    """
    Funcion name: check_filename
    Checks if a file exist or not, throws an exception if it does not exist.

    :param name: the name of the file (including its path)
    :return: True if file exist, ValueError if file does not exist
    """

    results = os.path.exists(name)

    if results == False:

        raise ValueError("Incorrect File name!")
    print(results)
    return results


def check_config(algorithm):
    """
    Function Name: check_config
    Checks the algorithm thats been passed through the function,

    :param algorithm:
    :return:
    """
    results = False

    if algorithm == 'Benford':
        results = True
    elif algorithm == 'Zipf':
        results = True

    return results


def check_size(size):
    """
    Function Name: check_size
    Checks the size of the Window for analysis, currently it is checking if it is either 1000 or 2000, (subject to change)

    :param size: a string that is converted to an integer
    :return: True if size is either 1000 or 2000, False otherwise
    """
    int_size = int(size)
    results = False

    if int_size == 1000:
        results = True
    elif int_size == 2000:
        results = True

    return results
