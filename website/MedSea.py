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

st.set_page_config(page_title='MedSea', page_icon=None, layout='wide', initial_sidebar_state='auto')
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
	st.markdown("<h1 style='text-align: center; border-style: groove; background-color:#D22B2B; font-family:times new roman; font-size:25px; background-image: red.jpg;'>MEDSEA <br><br><small>Demonstration shown in the paper</small><br><br> MATHEMATICAL EXPRESSIONS IN SOFTWARE ENGINEERING ARTIFACTS </h1>", unsafe_allow_html=True)
	st.text("")
	st.text("")
	col1,col2=st.columns(2)
	with col1:
		st.markdown( """<a style='display: block; text-align: center; font-family:times new roman; font-size:25px;' href="https://github.com/MathyB/MathyB_Dataset">Code</a> """, unsafe_allow_html=True, )
	
		
	st.text("")
	st.text("")
	
	c1,c2,c3,c4,c5,c6=st.columns(6)
	with c1:
		c1='1'
	with c2:
		c2='2'
	with c3:
		c3='3'
	with c4:
		c4='4'
	with c5:
		c5='5'
	with c6:
		c6='Try'
	
	if st.button('1',key=1):
		data = st.text_area("Enter text to check for ME", "Functionality to be moved to 'Commons RNG' (cf. RNG-140).") 
	
		
		if st.button("Run"):
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

					#final_output.reset_index(inplace=True)
					#final_output.rename(columns={'index': 'Bug_Id'},inplace=True)
					#final_output['Output']=output
					st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
					ss=pd.DataFrame(sample_info)
					st.dataframe(ss)
				except:
					st.success("File display unavailable")
			else:
      				st.error("ME not Found")
      				output='0'	
				
	if st.button('2',key=2):
		data = st.text_area("Enter text to check for ME", "Functionality to be moved to 'Commons RNG' (cf. RNG-140).") 
	
		
		if st.button("Run"):
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

					#final_output.reset_index(inplace=True)
					#final_output.rename(columns={'index': 'Bug_Id'},inplace=True)
					#final_output['Output']=output
					st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
					ss=pd.DataFrame(sample_info)
					st.dataframe(ss)
				except:
					st.success("File display unavailable")
			else:
      				st.error("ME not Found")
      				output='0'	
	
	if st.button('Try',key=6):
		data = st.text_area("Enter text to check for ME", "Functionality to be moved to 'Commons RNG' (cf. RNG-140).") 
	
		
		if st.button("Run"):
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

					#final_output.reset_index(inplace=True)
					#final_output.rename(columns={'index': 'Bug_Id'},inplace=True)
					#final_output['Output']=output
					st.markdown(get_table_download_link(final_output), unsafe_allow_html=True)
					ss=pd.DataFrame(sample_info)
					st.dataframe(ss)
				except:
					st.success("File display unavailable")
			else:
      				st.error("ME not Found")
      				output='0'	
	
		


		
main()
