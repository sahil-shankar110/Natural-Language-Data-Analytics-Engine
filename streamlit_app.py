import streamlit as st
from app.file_loader import load_file , load_demo_file
from app.database import read_query
from app.llm import generate_sql
from app.visualizer import generate_chart

# Set page config
st.set_page_config(page_icon="📊", page_title="Natural Language Data Analytics Engine", layout="wide")

# Session state to store data and results
if "data" not in st.session_state:
    st.session_state.data = None

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar For History
with st.sidebar:
    st.header("Query History")
    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            st.markdown(f"**Q{i+1}:** {item['question']}")
            st.markdown(item["explanation"])
            st.markdown("---")
    else:
        st.info("No queries yet. Ask something about your data!")    

# Main Interface
st.title("📊 Natural Language Data Analytics Engine")
st.write("Upload your data and ask questions in plain English")


# File Upload Section
st.subheader("Upload Your File")
supported_type = [".csv", ".xlsx", ".xls", ".json", ".db", ".sqlite", ".sqlite3"]

col1 , col2 = st.columns([3, 2])
with col1:
    uploaded_file = st.file_uploader("Choose a file", type= supported_type,max_upload_size=20, help="Supported formats: CSV, Excel, JSON, SQLite")
    load_uploaded_button = st.button("Load Uploaded File")

with col2:
    st.markdown("**Try Demo Files**")
    demo = st.selectbox("Select a demo file", ["None", "Students Data","Sales Data"])
    load_demo = st.button("Load Demo")


# Load Uploaded File
if load_uploaded_button and uploaded_file:
    with st.spinner("Reading file..."):
        try:
            data = load_file(uploaded_file)
            st.session_state.update(data)
            st.session_state.data = True
            st.session_state.history = []
            st.success(f"✅ Your data is ready!  {data['row_count']} rows · {data['col_count']} columns")
        except Exception as e:
            st.error(f"❌ {str(e)}")

# Load Demo File        
if load_demo and demo != "None":
    demo_files = { "Students Data": "Demo_Files/Student_Data.csv",
                  "Sales Data": "Demo_Files/Sales_Data.csv"}
    with st.spinner("Loading demo file..."):
        try:
                data = load_demo_file(demo_files[demo])
                st.session_state.update(data)
                st.session_state.data = True
                st.session_state.history = []
                st.success(f"✅ Demo data loaded!  {data['row_count']} rows · {data['col_count']} columns")
        except Exception as e:
            st.error(f"❌ could not load demo file: {str(e)}")


# Query Section
if st.session_state.data:

    st.divider()
    st.subheader("💬 Ask anything about your Data")

    # ── Show available columns ──
    st.caption(f"📋 **Available columns:** {', '.join(st.session_state.columns)}")

    # ── Suggested questions ──
    st.markdown("**💡 Try asking:**")
    suggestions = [
        f"Show me the top 5 records",
    f"How many rows are in this data?",
    f"Show me count of each unique value in {st.session_state.columns[0]}"
]

    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, use_container_width=True):
            st.session_state.selected_question = suggestion
            st.rerun()

# Question input        
    question = st.text_input("Type your question here", value=st.session_state.get("selected_question", ""),placeholder="e.g. 'What is the average value of column X?'")
    ask_button = st.button("Ask")

    if ask_button and question:
        with st.spinner("Generating SQL query..."):
            try:
                # Generate SQL query from LLM
                LLM_Result = generate_sql(
                    table_name=st.session_state.table_name,
                    schema=st.session_state.schema,
                    sample_rows= st.session_state.sample_rows,
                    question=question
                )
                sql_query = LLM_Result.get("sql")
                explanation = LLM_Result.get("explanation")
                chart_type = LLM_Result.get("chart_type","none")
                chart_X = LLM_Result.get("chart_x")
                chart_Y = LLM_Result.get("chart_y")
                error = LLM_Result.get("error")
                # Step 2: Handle unanswerable question
                if error or not sql_query:
                    st.warning(f"⚠️ {explanation}")
                else:
                    df_result = read_query(st.session_state.db_path, sql_query)
                    # Make column matching case-insensitive
                    actual_cols = [col.lower() for col in df_result.columns]


                    if chart_X and chart_X.lower() in actual_cols:
                        chart_X = df_result.columns[actual_cols.index(chart_X.lower())]
                    else:
                        chart_X = None

                    if chart_Y and chart_Y.lower() in actual_cols:
                        chart_Y = df_result.columns[actual_cols.index(chart_Y.lower())]
                    else:
                        chart_Y = None
                    # Show chart first
                    fig = generate_chart(df_result, chart_type, chart_X, chart_Y)
                    if fig:
                        st.subheader("📊 Chart")
                        st.plotly_chart(fig, use_container_width=True)

                    # Show Table Result   
                    st.subheader("📋 Data Table")
                    st.dataframe(df_result, use_container_width=True)


                    # Show Explanation
                    st.subheader("🧠 Explanation")
                    st.info(f"**Query Explanation:** {explanation}")

                    # SQL Query (for advanced users)
                    with st.expander("🔍 SQL Query"):
                        st.code(sql_query, language="sql")
                    # Save to history
                    st.session_state.history.append({
                        "question": question,
                        "explanation": explanation,
                        "sql_query" : sql_query,
                        "rows_returned": len(df_result)
                    })    

            except Exception as e:
                st.error(f"❌ {str(e)}")
