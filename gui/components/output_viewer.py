import streamlit as st

class OutputViewerComponent:
    @staticmethod
    def render(controller):
        st.subheader("Output / Code View")

        result = controller.get_crew_result()

        if result is None:
            st.info("No output yet. Submit a task to see results here.")
            return

        with st.expander("Full Result", expanded=True):
            st.text(result)

        tabs = st.tabs(["Code", "Summary", "Raw JSON"])

        with tabs[0]:
            result_str = str(result)
            if "```" in result_str:
                parts = result_str.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        language = part.split("\n")[0] if "\n" in part else ""
                        code = "\n".join(part.split("\n")[1:]) if language else part
                        if language:
                            st.code(code, language=language.strip())
                        else:
                            st.code(code)
                    else:
                        if part.strip():
                            st.markdown(part)
            else:
                st.text(result_str)

        with tabs[1]:
            if hasattr(result, "pydantic"):
                st.json(result.pydantic())
            elif hasattr(result, "dict"):
                st.json(result.dict())
            else:
                st.text(str(result))

        with tabs[2]:
            import json
            try:
                st.json(json.loads(str(result)))
            except Exception:
                st.text(str(result))