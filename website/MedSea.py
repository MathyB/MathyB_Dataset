import streamlit as st
import numpy as np
import os
import pandas as pd
import re
import csv
import base64
from st_aggrid import AgGrid
import webbrowser
from load_css import local_css

st.set_page_config(page_title="MedSea",layout='wide')
local_css("website/style.css")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

def get_table_download_link(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ME_Finder.csv" target="_blank">Download csv file</a>'
    return href

# path for input, output and rules file
OUTPUT_FILE = 'GCC.csv'
RULE_FILE = 'ME_RULES.csv'


me_rules = pd.read_csv(RULE_FILE)



class MEFinder():
    
    def __init__(self):
        
        return
    
    # removing Nan values from list and concatinating operators/expressions with '|'
    def rule_preprocess(self,me_rules,rule_no):
        pattern=[x for x in me_rules.iloc[:,rule_no].values if(x==x)]
        separator='|'
        pattern=separator.join(pattern)
        return pattern
    
    # Rule 1 for math functions like Math.exp, Math.log, Math.tan,etc.(case insensitive)
    def rule1(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)
        reg_pattern = '(?i)\s('+pattern+')[\(](?:[-])?\w+'
        return reg_pattern
    
    # Rule 2 for numbers in scientific notation
    def rule2(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)  
        reg_pattern='(?:[+-])?[\d.]+'+'['+pattern+'][+|-]?\d+\s'
        return reg_pattern
    
    # Rule 3 for constants like Math.PI,inf,Nan (case insensitive)
    def rule3(self,me_rules,rule_no):
        pattern = self.rule_preprocess(me_rules,rule_no)
        reg_pattern = '(?i)[.\s]?('+pattern+')[.;\s]+'
        return reg_pattern
    
    # Rule 4 for numerical sets or sequences contained within closed brackets i.e. {},(),[]
    def rule4(self,me_rules,rule_no):
        pattern=[x for x in me_rules.iloc[:,rule_no].values if(x==x)]
        #print("Rule no",rule_no," pattern:", pattern)
        separator='|'
        reg_pattern_indv=[]
        for i in range(0,len(pattern)-1):
            if(i%2 == 0 and i != len(pattern)-2):
                pattern_indv ='\{}\s*(?:[+-])?\d+(?:[.]\d+)?(?:[,]\s*(?:[+-])?\d+(?:[.]\d+)?)+\s*\{}'.format(pattern[i],pattern[i+1])
                reg_pattern_indv.append(pattern_indv+separator)
            elif(i == len(pattern)-2):
                pattern_indv ='\{}\s*(?:[+-])?\d+(?:[.]\d+)?(?:[,]\s*(?:[+-])?\d+(?:[.]\d+)?)+\s*\{}'.format(pattern[i],pattern[i+1])
                reg_pattern_indv.append(pattern_indv)
            else:
                continue
        reg_pattern=""
        for x in reg_pattern_indv:
            reg_pattern += x 
        return reg_pattern
    
    # Rule 5 for complex numbers : Numbers of the form x+iy,x+yi where x and y can be any real number
    def rule5(self, me_rules, rule_no):
        pattern = self.rule_preprocess(me_rules,rule_no)
        reg_pattern = '\d(?:[.]\d+)?\s*[+-]\s*\d(?:[.]\d+)?\s*[*]?\s*[{}]\s|\d(?:[.]\d+)\s*?[+-]\s*[{}]\s*[*]?\s*\d(?:[.]\d+)\s?'.format(pattern,pattern)
        return reg_pattern
    
    # Rule 6 for sets or sequences containing within closed brackets i.e. {},(),[] constants like 'NaN', 'Math.PI' as in Rule 6
    def rule6(self,me_rules,rule_no):
        pattern_pre = self.rule_preprocess(me_rules, rule_no)
        pattern = '(?i)('+pattern_pre+')'   
        
        pattern_brac = [x for x in me_rules.iloc[:,rule_no].values if(x==x)]
        separator='|'
        reg_pattern_indv=[]
        for i in range(0,len(pattern_brac)-1):
            if(i%2 == 0 and i != len(pattern_brac)-2):
                pattern_indv ='\{}\s*(?:[+-])?'.format(pattern_brac[i])+pattern+'?(?:[,]\s*(?:[+-])?'+pattern+')+\s*\{}'.format(pattern_brac[i+1])
                reg_pattern_indv.append(pattern_indv+separator)
            elif(i == len(pattern_brac)-2):
                pattern_indv ='\{}\s*(?:[+-])?'.format(pattern_brac[i])+pattern+'?(?:[,]\s*(?:[+-])?'+pattern+')+\s*\{}'.format(pattern_brac[i+1])
                reg_pattern_indv.append(pattern_indv)
            else:
                continue
        reg_pattern=""
        for x in reg_pattern_indv:
            reg_pattern+=x  
        return reg_pattern
    
    # Rule 7 for each of the operators +,*,=,%,/,<,>,! and * occuring twice,consecutively, and followed by a digit
    def rule7(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)        
        reg_pattern='['+pattern+']['+pattern+']\s*[0-9]'
        return reg_pattern
    
    # Rule 8 for each of the operators +,*,=,%,/,<,>,! and * occuring atleast once and must be followed by atleast one digit
    def rule8(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)   
        reg_pattern='\s*[\w+|\d+]\s*['+pattern+']['+pattern+']*\s*[0-9]+\s'
        return reg_pattern
    
    # Rule 9 : atleast one digit followed by 0 or more digits and followed by one or two of the operators +,*,=,%,/,<,>,! and * which must be followed by atleast one character and followed by 0 or more characters
    def rule9(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)        
        reg_pattern='\s([0-9]+(?:[.]\d+)?\s*['+pattern+']['+pattern+']\s*[a-zA-Z_]+|[0-9]+(?:[.]\d+)?\s*['+pattern+']\s*[a-zA-Z_]+)\s'
        return reg_pattern
    
    # Rule 10 : atleast one character followed by zero or more characters followed by atleast one of the operators +,*,=,%,/,<,>,! and * which must be followed by atleast one digit and followed by any number of digits
    def rule10(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)        
        reg_pattern='[a-zA-Z_]+\s*['+pattern+']\s*['+pattern+']*[0-9]+\s'
        return reg_pattern
    
    # Rule 11 for contiguous operators and numbers : there must be atleast 2 digits and 2 operators from +,*,=,%,/,<,>,! and *
    def rule11(self,me_rules,rule_no):
        pattern = self.rule_preprocess(me_rules,rule_no)        
        reg_pattern ='['+pattern+']\s*['+pattern+']+\s*[0-9][0-9]+|['+pattern+']\s*[0-9]\s*['+pattern+']+[0-9]+|[0-9]\s*[0-9]+\s*['+pattern+']\s*['+pattern+']\s*[\w+|\d+]'
        return reg_pattern

    #Rule 12 detects dimensions like 250x250 or 250 * 250
    def rule12(self,me_rules,rule_no):
        pattern=self.rule_preprocess(me_rules,rule_no)   
        reg_pattern='\s\d+\s*['+pattern+']\s*['+pattern+']*\s*[0-9]+\s'
        return reg_pattern
    
    def remove_words(self, me_rules, rule_no):
        pattern = [x for x in me_rules.iloc[:,rule_no].values if(x==x)]
        return pattern
   
    # generates a dictionary containing description, status and instances for each Bug_Id
    def apply(self, me_dict, me_rules, file, rule_no, remove_status):
        file_copy = file
        me_dict['Rule_{}_status'.format(rule_no+1)] = {}
        list_obj=[self.rule1(me_rules,rule_no),self.rule2(me_rules,rule_no),self.rule3(me_rules,rule_no)
                  ,self.rule4(me_rules,rule_no),self.rule5(me_rules,rule_no),self.rule6(me_rules,rule_no)
                  ,self.rule7(me_rules,rule_no),self.rule8(me_rules,rule_no),self.rule9(me_rules,rule_no)
                 ,self.rule10(me_rules,rule_no), self.rule11(me_rules,rule_no), self.rule12(me_rules,rule_no)] # list of function calls for ME_rules
        
        if(remove_status):
            index = []
            tokenize = file_copy.split(' ')

            for i in range(len(tokenize)):
                if tokenize[i].find("https") != -1 or tokenize[i].find("http") != -1 or tokenize[i].find("ftp") != -1 :
                    index.append(i)
            
            tokenize_copy = tokenize[:] 
            for i in index:
                tokenize_copy.remove(tokenize[i])
            file_copy = ' '.join(map(str, tokenize_copy))
            
            index = []
            tokenize = file_copy.split(' ')
            remove_words = self.remove_words(me_rules, len(me_rules.columns)-1)
            
            for i in range(len(tokenize)):
                for j in range(len(remove_words)):
                    if tokenize[i].find(remove_words[j]) != -1 :
                        index.append(i)
                        break
            tokenize_copy = tokenize[:] 
            for i in index:
                tokenize_copy.remove(tokenize[i])
            file_copy = ' '.join(map(str, tokenize_copy))
            
        pattern = list_obj[rule_no]
        search_pattern = re.compile(pattern)              # making appropriate function call 
        me_all = search_pattern.findall(file_copy)
        try:
            
            if(search_pattern.search(file_copy)):
                me_dict['Rule_{}_status'.format(rule_no+1)] = 1
                me_dict['Rule_{}_instances'.format(rule_no+1)] = me_all
                return 1
            else:
                me_dict['Rule_{}_status'.format(rule_no+1)] = 0
                me_dict['Rule_{}_instances'.format(rule_no+1)] ='Null'

                return 0
        except:
                me_dict['Rule_{}_status'.format(rule_no+1)] = 0
                me_dict['Rule_{}_instances'.format(rule_no+1)] ='Null'
                return 0


def main():
	st.markdown("<p style='text-align: center; border-style: groove; border-color: #000000;background-color:#D22B2B;  color:#ffffff; font-family:times new roman; font-size:50px; font-weight: bold;'>MEDSEA:<br><span class='highlight'>MATHEMATICAL EXPRESSIONS IN SOFTWARE ENGINEERING ARTIFACTS </span></p>", unsafe_allow_html=True)
	st.text("")
	st.text("")
	
	
	#st.markdown( """<a style='display: block; text-align: center; font-family:times new roman; font-size:20px;' href="https://github.com/MathyB/MathyB_Dataset">Github Repository</a> """, unsafe_allow_html=True, )
	st.markdown("[![Github](data:image/png;base64,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)](https://github.com/MathyB/MathyB_Dataset)")
		
	st.text("")
	st.text("")

	st.markdown("<h2 style='text-align: center; border-style: ridge; font-family:serif; font-size:20px; font-weight:bold;'> EXAMPLES </h2>", unsafe_allow_html=True)
	st.text("")
	c1,c2=st.columns(2)
	
	with c1:
		data = st.text_area("", "Several unit tests fail when upgrading to version 1.3 of ""Commons RNG"": [ERROR] Failures: [ERROR]   LogitTest.testDerivativesWithInverseFunction:195 maxOrder = 2 expected:<0.0> but was:<1.0658141036401503E-14> [ERROR]   EnumeratedIntegerDistributionTest.testMath1533:196 [ERROR]   EnumeratedIntegerDistributionTest.testSample:174 expected:<7.84> but was:<7.857073891264003> [ERROR]   MiniBatchKMeansClustererTest.testCompareToKMeans:86 Different score ratio 46.645378%!, diff points ratio: 34.716981% [ERROR]   CalinskiHarabaszTest.test_compare_to_skLearn:102 expected:<597.7763150683217> but was:<559.2829020672648> [ERROR]   MultiStartMultivariateOptimizerTest.testCircleFitting:76 expected:<69.9597> but was:<69.96228624385736> [ERROR]   MultiStartMultivariateOptimizerTest.testRosenbrock:114 numEval=873 [ERROR]   GaussianRandomGeneratorTest.testMeanAndStandardDeviation:37 expected:<1.0> but was:<0.9715310171501561> [ERROR]   NaturalRankingTest.testNaNsFixedTiesRandom:227 Array comparison failure",height=250) 
	
		
		if st.button("Run",key="1"):
			obj = MEFinder()
			sample_info = {}
			output = -1
			remove_status = True
			flag=[]
			for rule_no in range(12):
        			flag.append(obj.apply(sample_info, me_rules, data, rule_no, remove_status))
			if(sum(flag)>0):
				st.success("ME Found")
				output='1'
				try:
				
					final_output=pd.DataFrame(sample_info).T

			
					st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
					ss=pd.DataFrame(sample_info)
					st.dataframe(ss)
				except:
					st.success("File display unavailable")
			else:
      				st.error("ME not Found")
      				output='0'	
				
	
	with c2:
		data = st.text_area("", "java.lang.StackOverflowError is thrown in: double x = -10_000; double ans1 = Gamma.digamma(x);  // stack overflow double ans2 = Gamma.trigamma(x); // stack overflow It would be nice if the methods returned NaN / Infinity, rather than abort calculations.",height=250) 
	
		
		if st.button("Run",key="2"):
			obj = MEFinder()
			sample_info = {}
			output = -1
			remove_status = True
			flag=[]
			for rule_no in range(12):
        			flag.append(obj.apply(sample_info, me_rules, data, rule_no, remove_status))
			if(sum(flag)>0):
				st.success("ME Found")
				output='1'
				try:
				
					final_output=pd.DataFrame(sample_info).T

			
					st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
					ss=pd.DataFrame(sample_info)
					st.dataframe(ss)
				except:
					st.success("File display unavailable")
			else:
      				st.error("ME not Found")
      				output='0'	
	
	st.text("")
	st.markdown("<h2 style='text-align: center; border-style: ridge; font-family:serif; font-size:20px;font-weight:bold;'> TRY IT YOURSELF </h2>", unsafe_allow_html=True)
	st.text("")
	data = st.text_area("Enter text to check for ME", "",height=250) 
	
		
	if st.button("Run",key="3"):
		obj = MEFinder()
		sample_info = {}
		output = -1
		remove_status = True
		flag=[]
		for rule_no in range(12):
        		flag.append(obj.apply(sample_info, me_rules, data, rule_no, remove_status))
		if(sum(flag)>0):
			st.success("ME Found")
			output='1'
			try:
				
				final_output=pd.DataFrame(sample_info).T

			
				st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
				ss=pd.DataFrame(sample_info)
				st.dataframe(ss)
			except:
				st.success("File display unavailable")
		else:
      			st.error("ME not Found")
      			output='0'	
		


		
main()
