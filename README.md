# Nessus Audit Lang Helper Tools

I work with custom Nessus .audit files extensively on a day to day basis. Here are some tools I've developed to make it a little less painful. 


## Audit Formatter

The Formatter script is a Python tool designed to make Tenable .audit files easier to read and work with. It formats through indentation and commenting, leaving original content intact. The idea is to use this format in conjunction with folding in Visual Studio Code or similar to allow you to clearly follow logic flows or break out specific checks to work on. The script takes a command line input specifying the filename, and it outputs the formatted version with the "_formatted" suffix appended to the original filename.

## Check Condenser

This is a simple interface that allows you to paste in multi-part checks and transform them into one logic-bound report. Tenable is moving in the direction of this format for it's new files, so this can help rapidly convert legacy or custom checks you need. 

I recommend moving to this format, as it gives a much cleaner output for each control. 

## Tag Checker

Working in a secure environment, I can't use the VS Studio code extension container that automatically checks audit files. I was spending far too much time trying to find the problem in my file, only to find it was a missing tag. This script attempts to help out, counting the relevant logic opening/closing tags and giving a line number when it notices something missing. Not super robust, and I haven't gotten it to correctly identify a missing </if> , but everything else works. Helpful, if not super robust. 



