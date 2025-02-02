from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
import os
import psycopg2
from typing import Dict, List
import urllib.parse


load_dotenv()
mcp = FastMCP("LSD", dependencies=["psycopg2-binary"])
conn = psycopg2.connect(
    host="lsd.so",
    database=os.environ.get("LSD_USER"),
    user=os.environ.get("LSD_USER"),
    password=os.environ.get("LSD_API_KEY"),
    port="5432",
)

shared_docs = False

@mcp.tool()
def run_lsd(lsd_sql_code: str) -> List[List[str]]:
    """Runs LSD SQL using user credentials in .env"""
    with conn.cursor() as curs:
        curs.execute(lsd_sql_code)
        rows = curs.fetchall()
        return [list(r) for r in rows]

@mcp.tool()
async def view_lsd(lsd_sql_code: str) -> str:
    """"Returns a URL to a page where the user can view results as well as a visual playback of LSD SQL evaluation"""
    return f"https://lsd.so/view?query={urllib.parse.quote_plus(lsd_sql_code)}"

@mcp.resource("lsd://docs")
def fetch_lsd_docs() -> List[Dict[str, str]]:
    with conn.cursor() as curs:
        curs.execute("SCAN https://lsd.so/docs")
        rows = curs.fetchall()
        return [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]

@mcp.prompt()
def write_lsd_sql(objective: str) -> str:
    global shared_docs

    if not shared_docs:
        # Programmatically inserting docs to context
        with conn.cursor() as curs:
            curs.execute("SCAN https://lsd.so/docs")
            rows = curs.fetchall()
            lsd_docs = [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]
        shared_docs = True

        return f"""Here is documentation for a custom SQL language called LSD in a JSON list of objects where one has a MARKDOWN property with the markdown content of the page and a URL property with the URL of the page it belongs to. {lsd_docs} You may run LSD SQL along the way to obtain HTML or MARKDOWN in order to answer user inquiries. Using the keywords, {objective}"""

    return f"""You may run LSD SQL along the way to obtain HTML or MARKDOWN in order to answer user inquiries. Using the keywords, {objective}"""

@mcp.prompt()
async def write_and_run_lsd_sql(objective: str) -> str:
    global shared_docs

    if not shared_docs:
        # Programmatically inserting docs to context
        with conn.cursor() as curs:
            curs.execute("SCAN https://lsd.so/docs")
            rows = curs.fetchall()
            lsd_docs = [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]
        shared_docs = True

        return f"""Here is documentation for a custom SQL language called LSD in a JSON list of objects where one has a MARKDOWN property with the markdown content of the page and a URL property with the URL of the page it belongs to. {lsd_docs} You may run LSD SQL along the way to obtain HTML or MARKDOWN in order to answer user inquiries. Using the keywords, {objective}. When done run the LSD SQL statement and present the results to the user"""

    return f"""You may run LSD SQL along the way to obtain HTML or MARKDOWN in order to answer user inquiries. Using the keywords, {objective}"""
