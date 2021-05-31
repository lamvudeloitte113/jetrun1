import pandas as pd
import numpy as np
import os.path
import datetime
from datetime import datetime as dt
# from .JET_request import JET_form
    
class JET_run:
    
    def __init__(self,GL,TB,dict_parameters,df_jet_request_parameter):
#        self.JET_form = JET_form() 
        self.GL = GL
        self.TB = TB
        self.dict_parameters = dict_parameters
        self.dict_summary = {}
        self.df_jet_request_parameter = df_jet_request_parameter

    # def get_tables(self):
        
    #     if ('xlsx' in os.path.basename(GL_path)):
    #         self.GL = GL
    #     elif ('csv' in os.path.basename(GL_path)) :
    #         self.GL = pd.read_csv(GL_path,sep = "|")
    #     else :
    #         print("File format not identified")
            
    #     self.TB = pd.read_excel(TB_path)
        
        
    def get_summary (self,df) :
        Number_of_JE = len(df['JENumber'].unique())
        Number_of_rows = df.shape[0]
        
        return Number_of_JE,Number_of_rows
        
    def completeness(self):   
        def debits_column (amount):
            if amount >= 0 :
                return amount
            else : 
                return 0
        def credits_column (amount):
            if amount < 0 :
                return amount
            else : 
                return 0
            
        def reconcilation_status(diff):
            if diff == 0 :
                return 'Reconciled'
            else :
                return 'Non-reconciled'
            
        df_GL_2 = self.GL[['JENumber','AccountNumber','Amount']]
        df_GL_2['Debits']  = df_GL_2['Amount'].apply(lambda x : debits_column(x))
        df_GL_2['Credits']  = df_GL_2['Amount'].apply(lambda x : credits_column(x))
                          
        df_GL_3 = df_GL_2.groupby(by='AccountNumber').agg({
            'JENumber' : 'count',
            'Amount' : 'sum',
            'Debits' : 'sum',
            'Credits' : 'sum'
        }).reset_index().rename(columns = {
            'JENumber' : 'NumberOfLines',
            'Amount' : 'Movement_GL',
            'Debits' : 'TotalDebits_GL',
            'Credits' : 'TotalCredits_GL'
        })
                          
        df_TB_completeness = pd.merge(df_GL_3,self.TB,on = 'AccountNumber', how = 'left')
        df_TB_completeness['Movement_TB'] = df_TB_completeness['ClosingBalance'] - df_TB_completeness['OpeningBalance']
        df_TB_completeness['Difference'] = df_TB_completeness['Movement_GL'] - df_TB_completeness['Movement_TB']
        df_TB_completeness['Status'] = df_TB_completeness['Difference'].apply(lambda x : reconcilation_status(x))
        df_TB_completeness.AccountName.fillna('### Account NOT in Trial Balance ###',inplace = True)
        df_TB_completeness = df_TB_completeness[['AccountNumber','AccountName','NumberOfLines','Category','OpeningBalance',
                                        'ClosingBalance','Movement_TB','TotalDebits_GL','TotalCredits_GL','Movement_GL','Difference','Status']]
                          
        return df_TB_completeness
    
    
    
    def update_total_JE_amount(self):
        self.GL['TotalJEAmount']=self.GL.groupby(by = 'JENumber').Amount.transform(np.mean)
        self.GL = pd.merge (self.GL,self.TB[['AccountNumber','Category']],on = 'AccountNumber',how = 'left')
    
    
    def test_1a(self,list_key_words_1a = None) :
        
        if list_key_words_1a is None :
            list_key_words_1a = self.dict_parameters['1a']
            
        list_key_words_1a =  list(map(lambda x : x.upper(),list_key_words_1a))
        list_account = self.TB[self.TB['AccountName'].str.upper().str.contains('|'.join(list_key_words_1a))]['AccountNumber']
        df_1a = self.GL[self.GL['AccountNumber'].isin(list_account)]
        df_1a['Test'] = '1A'
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df1a)
        self.add_to_dict_summary(TestNo = '1a' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_1a
    
    def test_1b(self,list_account=None):
        
        if list_account is None:
            list_account = self.dict_parameters['1b']
        
        df_1b = self.GL[self.GL['AccountNumber'].isin(list_account)]
        df_1b['Test'] = '1B'
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_1b)
        self.add_to_dict_summary(TestNo = '1b' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_1b
    
    def test_2(self,freq  = None ) :
        if freq is None :
            freq  = self.dict_parameters['2']
        
        df_groupby = self.GL[['AccountNumber','JENumber']].groupby("AccountNumber").count().reset_index()
        list_account = list (df_groupby[df_groupby['JENumber'] <= freq]['AccountNumber'])
        df_2 = self.GL[self.GL['AccountNumber'].isin(list_account)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_2)
        self.add_to_dict_summary(TestNo = '2' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_2
    
    # def test_3
    def test_4(self,freq = None) :
        if freq is None :
            freq = self.dict_parameters['4']
            
        df_groupby = self.GL[['PreparerName','JENumber']].groupby(by='PreparerName').count().reset_index()
        list_preparername = list (df_groupby[df_groupby['JENumber'] <= freq]['PreparerName'])
        df_4 = self.GL[self.GL['PreparerName'].isin(list_preparername)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_4)
        self.add_to_dict_summary(TestNo = '4' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_4
    
    def test_5(self,len_of_description = None , how_many_days = None , the_closing_date = None) :
        
        if ( (len_of_description is None) | (how_many_days is None) | (the_closing_date is None) ) :
            len_of_description = self.dict_parameters['5'][0] 
            how_many_days = self.dict_parameters['5'][1]
            the_closing_date = self.dict_parameters['5'][2]

        df_5 = self.GL[(self.GL['Description'].str.len() < len_of_description) &
                    (self.GL['EffectiveDate'] > (the_closing_date - datetime.timedelta (days = how_many_days )))]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_5)
        self.add_to_dict_summary(TestNo = '5' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_5
        
    def test_6(self,list_para = None , saturday = None, sunday = None ):
        if ( (list_para is None) | (saturday is None) | (sunday is None) ):
            list_para = self.dict_parameters['6'][0]
            saturday = self.dict_parameters['6'][1]
            sunday = self.dict_parameters['6'][2]
        list_sat_sun = []
        if saturday == 'Yes':
            list_sat_sun.append(5)

        if sunday == 'Yes':
            list_sat_sun.append(6)
            
        df_6 = self.GL[
                        self.GL['PostingDate'].dt.weekday.isin(list_sat_sun) |
                        self.GL['PostingDate'].isin(list_para)
                    ] 
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_6)
        self.add_to_dict_summary(TestNo = '6' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_6
        
    def test_7(self,list_key_words = None):
        if (list_key_words is None):
            list_key_words = self.dict_parameters['7']
        list_key_words = list (map(lambda x: x.upper() ,list_key_words))
        df_7 = self.GL [self.GL['Description'].str.upper().str.contains('|'.join(list_key_words))]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_7)
        self.add_to_dict_summary(TestNo = '7' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_7
    
    def test_8(self,freq = None):
        if (freq is None) :
            freq = self.dict_parameters['8']
        list_number = []
        for i in range(1,10):
            list_number.append(str(i)*freq)
        df_8 = self.GL[self.GL['Amount'].astype(str).str.contains("|".join(list_number))]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_8)
        self.add_to_dict_summary(TestNo = '8' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_8
    
    def test_9(self,freq = None):
        if (freq is None):
            freq = self.dict_parameters['9']
        df_9  = self.GL[self.GL['Amount'].astype(str).str.contains('0'*freq)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_9)
        self.add_to_dict_summary(TestNo = '9' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_9
        
    def test_10(self,number = None ):
        if (number is None):
            number = self.dict_parameters['10']
        list_JENumber = list(self.GL[['JENumber','PostingDate']].groupby('JENumber').count().reset_index().sort_values('PostingDate',ascending = False).iloc[0:number]['JENumber'])
        df_10 = self.GL [self.GL['JENumber'].isin(list_JENumber)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_10)
        self.add_to_dict_summary(TestNo = '10' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_10
    
    def test_11a(self,openingdate = None):
        if (openingdate is None):
            openingdate = self.dict_parameters['11a']
        df_11a =  self.GL[self.GL['PostingDate'] < openingdate]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_11a)
        self.add_to_dict_summary(TestNo = '11a' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_11a
    
    def test_11b(self,closing_date= None):
        if (closing_date is None):
            closing_date = self.dict_parameters['11b']
        df_11b =  self.GL[self.GL['PostingDate'] > closing_date]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_11b)
        self.add_to_dict_summary(TestNo = '11b' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_11b
    
    def test_12 (self,list_users = None):
        if (list_users is None):
            list_users = self.dict_parameters['12']
        df_12 = self.GL[self.GL['PreparerName'].isin(list_users)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_12)
        self.add_to_dict_summary(TestNo = '12' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)

        return df_12 
    
    def test_13(self,threshold = None):
        if (threshold is None):
            threshold = self.dict_parameters['13']
        df_groupby = self.GL[self.GL['Category'] == 'Income (Revenue)'][['JENumber','Amount']].groupby('JENumber').sum().reset_index()
        list_JENumber = list (df_groupby [df_groupby['Amount'] > threshold ]['JENumber'])
        df_13 = self.GL[self.GL['JENumber'].isin(list_JENumber)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_13)
        self.add_to_dict_summary(TestNo = '13' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)

        return df_13
        
    def test_14(self,year_end = None,number_of_days = None,threshold = None):
        if ( (year_end is None) | (number_of_days is None) | (threshold is None) | () ):
            year_end = self.dict_parameters['14'][0]
            number_of_days = self.dict_parameters['14'][1]
            threshold = self.dict_parameters['14'][2]
        
        df_groupby = self.GL[
                        (self.GL.Category.isin(['Income (Revenue)','Income (Non-revenue)','Expenses']) )
                        &
                        (self.GL['EffectiveDate'] <  (year_end - datetime.timedelta(days = number_of_days)))
                        ][['JENumber','Amount']].groupby (by = 'JENumber').sum().reset_index()
        list_JENumber = list(df_groupby[df_groupby['Amount'] > threshold]['JENumber'])
        df_14 = self.GL[self.GL['JENumber'].isin(list_JENumber)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_14)
        self.add_to_dict_summary(TestNo = '14' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_14
    
    def test_15(self, year_end = None ,number_of_days = None,threshold = None):
        if ( (year_end is None) | (number_of_days is None) | (threshold is None) | () ):
            year_end = self.dict_parameters['15'][0]
            number_of_days = self.dict_parameters['15'][1]
            threshold = self.dict_parameters['15'][2]
        
        df_groupby = self.GL[
                        (self.GL.Category.isin(['Income (Revenue)','Income (Non-revenue)','Expenses']) )
                        &
                        (self.GL['EffectiveDate'] <  (year_end - datetime.timedelta(days = number_of_days)))
                        ][['JENumber','Amount']].groupby (by = 'JENumber').sum().reset_index()
        list_JENumber = list(df_groupby[df_groupby['Amount'] < -  threshold]['JENumber'])
        df_15 = self.GL[self.GL['JENumber'].isin(list_JENumber)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_15)
        self.add_to_dict_summary(TestNo = '15' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_15
    
    def test_a1(self,freq= None) :
        if ( freq is None) :
            freq = self.dict_parameters['A1']
        df_a1 = self.GL[self.GL['Description'].str.len() <= freq]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a1)
        self.add_to_dict_summary(TestNo = 'A1' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a1
    
    
    def test_a2(self) :
        list_account_TB = list(self.TB['AccountNumber'])
        df_A2 = self.GL[self.GL['AccountNumber'].isin(list_account_TB) == False]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_A2)
        self.add_to_dict_summary(TestNo = 'A2' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_A2
    
    def test_a3(self):
        df_credit = self.GL[self.GL['Amount']<0][['JENumber','Amount']].groupby ('JENumber').sum().reset_index().rename(columns = {'Amount' : 'Credits'})
        df_debit = self.GL[self.GL['Amount']>=0][['JENumber','Amount']].groupby ('JENumber').sum().reset_index().rename(columns = {'Amount' : 'Debits'})
        df_merge = pd.merge(df_credit,df_debit,how = 'outer', on ='JENumber').fillna(0)
        df_merge['Difference'] = df_merge['Debits']  + df_merge['Credits']
        list_JEnumber = list (df_merge[df_merge['Difference'] != 0]['JENumber'])
        df_a3 = self.GL[self.GL['JENumber'].isin(list_JEnumber)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a3)
        self.add_to_dict_summary(TestNo = 'A3' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a3
    
    def test_a4(self,list_users = None):
        if (list_users is None):
            list_users = self.dict_parameters['A4']
        df_a4 = self.GL[self.GL['PreparerName'].isin(list_users) == False]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a4)
        self.add_to_dict_summary(TestNo = 'A4' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a4
    
    def test_a5(self,interval = None):
        if (interval is None):
            interval = self.dict_parameters['A5']
        df_a5 = self.GL[ abs(self.GL['DocumentDate'] - self.GL['EffectiveDate']).dt.days >= interval ]

        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a5)
        self.add_to_dict_summary(TestNo = 'A5' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a5
    
    def test_a6(self,freq = None):
        if (freq is None):
            freq = self.dict_parameters['A6']
        df_groupby = self.GL[['Amount','JENumber']].groupby(by = 'Amount').count().reset_index()
        list_amount = df_groupby[df_groupby['JENumber'] >freq ]['Amount']
        df_a6 = self.GL[self.GL['Amount'].isin(list_amount)]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a6)
        self.add_to_dict_summary(TestNo = 'A6' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a6
            
    def test_a7(self,threshold = None):
        if (threshold is None) :
            threshold = self.dict_parameters['A7']
        df_a7 = self.GL[abs(self.GL['Amount'])>threshold]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a7)
        self.add_to_dict_summary(TestNo = 'A7' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a7
    
    def test_a8(self,threshold = None ,list_para = None):
        if ( (threshold is None) | (list_para is None ) ):
            threshold = self.dict_parameters['A8'][0]
            list_para = self.dict_parameters['A8'][1]
        df_a8 = self.GL[
                self.GL['AccountNumber'].isin(list_para) &
                self.GL['Amount'] >= threshold
             ]
        
        #Update reulst to summary table 
        Number_of_JE , Number_of_rows = self.get_summary(df_a8)
        self.add_to_dict_summary(TestNo = 'A8' , Number_of_JE = Number_of_JE ,Number_of_rows = Number_of_rows)
        
        return df_a8
    
    def call_func(self,test):
        func_name = "self.test_" + test.lower() + "()"
        return eval(func_name)
    
    def get_test_name (self,TestNo):
        TestName = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == TestNo]['Test Name'].iloc[0]
        return TestName
    
    def add_to_dict_summary(self,TestNo = None,Number_of_JE = None ,Number_of_rows = None):
        TestName = self.get_test_name(TestNo)
        list_values = [TestName,Number_of_JE, Number_of_rows]
        element = {TestNo : [TestName,Number_of_JE, Number_of_rows]}
        self.dict_summary[TestNo] = [TestName,Number_of_JE, Number_of_rows]
        
    def summary_table_show(self):
        df_table = pd.DataFrame(self.dict_summary).transpose().reset_index()
        df_table.columns = ['TestNo.','TestName','Number_of_JE_flagged','Number_of_rows_flagged']
        df_table['Time Created'] = str(datetime.date.today())
        
        return df_table