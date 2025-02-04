from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
import os
import psycopg2
from typing import Dict, List
import urllib.parse
from time import sleep


load_dotenv()
mcp = FastMCP("LSD", dependencies=["psycopg2-binary"])

LSD_PROMPT = """
Here is documentation for a custom SQL language called LSD in a JSON list of objects where one has a MARKDOWN property with the markdown content of the page and a URL property with the URL of the page it belongs to. {lsd_docs} You may run LSD SQL along the way to obtain HTML or MARKDOWN in order to answer user inquiries. Using the keywords, {objective}.
Here is an example of how to assign variables and run a query:
'''
post_container <| div.details |
post <| a |
domain <| a.domain |
author <| a.u-author.h-card |

FROM https://lobste.rs/
|> GROUP BY post_container
|> SELECT post, domain, author
'''

"""

def establish_connection():
    try:
        return psycopg2.connect(
            host="lsd.so",
            database=os.environ.get("LSD_USER"),
            user=os.environ.get("LSD_USER"),
            password=os.environ.get("LSD_API_KEY"),
            port="5432",
        )
    except Exception as e:
        sleep(1)
        return establish_connection()

@mcp.tool()
def run_lsd(lsd_sql_code: str) -> List[List[str]]:
    """Runs LSD SQL using user credentials in .env"""
    conn = establish_connection()
    with conn.cursor() as curs:
        curs.execute(lsd_sql_code)
        rows = curs.fetchall()
        return [list(r) for r in rows]

@mcp.tool()
def view_lsd(lsd_sql_code: str) -> str:
    """"Returns a URL to a page where the user can view results as well as a visual playback of LSD SQL evaluation"""
    return f"https://lsd.so/view?query={urllib.parse.quote_plus(lsd_sql_code)}"

@mcp.resource("lsd://docs")
def fetch_lsd_docs() -> List[Dict[str, str]]:
    conn = establish_connection()
    with conn.cursor() as curs:
        curs.execute("SCAN https://lsd.so/docs/database/language")
        rows = curs.fetchall()
        return [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]

@mcp.prompt()
def write_lsd_sql(objective: str) -> str:
    # Programmatically inserting docs to context
    conn = establish_connection()
    with conn.cursor() as curs:
        curs.execute("SCAN https://lsd.so/docs/database/language")
        rows = curs.fetchall()
        lsd_docs = [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]

    return LSD_PROMPT.format(lsd_docs=lsd_docs, objective=objective)

@mcp.prompt()
def write_and_run_lsd_sql(objective: str) -> str:
    # Programmatically inserting docs to context
    conn = establish_connection()
    with conn.cursor() as curs:
        curs.execute("SCAN https://lsd.so/docs/database/language")
        rows = curs.fetchall()
        lsd_docs = [{"URL": r[0], "MARKDOWN": r[1]} for r in rows]

    return LSD_PROMPT.format(lsd_docs=lsd_docs, objective=objective) + ". When done, run the LSD SQL trip and present the results to the user"
