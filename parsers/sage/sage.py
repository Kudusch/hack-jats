import json
import re
import typing

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

EXAMPLE_ARTICLE_URL = "https://journals.sagepub.com/doi/full/10.1177/10776990211049460"

"""
Extract a paper's text and return it in the form of an array of sections
"""
def scrape_full_text(soup: BeautifulSoup) -> typing.List[typing.Dict]:
    sections = []
    full_text_elem = soup.find("div", class_="hlFld-Fulltext")
    for child in full_text_elem.children:
        if child.name == "p":
            sections.append({"sec_title": "", "sec_content": child.text})
        elif child.name == "div":
            if child.find(class_="sectionHeading") is None:
                continue
            section_title = child.find(class_="sectionHeading").text
            if "section" not in section_title: continue
            section_body = "\n".join([paragraph for paragraph in child.find_all("p")])
            sections.append({"sec_title": section_title, "sec_content": section_body})
    return sections

"""
Naively parses a first and family name from a full name string. 
"""
def extract_given_and_last_name(full_name: str) -> typing.Dict[str, str]:
    last_name = ""
    given_name = ""
    if "," in full_name:
        last_name, given_name = full_name.split(",")  # refine
        given_name, last_name = given_name.strip(), last_name.strip()
    return {"full_name": full_name, "given_name": given_name, "last_name": last_name}

"""
Given a paper citation string, return the associated authors
"""
def parse_authors_from_citation_text(citation_text: str) -> typing.List[typing.Dict]:
    should_parse_name = False
    ref_authors = []
    num_commas = 0
    prev_comma_index = 0

    for ind, ch in enumerate(citation_text):  # Iterate by characters
        if ind == len(citation_text) - 1:  # If we get to the last character, assume we've just seen a full author name
            should_parse_name = True
        elif ch == ",": 
            num_commas += 1

            # After every second comma, assume we've seen a full name
            # Citation author list looks like: "De Coninck, D., d’Haenens, L., Matthijs, K."
            # First names are separated from family names with commas. Contributors are separated from other contributers with commas
            if num_commas % 2 == 0 and num_commas > 0: 
                should_parse_name = True

        if should_parse_name: # if we've seen a full name
            print(citation_text, prev_comma_index, ind+1)
            full_name = citation_text[prev_comma_index:ind+1].strip("(, \n)") #  strip new lines, spaces, commas, parentheses
            name_dict = extract_given_and_last_name(full_name)  # Split the name into first/last names
            prev_comma_index = ind+1  # advance string pointer
            ref_authors.append(name_dict)
            should_parse_name = False
    return ref_authors


"""
Helper method to access attributes from a DOI page's meta tags
"""
def grab_elements_content_from_attrs(soup, **kwargs) -> typing.List[str]:
    match_elements = soup.find_all(attrs=kwargs) 
    return [elem["content"] for elem in match_elements]


"""
Scrape the current papers' bibliography
"""
def get_references(soup: BeautifulSoup) -> typing.List[typing.Dict]:
    references = []
    references_elem = soup.find("table", class_="references")
    for ref in references_elem.contents:

        # Some reference attributes
        ref_authors = []
        ref_year = None
        ref_doi = None
        ref_journal = None
        ref_publication = None
        ref_title = ""
        reference_dict = {"authors": [], 
                          "year": None, 
                          "title": "",
                          "doi": "", 
                          "journal": ""}
        
        # For each reference, grab the element containing citation text
        ref_details = ref.find("td", attrs={"valign": "top"})

        # For each element (or chunk of text) in the citation
        for ind, elem in enumerate(ref_details.contents):
            if ind == 0: # The first element should always be the author name
                ref_authors = parse_authors_from_citation_text(elem.text) # Split the name into given/last names if possible
                reference_dict.update({"authors": ref_authors})
                continue

            # Don't process plaintext elements  or elements that don't have a class attribute
            # They contain information we need, but their order isn't standardized. 
            # We'll need more time to develop a method to extract data from them. 
            if not isinstance(elem, Tag) or not elem.get("class"):  
               continue

            if elem.get("class")[0] == "NLM_article-title":  # Paper title element
                ref_title = elem.text.strip(" ()")  # clean title string
                reference_dict.update({"title": ref_title})

            elif elem.get("class")[0] == "NLM_year": # publication year element
                ref_year = elem.text
                reference_dict.update({"year": ref_year})

            elif elem.get("class")[0] == "ext-link" and "doi" in elem.text: # DOI element
                ref_doi = elem.text
                reference_dict.update({"doi": ref_doi})

        references.append(reference_dict)
    return references

"""
Fetch the paper from Sage and assemble its attributes into a reference_dict
"""
def parse_paper(url: str) -> typing.Dict:
    # Article text is loaded asynchronously. For now, we'll just read the page source from a string
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, 'html.parser')

    with open("example.html", "r") as infile:
        paper_html_source = infile.read()
    soup = BeautifulSoup(paper_html_source)

    paper = {}

    paper["title"] = grab_elements_content_from_attrs(soup, name="dc.Title")[0]
    paper["authors"] = grab_elements_content_from_attrs(soup, name="dc.Creator")
    paper["journal"] = grab_elements_content_from_attrs(soup, name="citation_journal_title")[0]
    paper["keywords"] = grab_elements_content_from_attrs(soup, name="keywords")[0].split(",")
    paper["doi"] = grab_elements_content_from_attrs(soup, name="dc.Identifier", scheme="doi")[0]
    paper["text"] = scrape_full_text(soup)
    paper["abstract"] = soup.find("div", attrs={"class": "abstractSection"}).text
    paper["references"] = get_references(soup)
    return paper

def main():
    paper = parse_paper("https://journals.sagepub.com/doi/full/10.1177/10776990211049460")
    print(json.dumps(paper, indent=2))

if __name__ == "__main__":
    main()

