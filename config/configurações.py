from dotenv import load_dotenv
import os 
load_dotenv()
class conf_priv:
    STK = os.getenv("STK")
    URL = os.getenv("URL_DATABASE")
    ALGORITHM = os.getenv("ALGORITIMO")