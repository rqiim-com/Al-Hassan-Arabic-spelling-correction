# -*- coding: utf-8 -*-


import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')
# parser = argparse.ArgumentParser(description='Converts characters in Arabic free text to integers')
# parser.add_argument('-corpus', type=str, help='Path to the Arabic Corpus', required=True)
# parser.add_argument('-hamza', help='Include Hamzas as a letter', default='', nargs='?')
# parser.add_argument('-madda', help='Include Alefs with Madda on top as a separate letter (otherwise just Alef)',
#                     default='', nargs='?')
# parser.add_argument('-t', help='Include Tar Marbuta as a letter', default='', nargs='?')
# parser.add_argument('-harakat', help='Include diacritics as separate letters (otherwise stripped)', default='',
#                     nargs='?')
# parser.add_argument('-tatweel', help='Include tatweel as an underscore', default='', nargs='?')
# parser.add_argument('-toUTF', help='Take ASCII to Abjad', default='', nargs='?')
#
# args = parser.parse_args()
toUTF=True
hamza=True
madda =True
harakat=False
tatweel=False
corpus="/home/razzaz/Desktop/Data/FeaturedArticleFromRaqim/all.utf8.buck.arabiconly"
outFile=codecs.open("/home/razzaz/Desktop/Data/FeaturedArticleFromRaqim/all.utf8.buck.arabiconly.arabic",'w',encoding='utf-8')
NotConvertedFile=codecs.open("/home/razzaz/Desktop/Data/QALB-0.8.0-April08-2015-SharedTask/all.correct.new.notConvArabic",'w',encoding='utf-8')
abjad = {u"\u0627": 'A',
         u"\u0628": 'b', u"\u062A": 't', u"\u062B": 'v', u"\u062C": 'j',
         u"\u062D": 'H', u"\u062E": 'x', u"\u062F": 'd', u"\u0630": '*', u"\u0631": 'r',
         u"\u0632": 'z', u"\u0633": 's', u"\u0634": '$', u"\u0635": 'S', u"\u0636": 'D',
         u"\u0637": 'T', u"\u0638": 'Z', u"\u0639": 'E', u"\u063A": 'g', u"\u0641": 'f',
         u"\u0642": 'q', u"\u0643": 'k', u"\u0644": 'l', u"\u0645": 'm', u"\u0646": 'n',
         u"\u0647": 'h', u"\u0648": 'w', u"\u0649": 'Y', u"\u064A": 'y'}

# Create the reverse
alphabet = {}
if toUTF :
    for key in abjad:
        alphabet[abjad[key]] = key

abjad[u"\u0629"] = 'p'

# Hamza
if hamza :
    abjad[u"\u0621"] = '\''
    abjad[u"\u0623"] = '>'
    abjad[u"\u0625"] = '<'
    abjad[u"\u0624"] = '&'
    abjad[u"\u0626"] = '}'
    abjad[u"\u0654"] = '\''  # Hamza above
    abjad[u"\u0655"] = '\''  # Hamza below
else:
    abjad[u"\u0621"] = ''
    abjad[u"\u0623"] = 'A'
    abjad[u"\u0625"] = 'A'
    abjad[u"\u0624"] = ''  # I don't think that the wa is pronounced otherwise ...
    abjad[u"\u0626"] = ''  # Decide ...
    abjad[u"\u0654"] = ''
    abjad[u"\u0655"] = ''

# Alef with Madda on Top
if madda :
    abjad[u"\u0622"] = '|'
else:
    abjad[u"\u0622"] = 'A'

# Vowels/Diacritics
if harakat :
    abjad[u"\u064E"] = 'a'
    abjad[u"\u064F"] = 'u'
    abjad[u"\u0650"] = 'i'
    abjad[u"\u0651"] = '~'
    abjad[u"\u0652"] = 'o'
    abjad[u"\u064B"] = 'F'
    abjad[u"\u064C"] = 'N'
    abjad[u"\u064D"] = 'K'
else:
    abjad[u"\u064E"] = ''
    abjad[u"\u064F"] = ''
    abjad[u"\u0650"] = ''
    abjad[u"\u0651"] = ''
    abjad[u"\u0652"] = ''
    abjad[u"\u064B"] = ''
    abjad[u"\u064C"] = ''
    abjad[u"\u064D"] = ''

# Tatweel
if tatweel:
    abjad[u"\u0640"] = '_'
else:
    abjad[u"\u0640"] = ''

## Make sure mapping is right
# for key in abjad:
#  print key,
#  print " ",
#  print abjad[key]
if not toUTF :
    with codecs.open(corpus, 'r', encoding='utf-8') as f:
        for line in f:
            flag = 0
            for char in line:
                if "ک" in line or "ی" in line:
                    continue
                if char==" " or char=='\t'or char=='\n' or char=="." or char== "؟" or char =="،" or char=="؛":
                    outFile.write(char)
                    continue
                if char in abjad:
                    outFile.write(abjad[char])
                else:
                    # Leaving this in. Run iconv to see if all characters were caught
                    flag=1
                    NotConvertedFile.write(char)
            if flag==1:
                NotConvertedFile.write('\n')
    outFile.flush()
    NotConvertedFile.flush()
    outFile.close()
    NotConvertedFile.close()

# Take Buckwalter Transliterated Text and put it in vernacular
if toUTF :
    alphabet['|'] = u"\u0622"
    alphabet['a'] = u"\u064E"
    alphabet['u'] = u"\u064F"
    alphabet['i'] = u"\u0650"
    alphabet['~'] = u"\u0651"
    alphabet['o'] = u"\u0652"
    alphabet['F'] = u"\u064B"
    alphabet['N'] = u"\u064C"
    alphabet['K'] = u"\u064D"
    alphabet['\''] = u"\u0621"
    alphabet['>'] = u"\u0623"
    alphabet['<'] = u"\u0625"
    alphabet['&'] = u"\u0624"
    alphabet['}'] = u"\u0626"
    alphabet['p'] = u"\u0629"

    if not harakat:
        alphabet['a'] = ""
        alphabet['u'] = ""
        alphabet['i'] = ""
        alphabet['~'] = ""
        alphabet['o'] = ""
        alphabet['F'] = ""
        alphabet['N'] = ""
        alphabet['K'] = ""
    flag=0
    with codecs.open(corpus, 'r', encoding='utf-8') as f:
        for line in f:
            if "ک" in line  or   "ی"in line:
                    continue
            for char in line:
                if char == " " or char == '\t' or char == '\n' or char == "." or char == "؟" or char == "،" or char ==  "؛" or char=="“" or char=='‘':
                    outFile.write(char)
                    continue
                if char in alphabet:
                    outFile.write(alphabet[char])

                else:
                    flag=1
                    NotConvertedFile.write(char)
                    outFile.write("__")
            if flag==1:
                NotConvertedFile.write('\n')
                NotConvertedFile.flush()
    outFile.flush()
    outFile.close()
    NotConvertedFile.close()