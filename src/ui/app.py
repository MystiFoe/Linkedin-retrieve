import time
import streamlit as st
import json
import pandas as pd
import io
import os
import sys
import requests
import time
from src.config import Config
from src.api.linkedin_api import LinkedInAPI
from src.data.data_processor import DataProcessor
from src.logger import app_logger

class LinkedInExtractorApp:
    """Main Streamlit application class for LinkedIn Data Extractor"""
    
    def __init__(self):
        """Initialize the application"""
        self.linkedin_api = LinkedInAPI()
        self.data_processor = DataProcessor()
        app_logger.debug("Initializing LinkedIn Extractor App")
        
    def setup_page(self):
        """Set up the Streamlit page with enterprise styling matching Allied Worldwide"""
        st.set_page_config(
            page_title="Allied LinkedIn Data Extractor",
            page_icon="🔗",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;600;700&display=swap');
        
        /* Allied Worldwide Professional Color Palette */
        :root {
            --primary-blue: #0066cc;
            --primary-dark: #004499;
            --primary-light: #3385d6;
            --secondary-gray: #2c3e50;
            --secondary-light: #34495e;
            --accent-blue: #007acc;
            --neutral-100: #f8f9fa;
            --neutral-200: #e9ecef;
            --neutral-300: #dee2e6;
            --neutral-400: #adb5bd;
            --neutral-500: #6c757d;
            --neutral-600: #495057;
            --neutral-700: #343a40;
            --neutral-800: #212529;
            --neutral-900: #1a1d20;
            --success: #28a745;
            --warning: #ffc107;
            --error: #dc3545;
            --white: #ffffff;
            --background-primary: #ffffff;
            --background-secondary: #f8f9fa;
            
            /* Minimal Shadows */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.08);
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Global Reset - Ultra Compact */
        .stApp {
            background: var(--white);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: var(--neutral-800);
            line-height: 1.4;
        }
        
        .main > div {
            padding: 0.5rem 0.75rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Ultra Tight Form Elements */
        .stTextInput, .stSelectbox, .stNumberInput, .stTextArea, .stFileUploader {
            margin-bottom: 0.25rem !important;
        }
        
        .stTextInput > label, .stSelectbox > label, .stNumberInput > label, .stTextArea > label {
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            color: var(--neutral-700) !important;
            margin-bottom: 0.15rem !important;
            line-height: 1.2 !important;
        }
        
        /* Ultra Compact Checkboxes */
        .stCheckbox {
            margin: 0.1rem 0 !important;
            padding: 0 !important;
        }
        
        .stCheckbox > label {
            font-size: 0.85rem !important;
            margin-bottom: 0 !important;
            padding: 0.1rem 0 !important;
            line-height: 1.3 !important;
        }
        
        .stCheckbox > div {
            padding-top: 0 !important;
        }
        
        /* Minimal Button Spacing */
        .stButton {
            margin: 0.25rem 0 !important;
        }
        
        /* Compact Typography */
        .main-header {
            font-family: 'Roboto', sans-serif;
            font-size: 1.75rem;
            font-weight: 600;
            color: var(--primary-blue);
            text-align: center;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }
        
        .main-subtitle {
            font-size: 0.9rem;
            color: var(--neutral-600);
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 400;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Compact Professional Cards */
        .enterprise-card {
            background: var(--white);
            border: 1px solid var(--neutral-200);
            border-radius: 6px;
            box-shadow: var(--shadow-sm);
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.2s ease;
        }
        
        .enterprise-card:hover {
            box-shadow: var(--shadow-md);
        }
        
        /* Compact Section Headers */
        .section-header {
            font-family: 'Roboto', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--neutral-800);
            margin: 0 0 0.5rem 0;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid var(--primary-blue);
        }
        
        /* Compact Form Controls */
        .stTextInput > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > div > select,
        .stNumberInput > div > input {
            background: var(--white);
            border: 1px solid var(--neutral-300);
            border-radius: 4px;
            font-size: 0.9rem;
            padding: 0.5rem 0.75rem;
            font-family: 'Inter', sans-serif;
            color: var(--neutral-800);
            transition: border-color 0.2s ease;
            box-shadow: none;
            font-weight: 400;
            line-height: 1.4;
            min-height: auto;
        }
        
        .stTextInput > div > input:focus,
        .stTextArea > div > textarea:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > input:focus {
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
            outline: none;
        }
        
        /* Professional Compact Buttons */
        .stButton > button {
            background: var(--primary-blue);
            color: var(--white);
            border: none;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.9rem;
            padding: 0.5rem 1.25rem;
            font-family: 'Inter', sans-serif;
            transition: background-color 0.2s ease;
            box-shadow: var(--shadow-xs);
            letter-spacing: 0.01em;
            min-width: 120px;
            cursor: pointer;
            line-height: 1.4;
        }
        
        .stButton > button:hover {
            background: var(--primary-dark);
            box-shadow: var(--shadow-sm);
        }
        
        .stButton > button:active {
            background: var(--primary-dark);
            transform: translateY(1px);
        }
        
        /* Download Buttons */
        .stDownloadButton > button {
            background: var(--success);
            color: var(--white);
            border: none;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.85rem;
            padding: 0.45rem 1rem;
            margin-top: 0.25rem;
            transition: background-color 0.2s ease;
            box-shadow: var(--shadow-xs);
        }
        
        .stDownloadButton > button:hover {
            background: #218838;
        }
        
        /* Compact Data Display */
        .stDataFrame {
            background: var(--white);
            border: 1px solid var(--neutral-200);
            border-radius: 4px;
            box-shadow: var(--shadow-xs);
            margin: 0.5rem 0;
            overflow: hidden;
        }
        
        /* Ultra Compact Expander */
        .stExpander {
            background: var(--white);
            border: 1px solid var(--neutral-200);
            border-radius: 4px;
            margin: 0.25rem 0;
            box-shadow: var(--shadow-xs);
        }
        
        .stExpanderHeader {
            font-weight: 500;
            color: var(--neutral-700);
            font-size: 0.85rem;
            padding: 0.4rem 0.75rem;
            line-height: 1.3;
        }
        
        /* Compact File Uploader */
        .stFileUploader > div {
            background: var(--background-secondary);
            border: 1px dashed var(--neutral-300);
            border-radius: 4px;
            padding: 0.75rem;
            text-align: center;
            transition: border-color 0.2s ease;
            margin: 0.25rem 0;
        }
        
        .stFileUploader > div:hover {
            border-color: var(--primary-blue);
        }
        
        /* Ultra Compact Sidebar */
        .stSidebar {
            background: var(--background-secondary);
            border-right: 1px solid var(--neutral-200);
        }
        
        .stSidebar > div {
            padding-top: 0.5rem;
        }
        
        .sidebar-title {
            font-family: 'Roboto', sans-serif;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--neutral-800);
            margin-bottom: 0.5rem;
            text-align: center;
            padding-bottom: 0.25rem;
            border-bottom: 1px solid var(--neutral-300);
        }
        
        /* Ultra Compact Navigation */
        .stSidebar .stButton > button {
            width: 100%;
            text-align: left;
            background: transparent;
            color: var(--neutral-600);
            border: none;
            margin: 0.05rem 0;
            font-weight: 400;
            padding: 0.3rem 0.5rem;
            border-radius: 3px;
            transition: all 0.2s ease;
            font-size: 0.8rem;
            line-height: 1.2;
            min-height: auto;
            box-shadow: none;
        }
        
        .stSidebar .stButton > button:hover {
            background: var(--neutral-100);
            color: var(--primary-blue);
            transform: none;
            box-shadow: none;
        }
        
        /* Compact Columns */
        .stColumn {
            padding: 0 0.25rem;
        }
        
        /* Minimal Captions */
        .stCaptionContainer {
            color: var(--neutral-500);
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            line-height: 1.3;
            font-weight: 400;
        }
        
        /* Compact Subheaders */
        h3 {
            font-family: 'Roboto', sans-serif;
            color: var(--neutral-800);
            font-weight: 500;
            font-size: 1rem;
            margin: 0.75rem 0 0.35rem 0;
            padding-bottom: 0.15rem;
            border-bottom: 1px solid var(--neutral-200);
            line-height: 1.3;
        }
        
        /* Compact Success Messages */
        .success-msg {
            color: var(--success);
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        /* Compact Metrics Display */
        .metric-display {
            background: var(--background-secondary);
            border: 1px solid var(--neutral-200);
            border-radius: 4px;
            padding: 0.75rem;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: var(--shadow-xs);
        }
        
        .metric-value {
            font-family: 'Roboto', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--primary-blue);
            margin-bottom: 0.15rem;
            line-height: 1.2;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: var(--neutral-500);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Alert Messages - Compact */
        .stSuccess, .stError, .stWarning, .stInfo {
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 4px;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        .stSuccess {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .stError {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .stWarning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        
        .stInfo {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background: var(--primary-blue);
            border-radius: 2px;
        }
        
        /* Spinner */
        .stSpinner {
            color: var(--primary-blue);
        }
        
        /* Remove Excessive Streamlit Spacing */
        .stContainer > div {
            padding-top: 0;
        }
        
        .stMarkdown {
            margin-bottom: 0.25rem;
        }
        
        /* Ultra tight spacing for related form elements */
        .stTextInput + .stTextInput,
        .stSelectbox + .stSelectbox,
        .stTextInput + .stSelectbox,
        .stSelectbox + .stTextInput {
            margin-top: 0.1rem;
        }
        
        /* Reduce space between form groups */
        .stTextInput + .stCheckbox,
        .stSelectbox + .stCheckbox {
            margin-top: 0.15rem;
        }
        
        .stCheckbox + .stTextInput,
        .stCheckbox + .stSelectbox {
            margin-top: 0.15rem;
        }
        
        /* Compact number inputs */
        .stNumberInput > div {
            margin-bottom: 0;
        }
        
        /* Remove extra padding from main content area */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Hide Streamlit Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        
        /* Responsive Design - Maintain Compactness */
        @media (max-width: 768px) {
            .main-header {
                font-size: 1.5rem;
            }
            
            .section-header {
                font-size: 1rem;
            }
            
            .main > div {
                padding: 0.5rem;
            }
            
            .stButton > button {
                padding: 0.4rem 1rem;
                font-size: 0.85rem;
            }
            
            .sidebar-title {
                font-size: 0.85rem;
            }
            
            .stSidebar .stButton > button {
                padding: 0.25rem 0.4rem;
                font-size: 0.75rem;
            }
        }
        
        /* Focus Management */
        .stButton > button:focus-visible,
        .stDownloadButton > button:focus-visible {
            outline: 2px solid var(--primary-blue);
            outline-offset: 1px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Professional Header
        st.markdown("""
        <div class='main-header'>Allied LinkedIn Data Extractor</div>
        <div class='main-subtitle'>
            Professional LinkedIn data extraction and analysis platform
        </div>
        """, unsafe_allow_html=True)

    def display_navigation(self):
        """Display professional enterprise navigation"""
        st.sidebar.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)
        
        pages = [
            ("Keyword Search", "Search LinkedIn posts by keywords"),
            ("Post Extraction", "Extract data from a specific LinkedIn post"),
            ("Profile Extraction", "Extract data from a LinkedIn profile"),
            ("Company Extraction", "Extract data from a LinkedIn company page"),
            ("Profile Extraction (by Keyword)", "Extract LinkedIn profiles by keyword search"),
            ("Post Extraction (By Keyword)", "End-to-end workflow: search, extract, merge, filter, export"),
            ("Profile Batch Extraction", "Upload an Excel file and extract profile data for all listed URLs"),
            ("Comment Generator", "Generate comments for post content from Excel file"),
        ]
        
        selected_page = st.session_state.get("selected_page", pages[0][0])
        
        for page_name, tooltip in pages:
            if st.sidebar.button(
                page_name,
                key=f"nav_{page_name}",
                help=tooltip,
                use_container_width=True
            ):
                st.session_state["selected_page"] = page_name
                selected_page = page_name
                st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### About")
        st.sidebar.info("Professional LinkedIn data extraction platform powered by Allied Worldwide's automation technology.")
        
        return st.session_state.get("selected_page", pages[0][0])
    
    def _get_automation_and_account(self, automation_label):
        """Helper to get automationId and connectedAccountId for a given automation label"""
        # Use the correct LinkedIn platform ID from TexAU
        platform_id = "622f03eb770f6bba0b8facaa"  # LinkedIn
        # Use the correct automation ID for LinkedIn Post Scraper
        if automation_label.lower() == "post extraction":
            automation_id = "63fdd06c82e9647288a2d925"  # LinkedIn Post Scraper
        elif automation_label.lower() == "profile extraction":
            automation_id = "63f48ee97022e05c116fc798"  # LinkedIn Profile Scraper
        else:
            automations = self.linkedin_api.get_automations(platform_id)
            automation_id = None
            for a in automations.get("data", []):
                if automation_label.lower() in a.get("label", "").lower():
                    automation_id = a["id"]
                    break
        # Use the actual connected LinkedIn account ID
        connected_account_id = "68340dc4e7bb1f6b5af36e98"
        return automation_id, connected_account_id

    def clean_dataframe_for_streamlit(self, df):
        """
        Clean DataFrame to prevent PyArrow serialization errors in Streamlit.
        Handles mixed data types, empty strings, and ensures consistent column types.
        """
        if df.empty:
            return df
        
        df_cleaned = df.copy()
        
        for column in df_cleaned.columns:
            # Handle mixed types and empty strings
            try:
                # First, replace empty strings with None
                df_cleaned[column] = df_cleaned[column].replace('', None)
                
                # Check if column contains numeric data mixed with strings
                non_null_values = df_cleaned[column].dropna()
                
                if len(non_null_values) == 0:
                    continue
                    
                # Try to identify if it should be numeric
                numeric_count = 0
                for val in non_null_values.head(10):  # Sample first 10 non-null values
                    try:
                        float(str(val))
                        numeric_count += 1
                    except (ValueError, TypeError):
                        break
                
                # If most values are numeric, convert to numeric
                if numeric_count > len(non_null_values.head(10)) * 0.7:
                    df_cleaned[column] = pd.to_numeric(df_cleaned[column], errors='coerce')
                else:
                    # Ensure all values are strings
                    df_cleaned[column] = df_cleaned[column].astype(str)
                    # Replace 'None' and 'nan' strings with empty string
                    df_cleaned[column] = df_cleaned[column].replace(['None', 'nan', 'NaN'], '')
                    
            except Exception as e:
                # If any error occurs, convert to string as fallback
                app_logger.warning(f"Error processing column {column}: {e}. Converting to string.")
                df_cleaned[column] = df_cleaned[column].astype(str).replace(['None', 'nan', 'NaN'], '')
        
        return df_cleaned

    def remove_empty_columns(self, df):
        """
        Remove empty columns and clean data types for Streamlit compatibility.
        """
        if df.empty:
            return df
        
        # Remove columns where all values are empty (NaN or empty string)
        df_cleaned = df.dropna(axis=1, how='all').loc[:, ~(df == '').all(axis=0)]
        
        # Clean the DataFrame for Streamlit/PyArrow compatibility
        df_cleaned = self.clean_dataframe_for_streamlit(df_cleaned)
        
        return df_cleaned

    def expand_profiles_to_df(self, profiles):
        """
        Robustly expand a list of profile results (which may be JSON strings or dicts, or lists of dicts)
        into a columnar DataFrame. Handles nested lists and mixed types.
        """
        if not profiles:
            return pd.DataFrame()
        expanded = []
        for p in profiles:
            if isinstance(p, str):
                try:
                    obj = json.loads(p)
                except Exception:
                    continue
            else:
                obj = p
            if isinstance(obj, list):
                expanded.extend(obj)
            else:
                expanded.append(obj)
        
        df = pd.json_normalize(expanded)
        return self.clean_dataframe_for_streamlit(df)

    def keyword_search_page(self):
        st.markdown("<div class='section-header'>Search LinkedIn Posts by Keywords</div>", unsafe_allow_html=True)
        st.caption("Find posts by keyword or LinkedIn search URL. Use advanced filters for precise targeting.")
        
        search_input = st.text_input(
            "Keyword or LinkedIn Search URL",
            placeholder="e.g., Marketing or https://www.linkedin.com/search/results/content/?keywords=Marketing",
            help="Enter a keyword or LinkedIn search URL."
        )
        
        with st.expander("Advanced Filters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.selectbox(
                    "Time Range",
                    ["", "PAST 24H", "PAST WEEK", "PAST MONTH"],
                    format_func=lambda x: x if x else "-- All Time --"
                )
                sort_by = st.selectbox(
                    "Sort By",
                    ["", "DATE POSTED", "RELEVANCE"],
                    format_func=lambda x: x if x else "-- Default --"
                )
            with col2:
                posted_by = st.selectbox(
                    "Posted By",
                    ["", "1st CONNECTION", "ME", "PEOPLE YOU FOLLOW"],
                    format_func=lambda x: x if x else "-- Anyone --"
                )
                extract_limit = st.number_input(
                    "Post Extraction Limit (Max. 2500)",
                    min_value=1, max_value=2500, value=10, step=1, format="%d"
                )
        
        if st.button("Extract Posts", help="Start extraction based on your search criteria"):
            if not search_input:
                st.error("Please enter a keyword or LinkedIn search URL.")
            else:
                with st.spinner("Extracting posts..."):
                    automation_id = "64099c6e0936e46db5d76f4c"
                    _, connected_account_id = self._get_automation_and_account("keyword search")
                    api_inputs = {"liPostSearchUrl": search_input}
                    if start_time:
                        api_inputs["startTime"] = {"PAST 24H": "past-24h", "PAST WEEK": "past-week", "PAST MONTH": "past-month"}[start_time]
                    if sort_by:
                        api_inputs["sortBy"] = {"DATE POSTED": "date_posted", "RELEVANCE": "relevance"}[sort_by]
                    if posted_by:
                        api_inputs["postedBy"] = {"1st CONNECTION": "first", "ME": "me", "PEOPLE YOU FOLLOW": "following"}[posted_by]
                    if extract_limit:
                        api_inputs["maxCountPostSearch"] = int(extract_limit)
                    result = self.linkedin_api.run_automation(
                        name="Post Search Export",
                        description="Export LinkedIn posts by keywords",
                        automation_id=automation_id,
                        connected_account_id=connected_account_id,
                        timezone="Asia/Kolkata",
                        inputs=api_inputs
                    )
                    data = result.get("data", {})
                    execution_id = data.get("id") or data.get("workflowId")
                    final_result = None
                    if execution_id:
                        for _ in range(120):
                            final_result = self.linkedin_api.get_execution_result(execution_id)
                            if final_result.get("data"):
                                break
                            time.sleep(1)
                    if final_result and "data" in final_result:
                        df = pd.json_normalize(final_result["data"])
                        df = self.remove_empty_columns(df)
                        
                        # Display metrics
                        st.markdown(f"""
                        <div class='metric-display'>
                            <div class='metric-value'>{len(df)}</div>
                            <div class='metric-label'>Posts Found</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.dataframe(self.clean_dataframe_for_streamlit(df), use_container_width=True)
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                            if not df.empty:
                                df.to_excel(writer, sheet_name="keyword_posts", index=False)
                        excel_buffer.seek(0)
                        st.download_button(
                            label="Download Excel Report",
                            data=excel_buffer.getvalue(),
                            file_name="linkedin_keyword_posts.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    else:
                        st.warning("No posts found matching the search criteria.")

    def post_extraction_page(self):
        """Display post extraction page"""
        st.markdown("<div class='section-header'>Extract LinkedIn Post Data</div>", unsafe_allow_html=True)
        
        post_url = st.text_input("LinkedIn Post URL", placeholder="https://www.linkedin.com/posts/...")
        extract_likers = st.checkbox("Extract post likers")
        extract_comments = st.checkbox("Extract post comments")
        
        if st.button("Extract Post Data"):
            if post_url and "linkedin.com" in post_url:
                try:
                    app_logger.info("Extracting data for post: {}", post_url)
                    with st.spinner("Extracting post data..."):
                        # 1. Extract post content
                        automation_id, connected_account_id = self._get_automation_and_account("post extraction")
                        result = self.linkedin_api.extract_post_data(post_url, automation_id, connected_account_id)
                        if result and "data" in result:
                            dfs = self.data_processor.convert_to_dataframe(result, "post")
                            for key in dfs:
                                dfs[key] = self.remove_empty_columns(dfs[key])
                            st.subheader("Post Information")
                            st.dataframe(self.clean_dataframe_for_streamlit(dfs["post"]), use_container_width=True)
                            if not dfs["reactors"].empty:
                                st.subheader(f"Reactors ({len(dfs['reactors'])})")
                                st.dataframe(self.clean_dataframe_for_streamlit(dfs["reactors"]), use_container_width=True)
                            if not dfs["commenters"].empty:
                                st.subheader(f"Commenters ({len(dfs['commenters'])})")
                                st.dataframe(self.clean_dataframe_for_streamlit(dfs["commenters"]), use_container_width=True)
                            # 2. Optionally extract likers
                            if extract_likers:
                                with st.spinner("Extracting post likers..."):
                                    likers_automation_id = "63fc575f7022e05c11bba145"  # LinkedIn Post Likers Export
                                    likers_result = self.linkedin_api.run_automation(
                                        name="Post Likers Export",
                                        description="Export LinkedIn post likers",
                                        automation_id=likers_automation_id,
                                        connected_account_id=connected_account_id,
                                        timezone="Asia/Kolkata",
                                        inputs={"liPostUrl": post_url}
                                    )
                                    data = likers_result.get("data", {})
                                    execution_id = data.get("id") or data.get("workflowId")
                                    likers_final_result = None
                                    if execution_id:
                                        for _ in range(60):
                                            likers_final_result = self.linkedin_api.get_execution_result(execution_id)
                                            if likers_final_result.get("data"):
                                                break
                                            time.sleep(1)
                                    likers_df = pd.DataFrame()
                                    if likers_final_result and "data" in likers_final_result:
                                        likers_data = likers_final_result["data"]
                                        if isinstance(likers_data, list):
                                            likers_df = pd.json_normalize(likers_data)
                                        elif isinstance(likers_data, dict):
                                            likers_df = pd.json_normalize([likers_data])
                                    dfs["likers"] = self.remove_empty_columns(likers_df)
                                    if not likers_df.empty:
                                        st.subheader(f"Likers ({len(likers_df)})")
                                        st.dataframe(self.clean_dataframe_for_streamlit(likers_df), use_container_width=True)
                            # 3. Optionally extract comments
                            if extract_comments:
                                with st.spinner("Extracting post comments..."):
                                    comments_automation_id = "63fc8cd27022e05c113c3c73"  # LinkedIn Comments Scraper
                                    comments_result = self.linkedin_api.run_automation(
                                        name="Comments Export",
                                        description="Export LinkedIn post comments",
                                        automation_id=comments_automation_id,
                                        connected_account_id=connected_account_id,
                                        timezone="Asia/Kolkata",
                                        inputs={"liPostUrl": post_url}
                                    )
                                    data = comments_result.get("data", {})
                                    execution_id = data.get("id") or data.get("workflowId")
                                    comments_final_result = None
                                    if execution_id:
                                        for _ in range(60):
                                            comments_final_result = self.linkedin_api.get_execution_result(execution_id)
                                            if comments_final_result.get("data"):
                                                break
                                            time.sleep(1)
                                    comments_df = pd.DataFrame()
                                    if comments_final_result and "data" in comments_final_result:
                                        comments_data = comments_final_result["data"]
                                        if isinstance(comments_data, list):
                                            comments_df = pd.json_normalize(comments_data)
                                        elif isinstance(comments_data, dict):
                                            comments_df = pd.json_normalize([comments_data])
                                    dfs["comments_export"] = self.remove_empty_columns(comments_df)
                                    if not comments_df.empty:
                                        st.subheader(f"Comments Export ({len(comments_df)})")
                                        st.dataframe(self.clean_dataframe_for_streamlit(comments_df), use_container_width=True)
                            # Download as Excel (multi-sheet)
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                                for sheet_name, df in dfs.items():
                                    if not df.empty:
                                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                            excel_buffer.seek(0)
                            if st.download_button(
                                label="Download Complete Report",
                                data=excel_buffer.getvalue(),
                                file_name=f"linkedin_post_data.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            ):
                                filepath = self.data_processor.export_to_excel(dfs, "post")
                                st.markdown(f"<p class='success-msg'>Report generated successfully</p>", unsafe_allow_html=True)
                        else:
                            st.warning("No data found for this post URL.")
                except Exception as e:
                    app_logger.error("Error in post extraction: {}", str(e))
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a valid LinkedIn post URL.")

    def profile_extraction_page(self):
        """Display profile extraction page"""
        st.markdown("<div class='section-header'>Extract LinkedIn Profile Data</div>", unsafe_allow_html=True)
        
        profile_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/...")
        extract_activity = st.checkbox("Extract profile activities")
        activity_limit = None
        if extract_activity:
            activity_limit = st.number_input(
                "Recent Activity Extract Limit (Max. 1000)",
                min_value=1, max_value=1000, value=10, step=1, format="%d"
            )
        extract_posts = st.checkbox("Extract profile posts")
        posts_limit = None
        if extract_posts:
            posts_limit = st.number_input(
                "Recent Post Extract Limit (Max. 1000)",
                min_value=1, max_value=1000, value=5, step=1, format="%d"
            )
        
        if st.button("Extract Profile Data"):
            if profile_url and "linkedin.com/in/" in profile_url:
                try:
                    app_logger.info("Extracting data for profile: {}", profile_url)
                    with st.spinner("Extracting profile data..."):
                        # Use correct input key for LinkedIn Profile Scraper
                        automation_id, connected_account_id = self._get_automation_and_account("profile extraction")
                        result = self.linkedin_api.run_automation(
                            name="Profile Extraction",
                            description="Extract LinkedIn profile data",
                            automation_id=automation_id,
                            connected_account_id=connected_account_id,
                            timezone="Asia/Kolkata",
                            inputs={"liProfileUrl": profile_url}
                        )
                        # Get execution id from result
                        data = result.get("data", {})
                        execution_id = data.get("id") or data.get("workflowId")
                        final_result = None
                        if execution_id:
                            for _ in range(60):
                                final_result = self.linkedin_api.get_execution_result(execution_id)
                                if final_result.get("data"):
                                    break
                                time.sleep(1)
                        all_dfs = {}
                        if final_result and "data" in final_result:
                            df = self.data_processor.convert_to_dataframe(final_result, "profile")
                            df = self.remove_empty_columns(df)
                            st.subheader("Profile Information")
                            st.dataframe(self.clean_dataframe_for_streamlit(df), use_container_width=True)
                            # Format and display additional profile sections nicely
                            profile_data = final_result.get("data", {})
                            all_dfs["profile"] = df
                            if "experiences" in profile_data:
                                st.subheader("Experiences")
                                exp_df = pd.json_normalize(profile_data["experiences"])
                                exp_df = self.remove_empty_columns(exp_df)
                                st.dataframe(self.clean_dataframe_for_streamlit(exp_df), use_container_width=True)
                                all_dfs["experiences"] = exp_df
                            if "education" in profile_data:
                                st.subheader("Education")
                                edu_df = pd.json_normalize(profile_data["education"])
                                edu_df = self.remove_empty_columns(edu_df)
                                st.dataframe(self.clean_dataframe_for_streamlit(edu_df), use_container_width=True)
                                all_dfs["education"] = edu_df
                            if "skills" in profile_data:
                                st.subheader("Skills")
                                skills_df = pd.DataFrame(profile_data["skills"], columns=["Skill"])
                                skills_df = self.remove_empty_columns(skills_df)
                                st.dataframe(self.clean_dataframe_for_streamlit(skills_df), use_container_width=True)
                                all_dfs["skills"] = skills_df
                    # Optional: Extract profile activity if checkbox is selected
                    if extract_activity:
                        with st.spinner("Extracting profile activities..."):
                            activity_automation_id = "63f5bf1d7022e05c1119cff2"  # LinkedIn Profile Activity Export
                            activity_inputs = {"liProfileUrl": profile_url}
                            # Always add the limit with default 10 if not specified
                            activity_inputs["maxCount"] = int(activity_limit) if activity_limit else 10
                            activity_result = self.linkedin_api.run_automation(
                                name="Profile Activity Export",
                                description="Export LinkedIn profile activity",
                                automation_id=activity_automation_id,
                                connected_account_id=connected_account_id,
                                timezone="Asia/Kolkata",
                                inputs=activity_inputs
                            )
                            activity_data = activity_result.get("data", {})
                            activity_execution_id = activity_data.get("id") or activity_data.get("workflowId")
                            activity_final_result = None
                            if activity_execution_id:
                                for _ in range(600):  # wait up to 10 minutes
                                    activity_final_result = self.linkedin_api.get_execution_result(activity_execution_id)
                                    if activity_final_result.get("data"):
                                        break
                                    time.sleep(1)
                            if activity_final_result and "data" in activity_final_result:
                                # TexAU sometimes returns activity data under a nested key, handle both cases
                                activity_data = activity_final_result["data"]
                                if isinstance(activity_data, list):
                                    activity_df = pd.json_normalize(activity_data)
                                elif isinstance(activity_data, dict):
                                    for v in activity_data.values():
                                        if isinstance(v, list):
                                            activity_df = pd.json_normalize(v)
                                            break
                                    else:
                                        activity_df = pd.json_normalize([activity_data])
                                activity_df = self.remove_empty_columns(activity_df)
                                if not activity_df.empty:
                                    st.subheader(f"Profile Activity ({len(activity_df)})")
                                    st.dataframe(self.clean_dataframe_for_streamlit(activity_df), use_container_width=True)
                                    all_dfs["profile_activity"] = activity_df
                    # Optional: Extract profile posts if checkbox is selected
                    if extract_posts:
                        with st.spinner("Extracting profile posts..."):
                            posts_automation_id = "649425e10f7b435e858547c2"  # LinkedIn Profile Posts Export
                            posts_inputs = {"liProfileUrl": profile_url}
                            # Always add the limit with default 5 if not specified
                            posts_inputs["maxCount"] = int(posts_limit) if posts_limit else 5
                            posts_result = self.linkedin_api.run_automation(
                                name="Profile Posts Export",
                                description="Export LinkedIn profile posts",
                                automation_id=posts_automation_id,
                                connected_account_id=connected_account_id,
                                timezone="Asia/Kolkata",
                                inputs=posts_inputs
                            )
                            data = posts_result.get("data", {})
                            execution_id = data.get("id") or data.get("workflowId")
                            posts_final_result = None
                            if execution_id:
                                for _ in range(120):
                                    posts_final_result = self.linkedin_api.get_execution_result(execution_id)
                                    if posts_final_result.get("data"):
                                        break
                                    time.sleep(1)
                            if posts_final_result and "data" in posts_final_result:
                                posts_data = posts_final_result["data"]
                                if isinstance(posts_data, list):
                                    posts_df = pd.json_normalize(posts_data)
                                elif isinstance(posts_data, dict):
                                    for v in posts_data.values():
                                        if isinstance(v, list):
                                            posts_df = pd.json_normalize(v)
                                            break
                                    else:
                                        posts_df = pd.json_normalize([posts_data])
                                posts_df = self.remove_empty_columns(posts_df)
                                if not posts_df.empty:
                                    st.subheader(f"Profile Posts ({len(posts_df)})")
                                    st.dataframe(self.clean_dataframe_for_streamlit(posts_df), use_container_width=True)
                                    all_dfs["profile_posts"] = posts_df
                    # Download as Excel (multi-sheet)
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                        for sheet_name, df in all_dfs.items():
                            if not df.empty:
                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                    excel_buffer.seek(0)
                    if st.download_button(
                        label="Download Complete Profile Report",
                        data=excel_buffer.getvalue(),
                        file_name=f"linkedin_profile_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ):
                        filepath = self.data_processor.export_to_excel(all_dfs, "profile")
                        st.markdown(f"<p class='success-msg'>Profile report generated successfully</p>", unsafe_allow_html=True)
                except Exception as e:
                    app_logger.error("Error in profile extraction: {}", str(e))
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a valid LinkedIn profile URL.")
    def company_extraction_page(self):
        """Display company extraction page"""
        st.markdown("<div class='section-header'>Extract LinkedIn Company Data</div>", unsafe_allow_html=True)
        
        company_url = st.text_input("LinkedIn Company URL", placeholder="https://www.linkedin.com/company/...")
        extract_employees = st.checkbox("Extract company employees")
        extract_activity = st.checkbox("Extract recent posts/activity")
        
        if st.button("Extract Company Data"):
            if company_url and "linkedin.com/company/" in company_url:
                try:
                    app_logger.info("Extracting data for company: {}", company_url)
                    with st.spinner("Extracting company data..."):
                        # Use correct automation ID and input key for LinkedIn Company Scraper
                        automation_id = "63f742037022e05c11a9440e"  # LinkedIn Company Scraper
                        connected_account_id = self._get_automation_and_account("company extraction")[1]
                        result = self.linkedin_api.run_automation(
                            name="Company Extraction",
                            description="Extract LinkedIn company data",
                            automation_id=automation_id,
                            connected_account_id=connected_account_id,
                            timezone="Asia/Kolkata", 
                            inputs={"liCompanyUrl": company_url}
                        )
                        data = result.get("data", {})
                        execution_id = data.get("id") or data.get("workflowId")
                        final_result = None
                        if execution_id:
                            for _ in range(120):
                                final_result = self.linkedin_api.get_execution_result(execution_id)
                                if final_result.get("data"):
                                    break
                                time.sleep(1)
                        dfs = {}
                        if final_result and "data" in final_result:
                            dfs = self.data_processor.convert_to_dataframe(final_result, "company")
                            for key in dfs:
                                dfs[key] = self.remove_empty_columns(dfs[key])
                            st.subheader("Company Information")
                            st.dataframe(self.clean_dataframe_for_streamlit(dfs["company"]), use_container_width=True)
                            if not dfs["personnel"].empty:
                                st.subheader("Key Personnel")
                                st.dataframe(self.clean_dataframe_for_streamlit(dfs["personnel"]), use_container_width=True)
                        
                    # Optionally extract company employees
                    if extract_employees:
                        with st.spinner("Extracting company employees..."):
                            # Predefined keywords for decision makers and key positions
                            decision_maker_keywords = "founder,co-founder,chairman,executive chairman,president,executive vice president,ceo,chief executive officer,group chief executive officer,chief executive office,coo,chief operating officer,group chief operating officer,cfo,chief financial officer,group chief financial officer,cto,chief technology officer,chief innovation officer,chief technology & strategy officer,chief digital officer,chief information officer,cio,chief information architect,chief technology architect,chief digital & information officer,chro,chief human resources officer,chief people officer,chief people and sustainability officer,chief human resources and corporate officer,interim chief people and culture officer,group director of people & purpose,head of talent,head of talent acquisition,svp of people & culture,cpo,chief product officer,chief product & customer officer,chief customer officer,chief merchandising officer,chief supply chain officer,chief supply chain and industrial officer,cro,chief revenue officer,chief commercial officer,group chief commercial officer,group managing director, business development,vp - sales,svp of sales,cmo,chief marketing officer,group brand director,marketing director,head of marketing,marketing manager,vp of global marketing,clo,chief legal officer,group general counsel,general counsel,chief legal counsel,chief risk officer,chief compliance officer,group chief risk and regulatory officer,chief strategy officer,group strategy director,chief analytics officer,vp strategy,director of strategy,strategic advisor,chief growth officer,group corporate development director,finance director,head of finance,group cfo,vp of finance,finance manager,chief data officer,chief information security officer,group ciso,group it infrastructure manager,chief scientific officer,chief medical officer,vp of it and mis,vp of engineering,chief technology & chief analytics officer,lcms technical manager,senior lc technical specialist,group communication director,vp of communications,media enquiries lead,director of production and content,chief sustainability officer,group esg,sustainable development director,chief policy officer,head of operations,vp of operations,head of membership and marketing,customer experience manager,chief operations officer,head of quality,svp customer services,group senior legal manager,board member,managing director,group managing director,business unit director,director,director of strategy & programmers,associate director,deputy director,svp,senior vice president,vp,vice president,avp,assistant vice president,head of hr,head of hr & engagement,head of finance & operations,head of china & asia,head of event content,head of marketing and data,head of commercial banking,chief administrative officer,chief development officer,chief transformation officer,chief science officer,group advisory leader,global assurance leader,global chairman,vp of product,vp of global demand generation,customer experience director,senior business specialist,business development manager,director of insurance & partnerships"
                            
                            employees_automation_id = "645e38f5f74978ad3262f00d"  # LinkedIn Company Employees Export
                            employees_inputs = {
                                "liCompanyUrl": company_url,
                                "keyword": decision_maker_keywords  # Send predefined keywords in backend
                            }
                            
                            employees_result = self.linkedin_api.run_automation(
                                name="Company Employees Export",
                                description="Export LinkedIn company employees",
                                automation_id=employees_automation_id,
                                connected_account_id=connected_account_id,
                                timezone="Asia/Kolkata",
                                inputs=employees_inputs
                            )
                            employees_data = employees_result.get("data", {})
                            employees_execution_id = employees_data.get("id") or employees_data.get("workflowId")
                            employees_final_result = None
                            if employees_execution_id:
                                for _ in range(600):  # wait up to 10 minutes
                                    employees_final_result = self.linkedin_api.get_execution_result(employees_execution_id)
                                    if employees_final_result.get("data"):
                                        break
                                    time.sleep(1)
                            if employees_final_result and "data" in employees_final_result:
                                employees_data = employees_final_result["data"]
                                if isinstance(employees_data, list):
                                    employees_df = pd.json_normalize(employees_data)
                                elif isinstance(employees_data, dict):
                                    employees_df = pd.json_normalize([employees_data])
                                employees_df = self.remove_empty_columns(employees_df)
                                if not employees_df.empty:
                                    st.subheader(f"Company Employees ({len(employees_df)})")
                                    
                                    # Display metrics
                                    st.markdown(f"""
                                    <div class='metric-display'>
                                        <div class='metric-value'>{len(employees_df)}</div>
                                        <div class='metric-label'>Decision-Maker Employees Found</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    st.dataframe(self.clean_dataframe_for_streamlit(employees_df), use_container_width=True)
                                    dfs["company_employees"] = employees_df
                    
                    # Optionally extract company recent posts/activity
                    if extract_activity:
                        with st.spinner("Extracting company recent posts/activity..."):
                            activity_automation_id = "64709b0f90217363308b2aaa"  # LinkedIn Company Activity Extractor
                            activity_inputs = {
                                "liCompanyUrl": company_url,
                                "mode": "all",  # Extract all types of content
                                "maxCountCompanyActivity": 5  # Limit to 5 recent posts
                            }
                            
                            activity_result = self.linkedin_api.run_automation(
                                name="Company Activity Export",
                                description="Export LinkedIn company recent posts/activity",
                                automation_id=activity_automation_id,
                                connected_account_id=connected_account_id,
                                timezone="Asia/Kolkata",
                                inputs=activity_inputs
                            )
                            activity_data = activity_result.get("data", {})
                            activity_execution_id = activity_data.get("id") or activity_data.get("workflowId")
                            activity_final_result = None
                            if activity_execution_id:
                                for _ in range(600):  # wait up to 10 minutes
                                    activity_final_result = self.linkedin_api.get_execution_result(activity_execution_id)
                                    if activity_final_result.get("data"):
                                        break
                                    time.sleep(1)
                            if activity_final_result and "data" in activity_final_result:
                                activity_data = activity_final_result["data"]
                                if isinstance(activity_data, list):
                                    activity_df = pd.json_normalize(activity_data)
                                elif isinstance(activity_data, dict):
                                    activity_df = pd.json_normalize([activity_data])
                                activity_df = self.remove_empty_columns(activity_df)
                                if not activity_df.empty:
                                    st.subheader(f"Recent Posts/Activity ({len(activity_df)})")
                                    
                                    # Display metrics
                                    st.markdown(f"""
                                    <div class='metric-display'>
                                        <div class='metric-value'>{len(activity_df)}</div>
                                        <div class='metric-label'>Recent Posts Found</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    st.dataframe(self.clean_dataframe_for_streamlit(activity_df), use_container_width=True)
                                    dfs["company_activity"] = activity_df
                    
                    # Export button
                    if dfs:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                            for sheet_name, df in dfs.items():
                                if not df.empty:
                                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                        excel_buffer.seek(0)
                        if st.download_button(
                            label="Download Company Report",
                            data=excel_buffer.getvalue(),
                            file_name=f"linkedin_company_data.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        ):
                            filepath = self.data_processor.export_to_excel(dfs, "company")
                            st.markdown(f"<p class='success-msg'>Company report generated successfully</p>", unsafe_allow_html=True)
                    else:
                        st.warning("No data found for this company URL.")
                except Exception as e:
                    app_logger.error("Error in company extraction: {}", str(e))
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a valid LinkedIn company URL.")

    def profile_extraction_by_keyword_page(self):
        """Pipeline: Profile Extraction by Keyword or LinkedIn Search URL → Filter by Headline → Export"""
        st.markdown("<div class='section-header'>Profile Extraction by Keyword</div>", unsafe_allow_html=True)
        st.caption("Extract LinkedIn profiles by keyword search with automatic decision-maker filtering")

        keyword_or_url = st.text_input("Keyword or LinkedIn People Search URL", key="profile_pipeline_keyword")
        search_limit = st.number_input("Number of profiles to extract", min_value=1, max_value=1000, value=50, step=1, key="profile_pipeline_search_limit")
        
        if st.button("Run Profile Extraction Pipeline", key="profile_pipeline_run"):
            if keyword_or_url:
                with st.spinner("Running profile extraction pipeline..."):
                    # Step 1: Run Automation
                    automation_id = "63f5eaad7022e05c1180244a"  # LinkedIn People Search Export automation
                    connected_account_id = self._get_automation_and_account("keyword search")[1]
                    api_inputs = {
                        "liPeopleSearchUrl": keyword_or_url,
                        "maxCountPeopleSearch": int(search_limit)
                    }
                    result = self.linkedin_api.run_automation(
                        name="Profile Extraction by Keyword",
                        description="Pipeline: Extract LinkedIn profiles by keyword or search URL",
                        automation_id=automation_id,
                        connected_account_id=connected_account_id,
                        timezone="Asia/Kolkata",
                        inputs=api_inputs
                    )
                    data = result.get("data", {})
                    execution_id = data.get("id") or data.get("workflowId")

                    final_result = None
                    if execution_id:
                        for _ in range(300):
                            final_result = self.linkedin_api.get_execution_result(execution_id)
                            if final_result.get("data"):
                                break
                            time.sleep(1)

                    if not (final_result and "data" in final_result):
                        st.error("No profiles found for the given input.")
                        return

                    profiles_df = pd.json_normalize(final_result["data"])
                    profiles_df = self.remove_empty_columns(profiles_df)

                    # Step 2: Filter Decision-Makers (based on 'headline' column from API)
                    keywords = [
    # Founders, Chairs, Presidents
    "founder", "co-founder", "chairman", "executive chairman", "president", "executive vice president",
    
    # CEO-level
    "ceo", "chief executive officer", "group chief executive officer", "chief executive office",

    # COO-level
    "coo", "chief operating officer", "group chief operating officer",

    # CFO-level
    "cfo", "chief financial officer", "group chief financial officer",

    # CTO/Technology/Innovation
    "cto", "chief technology officer", "chief innovation officer", "chief technology & strategy officer", 
    "chief digital officer", "chief information officer", "cio", "chief information architect", "chief technology architect",
    "chief digital & information officer",

    # CHRO / People / Culture / Talent
    "chro", "chief human resources officer", "chief people officer", "chief people and sustainability officer",
    "chief human resources and corporate officer", "interim chief people and culture officer",
    "group director of people & purpose", "head of talent", "head of talent acquisition",
    "svp of people & culture",

    # Product & Customer
    "cpo", "chief product officer", "chief product & customer officer", "chief customer officer", 
    "chief merchandising officer", "chief supply chain officer", "chief supply chain and industrial officer",

    # Revenue & Commercial
    "cro", "chief revenue officer", "chief commercial officer", "group chief commercial officer",
    "group managing director, business development", "vp - sales", "svp of sales",

    # Marketing & Brand
    "cmo", "chief marketing officer", "group brand director", "marketing director", "head of marketing",
    "marketing manager", "vp of global marketing",

    # Legal, Risk, Compliance
    "clo", "chief legal officer", "group general counsel", "general counsel", "chief legal counsel",
    "chief risk officer", "chief compliance officer", "group chief risk and regulatory officer",

    # Strategy, Growth, Analytics
    "chief strategy officer", "group strategy director", "chief analytics officer", "vp strategy",
    "director of strategy", "strategic advisor", "chief growth officer", "group corporate development director",

    # Finance / Accounting
    "finance director", "head of finance", "group cfo", "vp of finance", "finance manager",

    # Data / Security
    "chief data officer", "chief information security officer", "group ciso", "group it infrastructure manager",

    # Science / Technology / Medical
    "chief scientific officer", "chief medical officer", "vp of it and mis", "vp of engineering", 
    "chief technology & chief analytics officer", "lcms technical manager", "senior lc technical specialist",

    # Communications / Media / Brand
    "group communication director", "vp of communications", "media enquiries lead", "director of production and content",

    # Sustainability / ESG / Policy
    "chief sustainability officer", "group esg", "sustainable development director", "chief policy officer",

    # Operations / Services
    "head of operations", "vp of operations", "head of membership and marketing", "customer experience manager",
    "chief operations officer", "head of quality", "svp customer services", "group senior legal manager",

    # Board Members / Directors
    "board member", "managing director", "group managing director", "business unit director",
    "director", "director of strategy & programmers", "associate director", "deputy director", "Chief Architect",
    
    # Misc Executive Roles
    "svp", "senior vice president", "vp", "vice president", "avp", "assistant vice president",

    # Functional Heads
    "head of hr", "head of hr & engagement", "head of finance & operations", "head of china & asia",
    "head of event content", "head of marketing and data", "head of commercial banking",

    # Misc Titles from List
    "chief administrative officer", "chief development officer", "chief transformation officer",
    "chief science officer", "group advisory leader", "global assurance leader", "global chairman",
    "vp of product", "vp of global demand generation", "customer experience director",
    "senior business specialist", "business development manager", "director of insurance & partnerships"
]


                    if "headline" in profiles_df.columns:
                        profiles_df["headline"] = profiles_df["headline"].astype(str).str.lower()
                        mask = profiles_df["headline"].apply(lambda x: any(k.lower() in x for k in keywords))
                        filtered_df = profiles_df[mask]
                    else:
                        st.warning("'headline' column not found. No filtering applied.")
                        filtered_df = profiles_df

                    # Define important columns in order
                    important_columns = [
                        "liPublicProfileUrl", "firstName", "lastName", "companyName", "jobTitle", "headline",
                        "locationArea", "connectionDegree", "emailAddressPersonal", "liProfileUrl", "liProfileImageUrl", "liProfilePublicId",
                        "snProfileUrl", "isPremium", "pastJobTitle", "hashtags", "serviceProvider"
                    ]

                    display_df = filtered_df[[col for col in important_columns if col in filtered_df.columns]]
                    
                    # Display metrics
                    st.markdown(f"""
                    <div class='metric-display'>
                        <div class='metric-value'>{len(filtered_df)}</div>
                        <div class='metric-label'>Decision-Maker Profiles</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(self.clean_dataframe_for_streamlit(display_df), use_container_width=True)

                    # Download filtered data
                    output_dir = "outputs"
                    os.makedirs(output_dir, exist_ok=True)
                    filtered_data_path = os.path.join(output_dir, "filtered_profiles.xlsx")
                    with pd.ExcelWriter(filtered_data_path, engine="openpyxl") as writer:
                        filtered_df.to_excel(writer, sheet_name="filtered_profiles", index=False)

                    with open(filtered_data_path, "rb") as f:
                        st.download_button(
                            label="Download Filtered Profiles",
                            data=f,
                            file_name="filtered_profiles.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

    def decision_maker_pipeline_page(self):
        """Simplified pipeline: Keyword Search → Filter by Headline → Export"""
        st.markdown("<div class='section-header'>Post Extraction by Keyword</div>", unsafe_allow_html=True)
        st.caption("Extract LinkedIn posts by keyword with automatic decision-maker filtering")

        keyword = st.text_input("Keyword for LinkedIn post search", key="pipeline_keyword_auto")

        with st.expander("Advanced Filters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.selectbox(
                    "Time Range",
                    ["", "PAST 24H", "PAST WEEK", "PAST MONTH"],
                    format_func=lambda x: x if x else "-- All Time --"
                )
                sort_by = st.selectbox(
                    "Sort By",
                    ["", "DATE POSTED", "RELEVANCE"],
                    format_func=lambda x: x if x else "-- Default --"
                )
            with col2:
                posted_by = st.selectbox(
                    "Posted By",
                    ["", "1st CONNECTION", "ME", "PEOPLE YOU FOLLOW"],
                    format_func=lambda x: x if x else "-- Anyone --"
                )
                search_limit = st.number_input(
                    "Number of posts to extract (Max. 2500)",
                    min_value=1, max_value=2500, value=10, step=1, key="pipeline_search_limit_auto"
                )

        if st.button("Run Pipeline", key="pipeline_run_all"):
            if keyword:
                with st.spinner("Running pipeline..."):
                    # Step 1: Keyword Search
                    automation_id = "64099c6e0936e46db5d76f4c"
                    connected_account_id = self._get_automation_and_account("keyword search")[1]
                    api_inputs = {"liPostSearchUrl": keyword}

                    if start_time:
                        api_inputs["startTime"] = {"PAST 24H": "past-24h", "PAST WEEK": "past-week", "PAST MONTH": "past-month"}[start_time]
                    if sort_by:
                        api_inputs["sortBy"] = {"DATE POSTED": "date_posted", "RELEVANCE": "relevance"}[sort_by]
                    if posted_by:
                        api_inputs["postedBy"] = {"1st CONNECTION": "first", "ME": "me", "PEOPLE YOU FOLLOW": "following"}[posted_by]
                    if search_limit:
                        api_inputs["maxCountPostSearch"] = int(search_limit)

                    result = self.linkedin_api.run_automation(
                        name="Pipeline Keyword Search",
                        description="Pipeline: Search LinkedIn posts by keywords",
                        automation_id=automation_id,
                        connected_account_id=connected_account_id,
                        timezone="Asia/Kolkata",
                        inputs=api_inputs
                    )
                    data = result.get("data", {})
                    execution_id = data.get("id") or data.get("workflowId")

                    final_result = None
                    if execution_id:
                        for _ in range(120):
                            final_result = self.linkedin_api.get_execution_result(execution_id)
                            if final_result.get("data"):
                                break
                            time.sleep(1)

                    if not (final_result and "data" in final_result):
                        st.error("No posts found for the given keyword.")
                        return

                    posts_df = pd.json_normalize(final_result["data"])
                    posts_df = self.remove_empty_columns(posts_df)

                    # Step 2: Filter Decision-Makers (only using 'liProfileHeadline' column)
                    keywords = [
        # Founders, Chairs, Presidents
        "founder", "co-founder", "chairman", "executive chairman", "president", "executive vice president",
        
        # CEO-level
        "ceo", "chief executive officer", "group chief executive officer", "chief executive office",

        # COO-level
        "coo", "chief operating officer", "group chief operating officer",

        # CFO-level
        "cfo", "chief financial officer", "group chief financial officer",

        # CTO/Technology/Innovation
        "cto", "chief technology officer", "chief innovation officer", "chief technology & strategy officer", 
        "chief digital officer", "chief information officer", "cio", "chief information architect", "chief technology architect",
        "chief digital & information officer",

        # CHRO / People / Culture / Talent
        "chro", "chief human resources officer", "chief people officer", "chief people and sustainability officer",
        "chief human resources and corporate officer", "interim chief people and culture officer",
        "group director of people & purpose", "head of talent", "head of talent acquisition",
        "svp of people & culture",

        # Product & Customer
        "cpo", "chief product officer", "chief product & customer officer", "chief customer officer", 
        "chief merchandising officer", "chief supply chain officer", "chief supply chain and industrial officer",

        # Revenue & Commercial
        "cro", "chief revenue officer", "chief commercial officer", "group chief commercial officer",
        "group managing director, business development", "vp - sales", "svp of sales",

        # Marketing & Brand
        "cmo", "chief marketing officer", "group brand director", "marketing director", "head of marketing",
        "marketing manager", "vp of global marketing",

        # Legal, Risk, Compliance
        "clo", "chief legal officer", "group general counsel", "general counsel", "chief legal counsel",
        "chief risk officer", "chief compliance officer", "group chief risk and regulatory officer",

        # Strategy, Growth, Analytics
        "chief strategy officer", "group strategy director", "chief analytics officer", "vp strategy",
        "director of strategy", "strategic advisor", "chief growth officer", "group corporate development director",

        # Finance / Accounting
        "finance director", "head of finance", "group cfo", "vp of finance", "finance manager",

        # Data / Security
        "chief data officer", "chief information security officer", "group ciso", "group it infrastructure manager",

        # Science / Technology / Medical
        "chief scientific officer", "chief medical officer", "vp of it and mis", "vp of engineering", 
        "chief technology & chief analytics officer", "lcms technical manager", "senior lc technical specialist",

        # Communications / Media / Brand
        "group communication director", "vp of communications", "media enquiries lead", "director of production and content",

        # Sustainability / ESG / Policy
        "chief sustainability officer", "group esg", "sustainable development director", "chief policy officer",

        # Operations / Services
        "head of operations", "vp of operations", "head of membership and marketing", "customer experience manager",
        "chief operations officer", "head of quality", "svp customer services", "group senior legal manager",

        # Board Members / Directors
        "board member", "managing director", "group managing director", "business unit director",
        "director", "director of strategy & programmers", "associate director", "deputy director", "Chief Architect",
        
        # Misc Executive Roles
        "svp", "senior vice president", "vp", "vice president", "avp", "assistant vice president",

        # Functional Heads
        "head of hr", "head of hr & engagement", "head of finance & operations", "head of china & asia",
        "head of event content", "head of marketing and data", "head of commercial banking",

        # Misc Titles from List
        "chief administrative officer", "chief development officer", "chief transformation officer",
        "chief science officer", "group advisory leader", "global assurance leader", "global chairman",
        "vp of product", "vp of global demand generation", "customer experience director",
        "senior business specialist", "business development manager", "director of insurance & partnerships"
    ]


                    if "liProfileHeadline" in posts_df.columns:
                        posts_df["liProfileHeadline"] = posts_df["liProfileHeadline"].astype(str).str.lower()
                        mask = posts_df["liProfileHeadline"].apply(lambda x: any(k.lower() in x for k in keywords))
                        filtered_df = posts_df[mask]
                    else:
                        st.warning("'liProfileHeadline' column not found. No filtering applied.")
                        filtered_df = posts_df

                    # Define important columns in the specified order
                    important_columns = [
                        "liPublicProfileUrl", "firstName", "lastName", "companyName", "liCompanyPublicUrl", "headcountRange",
                        "jobLocationArea", "jobTitle", "jobTenure", "profileDescription", "liProfileHeadline", "emailAddressPersonal",
                        "profileLocationCountry", "profileLocationCity", "profileLocationArea", "locationCountryCode", "industry"
                    ]

                    display_df = filtered_df[[col for col in important_columns if col in filtered_df.columns]]
                    
                    # Display metrics
                    st.markdown(f"""
                    <div class='metric-display'>
                        <div class='metric-value'>{len(filtered_df)}</div>
                        <div class='metric-label'>Decision-Maker Posts</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(self.clean_dataframe_for_streamlit(display_df), use_container_width=True)

                    # Download filtered data
                    output_dir = "outputs"
                    os.makedirs(output_dir, exist_ok=True)
                    filtered_data_path = os.path.join(output_dir, "decision_makers.xlsx")
                    with pd.ExcelWriter(filtered_data_path, engine="openpyxl") as writer:
                        filtered_df.to_excel(writer, sheet_name="decision_makers", index=False)

                    with open(filtered_data_path, "rb") as f:
                        st.download_button(
                            label="Download Decision-Makers Report",
                            data=f,
                            file_name="decision_makers.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

    def profile_batch_extraction_page(self):
        """Upload an Excel file, extract profile data for all liPublicProfileUrl, filter headcount > 450, and export."""
        st.markdown("<div class='section-header'>Profile Batch Extraction</div>", unsafe_allow_html=True)
        st.caption("Upload Excel file with profile URLs for batch processing and automated filtering")

        uploaded_file = st.file_uploader("Upload Excel file with 'liPublicProfileUrl' column", type=["xlsx"])
        
        if uploaded_file:
            try:
                input_df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"Failed to read Excel file: {e}")
                return

            if "liPublicProfileURL" not in input_df.columns:
                st.error("The uploaded file must contain a 'liPublicProfileURL' column.")
                return

            url_col_input = "liPublicProfileURL"
            profile_urls = input_df[url_col_input].dropna().unique().tolist()

            st.info(f"Found {len(profile_urls)} unique profile URLs. Starting extraction...")
            profile_data = []
            extraction_errors = []

            for idx, url in enumerate(profile_urls):
                st.write(f"Extracting profile {idx+1}/{len(profile_urls)}: {url}")
                try:
                    result = self.linkedin_api.run_automation(
                        name="Batch Profile Extraction",
                        description="Batch: Extract profile data",
                        automation_id="63f48ee97022e05c116fc798",
                        connected_account_id=self._get_automation_and_account("profile extraction")[1],
                        timezone="Asia/Kolkata",
                        inputs={"liProfileUrl": url}
                    )
                    data = result.get("data", {})
                    execution_id = data.get("id") or data.get("workflowId")
                    final_result = None
                    if execution_id:
                        for _ in range(60):
                            final_result = self.linkedin_api.get_execution_result(execution_id)
                            if final_result.get("data"):
                                break
                            time.sleep(1)
                    if final_result and "data" in final_result:
                        profile_data.append(final_result["data"])
                    else:
                        extraction_errors.append(f"No data for {url}")
                        st.error(f"Profile extraction failed or limit reached for: {url}. Try again later.")
                        break
                except Exception as e:
                    extraction_errors.append(f"Error for {url}: {e}")
                    st.error(f"Profile extraction failed for: {url}. Error: {e}")
                    break

            if profile_data:
                profiles_df = self.expand_profiles_to_df(profile_data)
                profiles_df = self.remove_empty_columns(profiles_df)

                profiles_df = profiles_df.rename(columns={
                    col: (f"profile_{col}" if col.lower() != url_col_input.lower() else col)
                    for col in profiles_df.columns
                })

                n = min(len(input_df), len(profiles_df))
                merged_df = pd.concat([input_df.iloc[:n].reset_index(drop=True), profiles_df.iloc[:n].reset_index(drop=True)], axis=1)
                merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

                # Auto filter: Headcount > 450
                if 'profile_headcountRange' in merged_df.columns:
                    def parse_headcount(x):
                        try:
                            parts = str(x).replace("+","").replace(",","").split("-")
                            if len(parts) == 2:
                                return int(parts[1].strip())
                            elif parts[0].strip().isdigit():
                                return int(parts[0].strip())
                        except:
                            return 0
                        return 0

                    merged_df['parsed_headcount'] = merged_df['profile_headcountRange'].apply(parse_headcount)
                    filtered_df = merged_df[merged_df['parsed_headcount'] > 450].drop(columns=['parsed_headcount'])

                    # Display metrics
                    st.markdown(f"""
                    <div class='metric-display'>
                        <div class='metric-value'>{len(filtered_df)}</div>
                        <div class='metric-label'>Large Companies (>450 employees)</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No 'profile_headcountRange' column found. Exporting full merged result.")
                    filtered_df = merged_df

                st.dataframe(self.clean_dataframe_for_streamlit(filtered_df), use_container_width=True)

                output_dir = "outputs"
                os.makedirs(output_dir, exist_ok=True)
                merged_data_path = os.path.join(output_dir, "batch_profiles_filtered.xlsx")

                with pd.ExcelWriter(merged_data_path, engine="openpyxl") as writer:
                    filtered_df.to_excel(writer, sheet_name="profiles", index=False)

                with open(merged_data_path, "rb") as f:
                    st.download_button(
                        label="Download Batch Processing Report",
                        data=f,
                        file_name="batch_profiles_filtered.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    def comment_generator_page(self):
        """Display comment generator page for LinkedIn post content"""
        import requests
        import time
        from src.config import Config
        
        st.markdown("<div class='section-header'>Generate Comments for LinkedIn Posts</div>", unsafe_allow_html=True)
        st.caption("Upload Excel file with post content to generate AI-powered professional comments")
        
        # File uploader for Excel file
        uploaded_file = st.file_uploader("Upload Excel file with post content", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # Load the Excel file
                df = pd.read_excel(uploaded_file)
                
                # Check if 'liPostContent' column exists
                if 'liPostContent' not in df.columns:
                    st.error("The Excel file must contain a column named 'liPostContent'.")
                else:
                    st.success(f"Successfully loaded Excel file with {len(df)} rows.")
                    
                    # Display the dataframe
                    st.subheader("Preview of uploaded data")
                    st.dataframe(self.clean_dataframe_for_streamlit(df.head(5)), use_container_width=True)
                    
                    # Button to generate comments
                    if st.button("Generate Comments", help="Start generating comments for each post content"):
                        with st.spinner("Initializing AI model connection..."):
                            try:
                                # Load configuration to get HF token
                                config = Config.load_config()
                                hf_token = config.get("HF_TOKEN")
                                
                                if not hf_token:
                                    try:
                                        hf_token = st.secrets["HF_TOKEN"]
                                    except:
                                        import os
                                        hf_token = os.getenv("HF_TOKEN")
                                
                                if not hf_token:
                                    st.error("HF_TOKEN not found in configuration.")
                                    return
                                
                                # Clean token
                                clean_token = hf_token.replace("Bearer ", "") if hf_token.startswith("Bearer ") else hf_token
                                
                                # API Configuration
                                API_URL = "https://iik6wo71sp9xhxjs.us-east-1.aws.endpoints.huggingface.cloud"
                                headers = {
                                    "Accept": "application/json",
                                    "Authorization": f"Bearer {clean_token}",
                                    "Content-Type": "application/json"
                                }
                                
                                def query(payload):
                                    """Query function with proper error handling"""
                                    try:
                                        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
                                        if response.status_code == 200:
                                            return response.json()
                                        else:
                                            return {"error": f"Status {response.status_code}: {response.text}"}
                                    except requests.exceptions.Timeout:
                                        return {"error": "Timeout after 2 minutes"}
                                    except Exception as e:
                                        return {"error": str(e)}
                                
                                # Test connection
                                st.info("Testing connection...")
                                test_output = query({
                                    "inputs": "This is a test post about technology innovation",
                                    "parameters": {
                                        "max_new_tokens": 100,
                                        "temperature": 0.7,
                                        "do_sample": True
                                    }
                                })
                                
                                if "error" in test_output:
                                    st.error(f"❌ Connection failed: {test_output['error']}")
                                    st.info("💡 The endpoint may be cold starting. This can take 1-2 minutes.")
                                    return
                                
                                st.success("✅ Connected successfully!")
                                
                                # Create progress tracking
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                
                                # Add comment column
                                df['generated_comment'] = ""
                                successful_generations = 0
                                
                                # Process each row with EXACT same parameters as local
                                for i, row in enumerate(df.itertuples()):
                                    if hasattr(row, 'liPostContent') and pd.notna(row.liPostContent) and str(row.liPostContent).strip():
                                        status_text.text(f"Generating comment for post {i+1} of {len(df)}...")
                                        
                                        post_content = str(row.liPostContent)
                                        if len(post_content) > 500:
                                            post_content = post_content[:500] + "..."
                                        
                                        # EXACT SAME PARAMETERS as local implementation
                                        output = query({
                                            "inputs": post_content,  # Handler will add the prompt
                                            "parameters": {
                                                "max_new_tokens": 100,
                                                "temperature": 0.7,      # Same as local
                                                "do_sample": True        # Same as local
                                            }
                                        })
                                        
                                        if "error" in output:
                                            comment = f"Error: {output['error']}"
                                        else:
                                            try:
                                                # Handle response format properly
                                                if isinstance(output, list) and len(output) > 0:
                                                    comment = output[0].get('generated_text', 'No response')
                                                elif isinstance(output, dict):
                                                    comment = output.get('generated_text', 'No response')
                                                else:
                                                    comment = "Error: Invalid response format"
                                            except Exception as e:
                                                comment = f"Error parsing response: {str(e)}"
                                        
                                        df.at[i, 'generated_comment'] = comment
                                        
                                        if not comment.startswith("Error:"):
                                            successful_generations += 1
                                        
                                        # Short delay to avoid rate limiting
                                        time.sleep(0.5)
                                        
                                    else:
                                        df.at[i, 'generated_comment'] = "No content to generate comment"
                                    
                                    progress_bar.progress((i + 1) / len(df))
                                
                                # Show results
                                st.success(f"🎉 Generated {successful_generations}/{len(df)} comments!")
                                st.markdown(f"""
                                <div class='metric-display'>
                                    <div class='metric-value'>{successful_generations}</div>
                                    <div class='metric-label'>Comments Generated</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.subheader("Results with Generated Comments")
                                st.dataframe(self.clean_dataframe_for_streamlit(df), use_container_width=True)
                                
                                # Download button
                                excel_buffer = io.BytesIO()
                                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                                    df.to_excel(writer, sheet_name="posts_with_comments", index=False)
                                excel_buffer.seek(0)
                                
                                st.download_button(
                                    label="Download Comments Report",
                                    data=excel_buffer.getvalue(),
                                    file_name="linkedin_posts_with_comments.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetsheet"
                                )
                                
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                                app_logger.error(f"Error in comment generation: {str(e)}")
                                
            except Exception as e:
                st.error(f"Error reading the Excel file: {str(e)}")
                app_logger.error(f"Error reading Excel file: {str(e)}")
    def run(self):
        """Run the Streamlit application"""
        self.setup_page()
        selected_page = self.display_navigation()
        
        if selected_page == "Keyword Search":
            self.keyword_search_page()
        elif selected_page == "Post Extraction":
            self.post_extraction_page()
        elif selected_page == "Profile Extraction":
            self.profile_extraction_page()
        elif selected_page == "Company Extraction":
            self.company_extraction_page()
        elif selected_page == "Profile Extraction (by Keyword)":
            self.profile_extraction_by_keyword_page()
        elif selected_page == "Post Extraction (By Keyword)":
            self.decision_maker_pipeline_page()
        elif selected_page == "Profile Batch Extraction":
            self.profile_batch_extraction_page()
        elif selected_page == "Comment Generator":
            self.comment_generator_page()

if __name__ == "__main__":
    app = LinkedInExtractorApp()
    app.run()