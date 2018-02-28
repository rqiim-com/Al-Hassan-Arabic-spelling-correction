# -*- coding: utf-8 -*-
import kenlm
model = kenlm.LanguageModel('/home/razzaz/Desktop/Raqim/languageModelTools/kenlm/txt.arpa')
s=model.score('nfsh wbdyn ElY	')
print "1 "+str(s)
s=model.score('nfsh wbdyn ')
print "2"+str(s)