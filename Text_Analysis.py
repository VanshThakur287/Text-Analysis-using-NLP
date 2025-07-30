#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from nltk.tokenize import sent_tokenize, word_tokenize
import string
import re


# In[2]:


file_name=input('\n ENTER THE FILE NAME WITH .xlsx format \n')
TA_file=pd.read_excel(file_name)


# In[3]:


TA_file


# In[4]:


TA_file.columns


# In[5]:


columns=["POSITIVE SCORE","NEGATIVE SCORE","POLARITY SCORE","SUBJECTIVITY SCORE","AVG SENTENCE LENGTH","PERCENTAGE OF COMPLEX WORDS","FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE","COMPLEX WORD COUNT","WORD COUNT","SYLLABLE PER WORD","PERSONAL PRONOUNS","AVG WORD LENGTH"]


# In[6]:


TA_file=TA_file.reindex(columns = TA_file.columns.tolist() + columns)


# In[7]:


TA_file


# In[8]:


TA_file.columns


# In[9]:


TA_file.info()


# In[10]:


TA_file.describe()


# In[11]:


TA_file["URL_ID"].unique


# In[12]:


TA_file.set_index("URL_ID",inplace=True)


# In[13]:


TA_file


# In[14]:


for i in TA_file.index:
    print(i)


# In[15]:


TA_file.index


# In[16]:


TA_file


# In[17]:


#TA_file.loc["bctech2011"][1]   #first row then column name


# In[ ]:





# # Seperating useful data from webpage

# In[36]:


def scraping_textfile(TA_file):
    URL=TA_file['URL']
    ID=TA_file.index
    f_path=input('\n ENTER THE FILE PATH SEPERATED WITH \\\ WHERE YOU WANT TO STORE THE TEXT FILES \n')
    a=0
    for link in URL:
        print('\n URL :',link,'\n')
        page=requests.get(link)
        soup=BeautifulSoup(page.text, 'html')
        content=soup.find('div', class_ = 'td-ss-main-content').text.strip()
        name=ID[a]
        file_path=os.path.join(f_path,f'{name}.txt')  #'C:\\Users\\Vansh\Desktop\\projects\\Blackcoffer\\text files'
        file=open(file_path,'w',encoding='utf-8')
        file.write(content)
        file.close()
        a=a+1
        print(f'\nFile {name} created successfully \n')


# In[21]:


#this method consumes time so, if there is another method to impore it, please let me know
scraping_textfile(TA_file)


# # Cleaning the data in file

# ## Getting stopwords from the file

# In[22]:


sw_path1='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_Auditor.txt'
sw_path2='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_Currencies.txt'
sw_path3='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_DatesandNumbers.txt'
sw_path4='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_Generic.txt'
sw_path5='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_GenericLong.txt'
sw_path6='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_Geographic.txt'
sw_path7='C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\StopWords\\StopWords_Names.txt'


# In[23]:


sw1=open(sw_path1,'r')
sw2=open(sw_path2,'r')
sw3=open(sw_path3,'r')
sw4=open(sw_path4,'r')
sw5=open(sw_path5,'r')
sw6=open(sw_path6,'r')
sw7=open(sw_path7,'r')
sw1=sw1.read()
sw2=sw2.read()
sw3=sw3.read()
sw4=sw4.read()
sw5=sw5.read()
sw6=sw6.read()
sw7=sw7.read()


# In[24]:


sw_lst=[sw1,sw2,sw3,sw4,sw5,sw6,sw7]
for w in sw_lst:
    print(w)


# In[37]:


#checking the working of the function
F_name=TA_file.index
F_name_len=len(F_name)
print(F_name_len)
file1_path=f'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\text files\\{F_name}.txt'
for file in F_name:
    file1_path=f'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\text files\\{file}.txt'
    file1=open(file1_path,'r',encoding='utf-8')
    file1=file1.read()
    print(f"File {file} Fetched successfully")


# In[26]:


TA_file.columns


# # EXTRACTING DERIVED VARIABLES

# In[38]:


def ext_der_var(sw,TA_file):
    f_name=TA_file.index
    for name in f_name:
        file_path=f'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\text files\\{name}.txt'
        file=open(file_path,'r',encoding='utf-8')
        file=file.read()
        file_token=word_tokenize(file)
        print("\n Words tokenized for file: ",name,"\n")
        #CLEANING THE WORDS 
        for word in file_token:
            if word in sw[0]:
                file_token.remove(word)
            elif word in sw[1]:
                file_token.remove(word)
            elif word not in sw[2]:
                file_token.remove(word)
            elif word not in sw[3]:
                file_token.remove(word)
            elif word not in sw[4]:
                file_token.remove(word)
            elif word not in sw[5]:
                file_token.remove(word)
            elif word not in sw[6]:
                file_token.remove(word)
        cfile_token=file_token
        c_words_totl=len(cfile_token)
        print("\n Words Cleaned For File: ",name,"\n")
        #fetching negative and positive words file
        nw_path= 'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\MasterDictionary\\negative-words.txt'
        pw_path= 'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\MasterDictionary\\positive-words.txt'
        nw_file=open(nw_path,'r')
        pw_file=open(pw_path,'r')
        nw=nw_file.read()
        pw=pw_file.read()
        #calculating negative score and positive score for the file
        pos_score=0
        neg_score=0
        for word in cfile_token:
            if word in pw:
                pos_score+=1
            elif word in nw:
                neg_score-=1
        neg_score=neg_score*(-1)
        #1st Variable POSITIVE SCORE
        TA_file.loc[name,'POSITIVE SCORE']=pos_score
        print(f"\n POSITIVE SCORE inserted into file: {name}\n")
            #2nd Variable NEGATIVE SCORE
        TA_file.loc[name,'NEGATIVE SCORE']=neg_score
        print(f'\n NEGATIVE SCORE inserted into file: {name}\n')
            #3RD variable POLARITY SCORE
        pol_score=(pos_score-neg_score)/((pos_score+neg_score)+0.000001)
        pol_score=round(pol_score,3)
        print(f"\n POLARITY SCORE inserted into file: {name}\n")
        TA_file.loc[name,'POLARITY SCORE']=pol_score
        #4th Variable SUBJECTIVITY SCORE 
        sub_score=(pos_score+neg_score)/((c_words_totl)+0.000001)
        sub_score=round(sub_score,3)
        TA_file.loc[name,'SUBJECTIVITY SCORE']=sub_score
        print(f'\n SUBJECTIVE SCORE inserted into file: {name}\n')
        #10TH VARIABLE: WORD COUNT
        punc=string.punctuation
        for w in cfile_token:
            if w in punc:
                cfile_token.remove(w)
        cwords_count=len(cfile_token)
        TA_file.loc[name,'WORD COUNT']=cwords_count
        print(f'\n WORD COUNT inserted into file: {name}\n')
        


# ### regerence for an error caused of chaining
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

# In[28]:


ext_der_var(sw_lst,TA_file)


# In[29]:


TA_file


# #  Analysis of readibility
# ## 5. Average Sentence Length
# ## 6. Percentage of Complex words
# ## 7. Fog Index 
# ## 8. Average number of words per sentence
# ## 9. Complex Word Count
# ## Tokenizing sentences

# In[30]:


TA_file.columns


# In[39]:


def analysis_readability(TA_file):
    f_name=TA_file.index
    vowels=['a','e','i','o','u']
    Per_pro=['I','we','my','ours','us']
    for name in f_name:
        file_path=f'C:\\Users\\Vansh\\Desktop\\projects\\Blackcoffer\\text files\\{name}.txt'
        file=open(file_path,'r',encoding='utf-8')
        file=file.read()
        f_sentt=sent_tokenize(file)
        f_sentt_len=len(f_sentt)
        f_wordt=word_tokenize(file)
        f_wordt_len=len(f_wordt)
        print("\n Words tokenized for file: ",name,"\n")
        print("\n Sentences tokenized for file: ",name,"\n")
        #5th Variable: AVERAGE SENTENCE LENGTH
        avg_sent_len=f_wordt_len/f_sentt_len
        avg_sent_len=round(avg_sent_len,3)
        TA_file.loc[name,'AVG SENTENCE LENGTH']=avg_sent_len
        print(f'\n AVG SENTENCE LENGTH inserted into file: {name} \n')
        word_comp=[]
        for word in f_wordt:
            vowel_count=0
            for a in word:
                if a in vowels:
                    vowel_count+=1
            if vowel_count>=2:         
                word_comp.append(word)
        #6TH VARIABLE: PERCENTAGE OF COMPLEX WORDS
        word_comp_len=len(word_comp)
        per_word_comp=word_comp_len/f_wordt_len
        per_word_comp=round(per_word_comp,3)
        TA_file.loc[name,'PERCENTAGE OF COMPLEX WORDS']=per_word_comp
        print(f'\n PERCENTAGE OF COMPLEX WORDS inserted into file: {name} \n')
        #7TH VARIABLE: FOG INDEX
        fog_idx=0.4*(avg_sent_len+per_word_comp)
        fog_idx=round(fog_idx,3)
        TA_file.loc[name,'FOG INDEX']=fog_idx
        print(f'\n FOG INDEX inserted into file: {name} \n')
        #8TH VARIABLE: AVG NUMBER OF WORDS PER SENTENCE
        avg_word_per_sent=f_wordt_len/f_sentt_len
        avg_word_per_sent=round(avg_word_per_sent,3)
        TA_file.loc[name,'AVG NUMBER OF WORDS PER SENTENCE']=avg_word_per_sent
        print(f'\n AVG NUMBER OF WORDS PER SENTENCE inserted into file: {name} \n')
        #9TH VARIABLE: COMPLEX WORD COUNT
        TA_file.loc[name,'COMPLEX WORD COUNT']=word_comp_len
        print(f'\n COMPLEX WORD COUNT inserted into file: {name} \n')
        #11TH VARIABLE: SYLLABLE PER WORD
        vcpw=[]
        for word in f_wordt:
            vowel_count=0
            for a in word:
                if word[-2:]=='es':
                    word=word[:-2]
                if a in vowels:
                    vowel_count+=1

            if vowel_count>=2:
                if word not in word_comp:             #if repetition is not allowed then we use this command and fix indentation
                    word_comp.append(word)
                    vcpw.append(vowel_count)
        VCPW=sum(vcpw)
        TA_file.loc[name,'SYLLABLE PER WORD']=VCPW  
        print(f'\n SYLLABLE PER WORD inserted into file: {name} \n')
        #12TH VARIABLE: PERSONAL PRONOUNS
        pattern = r"\b(" + "|".join(Per_pro) + r")\b"
        for w in f_wordt:
            matches=re.findall(pattern,str(f_wordt))
            PP_count=len(matches)
        TA_file.loc[name,'PERSONAL PRONOUNS']=PP_count
        print(f'\n PERSONAL PRONOUNS inserted into file: {name} \n')
        ##13TH VARIABLE: AVG WORD LENGTH
        sum_wlen=0
        for w in f_wordt:
            wl=len(w)
            sum_wlen+=wl
        avg_word_len=sum_wlen/len(f_wordt)
        avg_word_len=round(avg_word_len)
        TA_file.loc[name,'AVG WORD LENGTH']=avg_word_len
        print(f'\n AVG WORD LENGTH inserted into file: {name} \n')


# In[32]:


analysis_readability(TA_file)


# In[33]:


TA_file


# In[40]:


TA_file.to_excel("Final output data.xlsx")
print('\n SOLUTION GENERATED AND EXPORTED AS EXCEL FILE\n')
print('\n THANKYOU FOR USING THE PROGRAM \n')


# In[ ]:




