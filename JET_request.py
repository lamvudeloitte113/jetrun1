import pandas as pd 
import numpy as np

class JET_form:
    def __init__(self,filename):
        self.filename = filename
        self.df_overall_info = pd.DataFrame()
        self.df_jet_request_parameter = pd.DataFrame()
        self.df_jet_support_sheet =pd.DataFrame() 
        self.dict_parameters = {}
        
# Convert sheets of excel file to DataFrames
    def get_file(self):
        link_jet_request = self.filename
        self.df_overall_info = pd.read_excel(link_jet_request,sheet_name='1. Overall Info')
        self.df_jet_request_parameter = pd.read_excel(link_jet_request,sheet_name='2. Parameters' ,header = 1)
        self.df_jet_support_sheet = pd.read_excel(link_jet_request,sheet_name='3. Support Sheet' ,header = 1)
        self.df_jet_headermapping= pd.read_excel(link_jet_request,sheet_name='Header_Mapping' ,header = 1)
        
        #standardize some datatypes :
        self.df_jet_request_parameter['Test No.'] = self.df_jet_request_parameter['Test No.'].astype('str')
        
        
# Extract infomation of Overall Info sheet :
    def extract_overall_info(self):
        df_overall =  self.df_overall_info.iloc[:9][['CLIENT INFORMATION','Unnamed: 2']].rename(columns = {'CLIENT INFORMATION' : 'CLIENT','Unnamed: 2':'INFORMATION'})
        return df_overall
    
# Extract tests to run
    def extract_test_to_run(self):
        list_test = list(self.df_jet_request_parameter[self.df_jet_request_parameter['To run? (mandatory)'] =='Yes']['Test No.'])
        return list_test
    
# Extract paramters 
    def extract_1a_para (self): 
        list_1a_test_para = list(self.df_jet_support_sheet.iloc[3:,1].dropna())
        return list_1a_test_para

    def extract_1b_para (self): 
        list_1b_test_para = list(self.df_jet_support_sheet.iloc[3:,5].dropna())
        return list_1b_test_para

    def extract_2_para (self): 
        freq_2_para = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '2']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return freq_2_para

    def extract_3_para (self): 
        AP = list(self.df_jet_support_sheet['Test No.3'][3:].dropna())
        AS = list(self.df_jet_support_sheet['Unnamed: 10'][3:].dropna())

        BP = list(self.df_jet_support_sheet['Unnamed: 12'][3:].dropna())
        BS = list(self.df_jet_support_sheet['Unnamed: 13'][3:].dropna())

        CP = list(self.df_jet_support_sheet['Unnamed: 15'][3:].dropna())
        CS = list(self.df_jet_support_sheet['Unnamed: 16'][3:].dropna())

        DP = list(self.df_jet_support_sheet['Unnamed: 18'][3:].dropna())
        DS = list(self.df_jet_support_sheet['Unnamed: 19'][3:].dropna())
        return AP,AS,BP,BS,CP,CS,DP,DS

    def extract_4_para (self): 
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '4']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return number

    def extract_5_para (self) :
        len_of_description = self.df_jet_support_sheet['Test No.5'][3]
        how_many_days = self.df_jet_support_sheet['Unnamed: 24'][3]
        the_closing_date = self.df_jet_support_sheet['Unnamed: 25'][3]

        return len_of_description,how_many_days,the_closing_date


    def extract_6_para (self) :
        list_para = list(self.df_jet_support_sheet['Test No.6'][3:].dropna())
        saturday = self.df_jet_support_sheet['Unnamed: 32'][3]
        sunday = self.df_jet_support_sheet['Unnamed: 32'][4]
        return list_para , saturday, sunday


    def extract_7_para (self) :
        list_para = list(self.df_jet_support_sheet['Test No.7'][3:].dropna())
        return list_para

    def extract_8_para (self): 
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '8']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)

    def extract_9_para (self):
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '9']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)

    def extract_10_para (self):
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '10']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)

    def extract_11a_para (self):
        date = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '11a']['Date\n(dd/mm/yyyy)'].iloc[0]
        return date

    def extract_11b_para (self):
        date = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '11b']['Date\n(dd/mm/yyyy)'].iloc[0]
        return date

    def extract_12_para (self):
        list_para = list(self.df_jet_support_sheet['Test No.12'][3:].dropna())
        return list_para
    
    def extract_13_para (self):
        threshold = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '13']['Threshold'].iloc[0]
        return threshold
    
    def extract_14_para (self):
        threshold = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '14']['Threshold'].iloc[0]
        number_of_days = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '14']['No_of_days'].iloc[0]
        date = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '14']['Date\n(dd/mm/yyyy)'].iloc[0]
        return date,number_of_days,threshold
    
    def extract_15_para (self):
        threshold = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '15']['Threshold'].iloc[0]
        number_of_days = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '15']['No_of_days'].iloc[0]
        date = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == '15']['Date\n(dd/mm/yyyy)'].iloc[0]
        return date,number_of_days,threshold

    def extract_a1_para (self):
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == 'A1']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)

    def extract_a4_para (self):
        list_para = list(self.df_jet_support_sheet['Test No.A4'][3:].dropna())
        return list_para

    def extract_a5_para (self):
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == 'A5']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)

    def extract_a6_para (self):
        number = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == 'A6']['Frequency/\nNo_of_digits/\nNo_of_characters'].iloc[0]
        return int(number)
    
    def extract_a7_para (self):
        threshold = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == 'A7']['Threshold'].iloc[0]
        return threshold

    def extract_a8_para (self):
        list_para = list(self.df_jet_support_sheet['Test No.A8'][3:].dropna())
        threshold = self.df_jet_request_parameter[self.df_jet_request_parameter['Test No.'] == 'A8']['Threshold'].iloc[0]
        return threshold,list_para

# class JET_results_display(JET_form) :

    def call_func(self,test):
        dispatcher = {
            '1a' :self.extract_1a_para(), # list of accounts
            '1b' :self.extract_1b_para(), # list of accounts
            '2'  :self.extract_2_para(),  # frequency
            '3'  :self.extract_3_para(),  # list of list of accounts
            '4'  :self.extract_4_para(),  # number of entries
            '5'  :self.extract_5_para(),  # number of character ,before x days , closing date 
            '6'  :self.extract_6_para(),  # list of non-business day , saturday included ? , sunday included ? 
            '7'  :self.extract_7_para(),  # list of key words
            '8'  :self.extract_8_para(),  # number of consecutiveness
            '9'  :self.extract_9_para(),  # number of consecutiveness
            '10' :self.extract_10_para(), # top x of number of lines
            '11a':self.extract_11a_para(),#
            '11b':self.extract_11b_para(),
            '12' :self.extract_12_para(),
            '13' :self.extract_13_para(),
            '14' :self.extract_14_para(),
            '15' :self.extract_15_para(),
            'A1' :self.extract_a1_para(),
            'A4' :self.extract_a4_para(),
            'A5' :self.extract_a5_para(),
            'A6' :self.extract_a6_para(),
            'A7' :self.extract_a7_para(),
            'A8' :self.extract_a8_para()    
        }
        return dispatcher[test]
    
    def test_parameters_table_run(self):
        
        list_test_run = self.extract_test_to_run()
        self.dict_parameters = {}
        for i in list_test_run :
            try: 
                self.dict_parameters[i] = self.call_func(i)
            except :
                 self.dict_parameters[i] = ''
        return self.dict_parameters  
    
    
    def test_parameters_table_show(self):
#         table_parameters = pd.DataFrame(self.dict_parameters)
#         return table_parameters
        pass 