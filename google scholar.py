#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH='./chromedriver'
driver = webdriver.Chrome(PATH)

#open homepage
driver.get("https://scholar.google.com/")
print(driver.title)


# In[2]:


#enter search box
search_box = driver.find_element_by_css_selector('input#gs_hdr_tsi.gs_in_txt.gs_in_ac')
search_box.send_keys("Thammasat University",Keys.ENTER)


# In[3]:


#click Thammasat University
driver.implicitly_wait(3)
driver.find_element_by_css_selector('div.gs_ob_inst_r')    .find_element_by_css_selector('a').click()


# In[4]:


#create dataframe
import pandas as pd
df = pd.DataFrame(
    {
        'user_ID' : [],
        'name' : [],
        'affiliation' : []
    })


# In[5]:


#for every author, get detail and save to df
while 1:
    
    for i in driver.find_elements(By.CSS_SELECTOR,'div.gs_ai_t'):
        author = i.find_element_by_css_selector('a')
        aff = i.find_element_by_css_selector('div.gs_ai_aff')
        print(
            author.get_attribute('href').split('=')[-1],  
            author.text,
            aff.text
        )
    
        #append to df
        df = df.append(
            {
                'user_ID' : author.get_attribute('href').split('=')[-1],
                'name' : author.text,
                'affiliation' : aff.text
            }
            ,ignore_index=True
        )
    
    driver.implicitly_wait(3)
    
    #click next page
    b = driver.find_element_by_css_selector('#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
    b.click()
            


# In[6]:


#show df
df


# In[7]:


#store df in excel
writer = pd.ExcelWriter('authors.xlsx')
df.to_excel(writer)
writer.save()

#store to csv
df.to_csv('authors.csv')


# In[8]:


#create dataframe
paper = pd.DataFrame(columns=['title','authors','publication_date','description','cite_by'])


# In[9]:


#for every paper, get detail and save to df
PATH='./chromedriver'
driver = webdriver.Chrome(PATH)
import time 

row = 0
re = 0
for usr_id in df['user_ID']:
    driver.get('https://scholar.google.com/citations?hlen&user='+usr_id)

    a=driver.find_elements_by_class_name('gs_btnPD')
    while a[0].is_enabled()==True:
        driver.find_element_by_class_name('gs_btnPD').click()
        time.sleep(3)
    link = driver.find_elements_by_class_name('gsc_a_at')
    link = [i.get_attribute('data-href') for i in link]
    print(len(link))

    for url in link:
        driver.get('https://scholar.google.com/'+url)
        try :
            
            table = driver.find_element_by_id('gsc_vcd_table')
            b = table.find_elements_by_class_name('gs_scl')
            title =''
            Au = ''
            PD = ''
            Des = ''
            cited = ''
            for i in b:
                title = driver.find_elements_by_class_name('gsc_vcd_title_link')[0].text
                if i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Authors':
                    Au = i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Publication date':
                    PD =i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Description':
                    Des =i.find_elements_by_class_name('gsc_vcd_value')[0].text
                elif i.find_elements_by_class_name('gsc_vcd_field')[0].text == 'Total citations':
                    cited =i.find_elements_by_css_selector('a')[0].text.replace('Cited by ','')

            paper.loc[row]=[title,Au,PD,Des,cited]
            row += 1
        except :
            pass
        
        print('people pass',re)
        print('no.',len(paper))
        time.sleep(2)
    re += 1


# In[10]:


#show df
paper


# In[11]:


paper.to_csv('papers.csv')

