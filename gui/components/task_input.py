import streamlit as st

class TaskInputComponent:
    @staticmethod
    def render(controller, key: str = "task_input"):
        st.subheader("Task Input")

        with st.form(key=key, clear_on_submit=True):
            task_description = st.text_area(
                "Describe your task",
                placeholder="e.g., Build a tic tac toe game with React",
                height=100,
            )

            project_name = st.text_input(
                "Project Name",
                value="default",
                placeholder="my-project",
            )

            submitted = st.form_submit_button("Submit Task", use_container_width=True)

            if submitted and task_description:
                with st.spinner("Executing task with AI team..."):
                    result = controller.execute_task(task_description, project_name)

                if result["status"] == "success":
                    st.success("Task completed successfully!")
                else:
                    st.error(f"Task failed: {result.get('error', 'Unknown error')}")

                st.rerun()

        return task_description, project_name