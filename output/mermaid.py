from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from pathlib import Path
from utils.logging import logger
from colorama import Fore, Style

data_flow_ops = ['INSERT', 'REPLACE', 'UPDATE', 'CREATE TABLE QUERY']


class Mermaid:

    def __init__(self, results: List[Dict]):

        self.graph_type = "graph LR; \nlinkStyle default interpolate basis\n"
        self.tables_flow = []
        self.functions_flow = []
        self.input = results
        self.output = ''
        with open(f'{Path(__file__).parent}/resources/template.html', 'r') as template:
            self.soup = BeautifulSoup(template.read(), features="html.parser")

    def arrow(self, statement: Dict, statement_part: str) -> None:

        """
        Generate Markdown code representing mermaid.js arrows and adds them to results

        :param statement: statement dictionary
        :param statement_part: statement key to get tables from, should be
        from_table or join_table.
        """

        if statement.get(statement_part):
            for table in statement.get(statement_part):

                arrow = f"{table['schema']}.{table['name']}" \
                        f"-->|{statement['procedure']}|" \
                        f"{statement['target_table']['schema']}" \
                        f".{statement['target_table']['name']};"

                # If arrow not already existing, add it to the chart
                if arrow not in self.tables_flow:
                    self.tables_flow.append(arrow)

    def tables_chart(self, path: Optional[str]) -> BeautifulSoup:

        """
        Creates HTML flowchart file (using mermaid.js) representing tables data flows
        and saves it at specified path.

        :param path: output HTML file destination
        """

        try:

            # Creating mermaid markdown arrows' list
            for p in self.input:
                # For all statements in parsed procedure/file
                for s in p['statements']:
                    if s['operation'] in data_flow_ops:
                        self.arrow(s, 'from_table')
                        self.arrow(s, 'join_table')

            # Generate markdown string from the list of arrows
            self.tables_flow.insert(0, self.graph_type)
            self.output = '\n'.join(self.tables_flow)

            # Update <div class="mermaid"> in HTML template code with our Mermaid markdown
            mermaid = self.soup.find("div", {"class": "mermaid"})
            chart = self.soup.new_tag("div")
            chart.attrs["class"] = "mermaid"
            chart.string = self.output
            mermaid.replace_with(chart)

            if path:
                # Save HTML file at specified path
                with open(path, 'w') as outfile:
                    outfile.write(str(self.soup))

            print(f'{Fore.GREEN}{path} successfully saved{Style.RESET_ALL}')

        except Exception as e:
            logger.error(f'{Fore.RED}Could not save HTML chart at {path}{Style.RESET_ALL}')

        return self.soup
