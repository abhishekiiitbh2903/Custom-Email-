import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from links import Portfolio
from utils import clean_text
import os 
from dotenv import load_dotenv
load_dotenv()
from langchain.globals import set_verbose
set_verbose(True)

def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📧 Cold Mail Generator using Llama</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Generate personalized cold emails based on job descriptions.</p>", unsafe_allow_html=True)

    url_input = st.text_input("Enter a Job URL:", value="", placeholder="Enter Job URL here")

    submit_button = st.button("Submit", help="Click to generate cold email", key="submit_button")

    if submit_button:
        st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
        try:
            with st.spinner("Processing... Please wait."):
                loader = WebBaseLoader([url_input])
                loaded_data = loader.load()

                if not loaded_data:
                    st.error("Failed to load content from the provided URL.")
                    return

                data = clean_text(loaded_data.pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                st.success(f"Found {len(jobs)} job(s) in the provided URL.")
                
                if len(jobs) == 0:
                    st.warning("No jobs found in the provided URL.")
                else:
                    for i, job in enumerate(jobs[:3], start=1):
                        skills = job.get('skills', [])
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)
                        st.markdown(f"<h3 style='color: #4CAF50;'>Job {i}</h3>", unsafe_allow_html=True)
                        st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")
        finally:
            st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    USER_AGENT = os.getenv("USER_AGENT")
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
