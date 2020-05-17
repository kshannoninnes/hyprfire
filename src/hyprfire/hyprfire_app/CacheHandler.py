# This File here will handle the "anaylze request" from the Django Framework
# The file must be able to handle the configuration items that have been sent from the analyze request.

import os
from .new_scripts import pcapconverter, packetdata_converter, plot_csvdata
from .models import Data


def CacheHandler(file_name, algorith_type, windowsize, analysis):
    """
    CacheHandler
    This function does the "caching" section of the application. It does a quick check in the database if there is an
    item that has the exact: filename, algorithm_type, windowsize and analysis.
    If it does it will then grab it from the data instead.

    Else it will run the ScriptProcessor, then save the data to the database at the end.

    :param file_name: the filepath/name of the pcap file to search for/process
    :param algorith_type: either Benford or Zipf
    :param windowsize: an integer on
    :param analysis:
    :return:
    """

    # Gets a queryset from the database on how many Data of the same filename, algorithm, windowsize and analysis
    result = Data.objects.filter(filename=file_name, algorithm=algorith_type, window_size=windowsize, analysis=analysis)

    if len(result) != 0:
        # If it is more than 0 then it exists in the database, and just pull the data from there.
        print("Item already exists in the database.... pulling cached data")
        csv_data = Data.objects.get(filename=file_name, algorithm=algorith_type, window_size=windowsize, analysis=analysis)
        csv_data = csv_data.data

    else:
        csv_data = ScriptProcessor(file_name, algorith_type, windowsize, analysis)

        # Create a new Object (ORM)
        database = Data.objects.create(filename=file_name, algorithm=algorith_type, window_size=windowsize,
                                       analysis=analysis, data=csv_data)
        # Save it to the database
        database.save()

    response = plot_csvdata.get_plot(csv_data)

    return response


def ScriptProcessor(file_name, algorithm_type, windowsize, analysis):
    """
     ScriptProcessor
     Uses the new scripts that were derived from Stefan's old Script. Uses memory based handling instead of reading
     and creating new files

     Parameters
     filename: the base pcap file (found in the hyprfire/pcaps directory)
     algorithm_type: whether to use benfords or zipf algorithm
     windowsize: the window size of the pcap analysis done in NewBasics3.py script

     Returns
     HTML/JavaScript to display a plotly generated graph based on the data from the pcap
     """

    # Checks if arguments being passed through is valid
    if arguments_valid(file_name, algorithm_type, windowsize, analysis):

        print("Starting Sprint Processor")

        dumpfile = pcapconverter.pcapConverter(file_name)

        if algorithm_type == 'Benford':

            algorithm = 'b'

        elif algorithm_type == 'Zipf':

            algorithm = 'z'

        else:
            raise ValueError("Incorrect Algorithm Type")

        if analysis == 'Length':

            analysis_type = 'l'

        elif analysis == 'Time':

            analysis_type = 't'

        else:
            raise ValueError("Incorrect Analysis type")

        csv_data = packetdata_converter.convert_to_csv(dumpfile, algorithm, int(windowsize), analysis_type)

        print("SCRIPT PROCESSOR is DONE!")
        print(csv_data)

        return csv_data # csv_data is the real return value for this method. Commenting out so we can skip the databasing for now.

    else:
        raise ValueError("Error in Processing Arguments: filenames, algorithm, windowsize or analysis type")


def arguments_valid(name, algorithm, size, analysis):
    """
    Function Name: arguments_valid
    This function checks if the configuration items sent from the front end are valid

    :param name: the name of the file (path included)
    :param algorithm: the type of algorithm being used.
    :param size: the window size for the amount of pcaps to analyze
    :return: True if all checks passes, False if at least one fails
    """

    if check_filename(name) and check_config(algorithm) and check_size(size) and check_analysis(analysis):
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
    :return: True if size is greater than 0, a value error if it is not
    """
    int_size = int(size)

    if int_size > 0:
        results = True
    else:
        raise ValueError("Cannot have a window size less than or equal to 0")

    return results


def check_analysis(analysis):
    """
    Function Name: check_analysis
    Checks the analysis variable that was passed through, it is checking if it is length vs time based.

    :param analysis: a string that identifies a configuration option (time/length)
    :return: response, a boolean type variable.
    """
    if analysis == 'Time':
        response = True
    elif analysis == 'Length':
        response = True
    else:
        response = False

    return response

