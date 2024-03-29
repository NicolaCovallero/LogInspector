# Log Parser

This repository contains a simple log parser program.

Given the nature of logs, overall for robotics, there are a lot of informations to parse when we are interested only on few of them when testing. Moreover, when testing, it is likely that the same test is done several times, let's think about when we are tuning a controller. You could use program like Visual Studio Code or Notepad++ to parse the log and convert it to a format like CSV that can be inspected afterwards by programs like PlotJuggler to have charts very usefull for debugging, but you are likely doing the same sequence of operations manually, this is time consuming and error prone. 

Let's automatize it!

This log parser allows you to parse any file with a sequence of operations based on regular expressions.

Currently the only operations supported are:

1.  Find: for each line find all the characters matching with the regual expression.
2.  Replace: for each line replace all the characters matching with the regular expression and substitute them.

A sequence of operation is called **configuration**, and they can optionally have a header field, if there is the parsed file is the result of the last regular expression appended to the header. The purpose of the header is to add the name of columns, these might be usefull when you will use your parsed file by programs like PlotJuggler.

Notice that the program is though to output CSV files but it is not contrasined to them. Due to this flexibility there is no control on how the resulting parsed file is. It is your responsability to provide the right regular expressions accordingly to the input text domain.

My suggestion is to provide easy and unique identifiable set of characters to constraints the data you are interested about in your test so the parsin is easy and effortless.

This program comes with two programs:

1.  A GUI **log_config_creator.py** to easily design your configuration file given an input file to parse. With this you can save your configuration and also the parsed file. This program needs the qt5 installed, for this reason install the requirements.
I suggest to create a virtual environment.

2.  A command line program **log_parser.py** to parse an input file given the input configuration. This program is minimal and it does noy depend on qt5, you should be able to run it with a basic python installation.

Everthing has been tested with Python 3.8

## Example

You can see the potential of this little program on the [sample.log](sample.log) (open it with CTRL-O), if parsed with the configuration [sample.json](sample.json) (to load it CTRL-L) outputs the file [sample.csv](sample.csv) which can be fed to program that needs CSV files. 
x
The log is a very simple log with no particular meaning, and so the parsing sequence is jsut for demonstration purposes.

## TIPS

Learning in detail how to use regular expression might be cumbersome for some people, and maybe not that usefull for their job. With this tool you can do the most of the things by knowing the two most important expressions:

*   **.\*** allows to match any character. So you can simply delimitate the part of the log you want to analyse but easy identifiable characters, such as START_LINE and END_LINE, so if you could use the follwoing expressions **START_LINE.\*END_LINE**, and afterwards get rid of the characters you are not interested about.
*   | allows you to merge multiple expressions into one, it works as an OR boolean operator. For instance, if you want to find two different lines you could use the following **START_LINE1.\*END_LINE1|START_LINE2.\*END_LINE2** the same works for the replace operator.

## Attributions
For this app some icons from the Fugue Icons icon pack has been used. 

Fugue Icons

(C) 2013 Yusuke Kamiyamane. All rights reserved.

These icons are licensed under a Creative Commons
Attribution 3.0 License.
<http://creativecommons.org/licenses/by/3.0/>
