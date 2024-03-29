import streamlit as st
import pandas as pd 
from db_fxns import * 
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu



import plotly.express as px 
st.set_page_config(page_title='Todo App By Palasha',page_icon=':pencil:',layout='wide')

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App</h1>
    <p style="color:white;text-align:center;">Made with ❤️ by Palasha Pawan, Ujjwal Tiwari & Preeti Sharma</p>
    </div>
    """


def main():
	stc.html(HTML_BANNER)


	with st.sidebar:
		choice = option_menu("Menu", ["Create", "Read", "Update", "Delete"],
                         icons=['check2-square', 'list-task', 'gear', 'trash'],
                         menu_icon="menu-button-wide", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#464e5f"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#D3D3D3"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
	
	create_table()

	if choice == "Create":
		st.subheader("Add Item")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_area("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added {} To Task".format(task))


	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)


	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated {} To {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

	


if __name__ == '__main__':
	main()
