Arabic spelling checker:

A software and web API for detecting Arabic miss spelled words and also suggests a list of words that may be the correct one based on the context of the miss spelled words. 
this code is V0.0 Version


Prerequisites

	1-python 2.7
	2-kenlm language mdeol python lib

Getting Started	

	to run this project on your local machine you can use "main.py" file:
		1- open a terminal and change your directory to the project folder	
		2- run the follwing command on your terminal "python main.py" and follow the instructions
	to use the web API: 
		1- open a terminal and change your directory to the project folder	
		2- run the follwing command on your terminal "python webAPI.py" and follow the instructions
		3- you can make a post request to the follwoing 'sereverIPadress/5000/spell/' by the follwing jason data sentence="the sentence you want to correct"
		4- the reply will be in a json format --> word="list of sugesstion" and if it is a correct word word='null' and if it is awrong word but we do't have a sugesstion 			word="no match"
	

Authors

Mohammed ElRazzaz, emai:Mohammed.elrzzaz@gmail.com