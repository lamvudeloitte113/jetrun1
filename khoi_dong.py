import streamlit as st
import pandas as pd
import numpy as np
import os.path
# import datetime
# from datetime import datetime as dt


from JET_request import JET_form
from JET_run import JET_run


def read_input(file) :
	if ('xlsx' in file.name) :
		return pd.read_excel(file)
	elif("csv" in file.name) :
		return pd.read_csv(file)

st.title("JET TEST")

menu = ['Completeness','JET running', 'Visualization']

# choice = st.sidebar.selectbox('Menu',menu)

# st.subheader(choice)


GL = None
TB = None
JET_form_ins = None

# if (choice == 'Import Data and Completeness') :

st.subheader("Import Data")
GL_file = st.file_uploader("Import GL" , type = [".csv",".xlsx"])
TB_file = st.file_uploader("Import TB" , type = [".csv",".xlsx"])
Request_form_file = st.file_uploader("Import Request form" , type = [".xlsx"])


if (GL_file != None) :
	GL = read_input(GL_file)
if (TB_file != None) :
	TB = read_input(TB_file)
if (Request_form_file != None) :
	JET_form_ins = JET_form(Request_form_file)
	JET_form_ins.get_file()
	dict_parameters = JET_form_ins.test_parameters_table_run()
	overall_info = JET_form_ins.extract_overall_info()
	df_jet_request_parameter = JET_form_ins.df_jet_request_parameter

if ( (GL_file != None) & (TB_file != None) ):
	try :
		JET_run = JET_run(GL,TB,dict_parameters,df_jet_request_parameter)
	except :
		pass


st.write("Preview GL")
if ( (GL_file != None) ) :
	st.dataframe(GL.head(5))

st.write("Preview TB")
if ((TB_file != None) ) :
	st.dataframe(TB.head(5))

st.write("Overall information")
if ((Request_form_file != None) ) :
 	st.dataframe(overall_info)


st.write("Requested Tests ")



# if (choice == 'Completeness') :

st.write("Completeness table")
if (JET_run!= None) :
	try :
		st.dataframe(JET_run.completeness())
	except :
		pass



# elif (choice ==  'JET running'):
st.write("Run JET")
if (( (GL  is None) ==False ) & ( (TB is  None) == False)):
	try :
		for i in JET_form_ins.dict_parameters.keys():
			st.write("Test " , i)
			st.dataframe(JET_run.call_func(i))
		st.dataframe(JET_run.summary_table_show())

	except :
		pass



# 	st.write("Preview")






















