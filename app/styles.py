"""
Custom CSS styles for Streamlit.
"""

def get_custom_css() -> str:
    """
    Returns the custom CSS for the application.
    
    Returns:
        String containing CSS to inject
    """
    return """
    <style>
    /* Main Background & Text */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers with Gradient */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #3B82F6, #1D4ED8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Sidebar Styling & Navigation */
    section[data-testid="stSidebar"] {
        background-color: #11141E !important;
        border-right: 1px solid #232936 !important;
        width: 320px !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        background: -webkit-linear-gradient(45deg, #3B82F6, #1D4ED8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        border-bottom: none !important;
    }

    /* Style Streamlit Radio Buttons as flat vertical menu items */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        gap: 4px !important;
        padding-top: 10px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 6px 0px !important;
        transition: color 0.2s ease-in-out !important;
        cursor: pointer !important;
        width: 100% !important;
        color: #8E9AA8 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        box-shadow: none !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label p {
        white-space: nowrap !important;
        margin: 0 !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        display: inline-block !important;
    }

    /* Hover Style */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover p {
        color: #FFFFFF !important;
    }

    /* Selected Option Style */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] {
        background: transparent !important;
        border: none !important;
        color: #3B82F6 !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #3B82F6 !important;
        font-weight: 700 !important;
    }
    
    /* Prepend arrow to active item */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] p::before {
        content: "> " !important;
        color: #3B82F6 !important;
        font-weight: 700 !important;
    }
    
    /* Hide default radio circle indicator */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label [role="presentation"] {
        display: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[class*="StyledRadio"] {
        display: none !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label div[data-testid="stRadioCircle"] {
        display: none !important;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1E1E1E;
        border: 1px solid #333;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Custom divider */
    hr {
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(59, 130, 246, 0), rgba(59, 130, 246, 0.5), rgba(59, 130, 246, 0));
        margin: 40px 0;
    }
    </style>
    """
