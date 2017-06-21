# /**********************************/
# /*       Copyright (c) 2014       */
# /*   Riverbed Technology, Inc.    */
# /*      All Rights Reserved.      */
# /**********************************/
"""
Generates an example line chart of transactioncounts over time,
grouped by a field that users can search for in TTW (for example: URL).

According to the file 'transactioncount_example.info', when a user runs the
transactioncount_example operator, we will execute the "plugin_main" function
that is defined below.

"""

# First we import all of the modules that we are going to use...

# This module gives us access to the TTW Application Programming Interface
import ttw

# This module allows us to create graphs
import ttw.graph

# This module is used to work with dates and times
import datetime

# This module is used for printing debug messages to the browser window
import logging


# Next we define our functions that are going to describe
# what this operator should do.
#
## PYTHON LESSON
##
## Organizing blocks of code into functions also helps with simplifying and
## structuring your code well. It improves readability of the code.
##
## A Python function takes in some input (optional), does some set
## of calculations, and returns some output (optional).
## Python functions are defined using the 'def' keyword,
## and any input (arguments) are specified inside the parentheses.
## Functions can be called more than once in a Python script,
## and they are useful when a specific set of calculations
## must be done multiple times.


def plugin_main():
    """
    This function contains the main logic for the transactioncount_example
    operator. It executes the following steps:

        1. Get the information that the user entered on the TTW search bar
        2. Determine what string was passed in for the group_by argument
        3. Create a blank chart
        4. Set up a query to be executed in TTW
        5. Run the query and iterate over the results
        6. Create the output page that will be displayed to the user
        7. Send the Output Page back to TTW

    """

    # Before we start doing the operator steps,
    # let's demonstrate how to print debug messages.
    #
    # Note: The logger name must begin with "plugins."
    #
    # The debug function will print a message to the browser window
    # if the user runs the operator with the '--debug' option
    logger = logging.getLogger("plugins.my_example")
    logger.debug("This is a debug message. Hello!")


    # Step 1. Get the information that the user entered on the TTW search bar
    # The get_user_inputs() function will return a dictionary,
    # which we are going to store in the variable 'input_data'.
    #
    ## PYTHON LESSON
    ##
    ## A dictionary is a collection of key:value pairs, and is useful
    ## for when you want to associate one thing with another. You can
    ## think of it like an actual English language dictionary (i.e. Webster's
    ## Dictionary), where English words (the keys) are associated with
    ## definitions (the values).
    ##
    ## For example, we can create a dictionary to map animals to the sounds
    ## that they make using a Python dictionary.  Here is an example:
    ##
    ##    animal_dict = {}
    ##    animal_dict["dog"] = "bark"
    ##    animal_dict["cat"] = "meow"
    ##
    ##    print "A dog says", animal_dict["dog"]
    ##
    ## Note that Python dictionaries use square brackets to set a value
    ## for a key, or to look up an existing value already associated
    ## to a key.
    input_data = ttw.get_user_inputs()


    # TTW operators allow users to pass in information using pre-defined
    # arguments. This operator lets a user pass in a value for the
    # argument 'group_by', as specified in the operator's .info file.

    # Step 2. Determine what string was passed in for the group_by argument
    #
    # Note: If the user did not use the 'group_by' argument,
    #       it will contain the default value that is defined for it in
    #       the .info file (transactioncount_example.info).
    group_by_field = input_data['group_by']



    # Step 3. Create a blank chart.
    #
    # Note: The ttw.graph module contains many different kinds of charts.
    chart = ttw.graph.MultiLineGraph()

    # Let's turn on the chart legend
    chart.set_legend(True)


    # Step 4. Set up a query to be executed in TTW.
    # A query will send search parameters to TTW and TTW will send back
    # a list of results. This is similar to what happens when you search
    # for transactions on the TTW search screen.
    #
    # Create an index query object. An index query will return the number of
    # transactions for each value of a given field. For example, the results
    # might look something like this for URL:
    #
    #    http://google.com : 5
    #    http://amazon.com : 9
    #    ...
    #
    #
    # Note: See the documentation for the IndexQuery class to explore the
    # different ways to set up and use this query.
    query = ttw.create_index_query()

    # Set the TTW field that we want to group the results by
    #
    # The variable we created named "query" is an object,
    # and we are calling the set_index_field method of that object.
    query.set_index_field(group_by_field)

    # Set the number of buckets we wish to use. For now, let's use 30 buckets.
    # TTW will report transaction counts for each field value,
    # broken down into 30 intervals over the search period.
    query.set_num_buckets(50)

    # Let's only ask for the top 20 results, otherwise our
    # chart could look messy if there is too much data on it.
    query.set_num_results(50)


    # Step 5. Run the query and iterate over the results.
    # The 'get_results' function will both execute the query
    # in TTW and let us iterate over the results. For the index query,
    # each result is a dictionary.
    #
    ## PYTHON LESSON
    ##
    ## We are going to use a 'for' loop to visit each result from the query
    ## and do something with it. The Python syntax of a 'for' loop is:
    ##
    ##     for <x> in <iterable>:
    ##
    ## where x can have any name you wish (in our case, we used
    ## the word 'result'). For each iteration of the 'for' loop,
    ## 'result' will represent one of the results returned by the TTW query.

    for result in query.get_results():

        # Recall that we set a group_by field for the index query, so
        # each result will represent one of these groups. We can get the
        # name of this group by looking up what is associated with the
        # word "value" in the dictionary. For example, if we grouped by URL,
        # the field value might be "http://google.com".
        field_value = result['value']


        # When we built the index query, we asked TTW to bucketize the results.
        # For each result value, a list of the number of hits and the
        # start time of the bucket are associated with the 'time_series' key.
        for data in result['time_series']:

            # Each data point contains the start time and the number of
            # transactions that match the current field value for that bucket.

            #  Get the time that this data point represents.
            #  We will call a function to make this time more readable
            #  to the user.
            data_x_value = format_timestamp(data['time'])

            #  Get the number of transactions that occurred for this time bucket
            data_y_value = data['hits']

            # Now, we can add our data point to the chart.
            # We will use the field_value as the data series name in the chart.
            chart.add_data_point(field_value, data_x_value, data_y_value)



    # Step 6. Create the output page that will be displayed to the user
    # We do this by creating an OutputPage object defined in
    # the ttw.html module.
    #
    # Note: The ttw.html module contains numerous types of HTML elements
    # that can be added to an OutputPage. These include tables, images,
    # and text. For more information on how to format your OutputPage,
    # see the documentation for the ttw.html module.
    output_page = ttw.html.OutputPage()


    # Create a title for the page.
    #
    ## PYTHON LESSON
    ##
    ## To insert a variable into a string, use the % operator. For example,
    ## here are using %s to insert one string into another.
    ## For more information on formatting strings, see the Python documentation.
    report_title = "Transactions Grouped by Queue"

    # Tell the output page that we want to use the report title that we created
    output_page.set_title(report_title)

    # Add our chart to the output page.
    output_page.append_element(chart)

    # Step 7. Send the Output Page back to TTW
    ttw.set_output(output_page)



def format_timestamp(timestamp):
    """ This function will convert a timestamp (in msec) to a human
        readable string. Note that the timestamp should be an epoch
        timestamp, which designates 0 as midnight on Jan. 1, 1970.
    """

    # This is a two-step process.

    # First we use the datetime.datetime module to convert our timestamp
    # to a datetime object. This module wants the timestamp to be in seconds,
    # so be sure to divide by 1000 to put the timestamp
    # in seconds first.
    datetime_object = datetime.datetime.fromtimestamp(timestamp/1000.)

    # Using our datetime object, we can generate a string using any format
    # we like.  In this case, %H is the hour and %M is the minute.
    # There are other codes you can use. See the list of codes in the Python
    # documentation for the datetime module.
    timestamp_as_string = datetime_object.strftime("%m/%d/%y %H:%M")

    # Finally, we return our properly formatted string back to the caller
    return timestamp_as_string
