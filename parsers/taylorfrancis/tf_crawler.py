#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import bibtexparser
from bibtexparser.bparser import BibTexParser
import datetime
import requests
import sys
import json
import re
from nameparser import HumanName

def get_heading(el):
    for i in range(1, 7):
        h = el.find(f"h{i}")
        if h:
            return(h.text)
    return("")

def parse_bib(doi):
    u = "https://www.tandfonline.com/action/downloadCitation"
    data = {"doi":doi, "downloadFileName":"tandf_rjos2018_1470", "format":"bibtex", "include":"ref", "direct":"true"}
    cookies = {"timezone":"60"}
    try:
        r = requests.post(url=u, data=data, cookies=cookies)
    except Exception as e:
        print(e)
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False
    bib_article = bibtexparser.loads(r.content, parser).entries[0]
    refs = get_references(r.text)
    return(bib_article, refs)

def get_references(bib_string):
    refs_dicts = []
    regex = r"@article {(.*?)}\n\n"
    matches = re.finditer(regex, bib_string, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    for i, m in enumerate(matches):
        year = re.findall(r"year = {(.*?)}", m.group(0), re.IGNORECASE)
        title = re.findall(r"title = {(.*?)}", m.group(0), re.IGNORECASE)
        journal = re.findall(r"journal = {(.*?)}", m.group(0), re.IGNORECASE)
        volume = re.findall(r"volume = {(.*?)}", m.group(0), re.IGNORECASE)
        authors = [HumanName(author) for author in re.findall(r"author = {(.*?)}", m.group(0), re.IGNORECASE)]
        authors = [{"name":str(author), "first_name":author.first, "last_name":author.last} for author in authors]
        refs_dicts.append({
            "title":title[0],
            "year":year[0],
            "journal":journal[0],
            "volume":volume[0],
            "authors":authors
        })
    return(refs_dicts)


def get_authors(doi):
    auths = []
    u = "https://www.tandfonline.com/action/downloadCitation"
    data = {"doi":doi, "downloadFileName":"tandf_rjos2018_1470", "format":"ris", "include":"abs", "direct":"true"}
    cookies = {"timezone":"60"}
    try:
        r = requests.post(url=u, data=data, cookies=cookies)
    except Exception as e:
        print(e)

    regex = r"AU\s*-\s(.*?)\n"
    matches = re.finditer(regex, r.text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    for m in matches:
        try:
            name = HumanName(m.group(1))
            auths.append({"last_name":name.last, "first_name":name.first, "name":str(name).strip()})
        except:
            auths.append({"last_name":"", "first_name":"", "name":m.group(1).strip()})
        # try:
        #     last_name, first_name = [n.strip() for n in m.group(1).split(", ")]
        # except:
        #     last_name, first_name = ["", ""]

    return(auths)

def download_article(doi, file = ""):
    parsed_article = {}
    
    authors = get_authors(doi)
    parsed_bib, refs = parse_bib(doi)

    parsed_article["doi"] = doi
    parsed_article["url"] = parsed_bib["url"].strip()
    parsed_article["title"] = parsed_bib["title"].strip()
    parsed_article["volume"] = parsed_bib["volume"].strip()
    parsed_article["year"] = parsed_bib["year"].strip()
    parsed_article["issue"] = parsed_bib["number"].strip()
    parsed_article["journal_name"] = parsed_bib["journal"].strip()
    parsed_article["publisher"] = parsed_bib["publisher"].strip()
    parsed_article["authors"] = authors

    u = f"https://www.tandfonline.com/doi/full/{doi}"
    r = requests.get(url=u)
    s = BeautifulSoup(r.text, "html.parser")
    keywords = s.find("div", {"class":"abstractKeywords"})
    keywords = [a.text for a in keywords.find_all("a")]

    abstract = s.find("div", {"class":"abstractInFull"}).text
    parsed_article["abstract"] = abstract

    full_text = s.find("div", {"class":"hlFld-Fulltext"})
    sections_raw = [sec for sec in full_text.find_all("div", {"class":"NLM_sec_level_1"})]

    sections_parsed = []

    for n, sec in enumerate(sections_raw):
        h = get_heading(sec)
        sections_parsed.append({"title": h, "paragraphs":[p.text for p in sec.find_all("p")]})

    parsed_article["body"] = sections_parsed

    parsed_article["references"] = refs

    if file:
        with open(file, "w") as f:
            json.dump(parsed_article, f)
    return(parsed_article)