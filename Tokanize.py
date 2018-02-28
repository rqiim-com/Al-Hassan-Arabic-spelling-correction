# -*- coding: utf-8 -*-

from xml.dom import minidom
import os
def tokanize(sen,infile,outfile,madaMiraPath):
    outputfileName= outfile
    inputFileName= infile
    input=sen
    inputXML='<madamira_input xmlns="urn:edu.columbia.ccls.madamira.configuration:0.1">\n\t<madamira_configuration>\n\t\t<preprocessing sentence_ids="false" separate_punct="true" input_encoding="UTF8"/>\n\t\t<overall_vars output_encoding="UTF8" dialect="MSA" output_analyses="TOP" morph_backoff="NONE"/>\n\t\t<tokenization>\n\t\t<scheme alias="D34MT"/>\n\t\t</tokenization>\n\t</madamira_configuration>\t\n<in_doc id="ExampleDocument">\n\t\t<in_seg id="SENT1">' +input+'</in_seg>\n\t</in_doc>\n</madamira_input>'
    outFile=open(inputFileName,'w')
    outFile.write(inputXML)
    outFile.flush()
    outFile.close()
    command="java -jar "+madaMiraPath+ " -c -i " + inputFileName + " -o " + outputfileName
    print command
    os.system(command)
    xmldoc=minidom.parse(outputfileName)
    itemlist = xmldoc.getElementsByTagName('word')

    for s in itemlist:
        print s.getAttribute("word")

        x=s.getElementsByTagName("tokenized")[0]
        list=x.childNodes
        for f in list:
            if f.nodeType != minidom.Node.TEXT_NODE:
                print f.getAttribute("form0")

        print "------------------"

madaMiraPath="/home/razzaz/Desktop/tools/MADAMIRA-release-20150421-2.1/MADAMIRA-release-20150421-2.1.jar"
tokanize("الأحمد","./in","./out",madaMiraPath)