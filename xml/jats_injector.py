import xml.etree.ElementTree as ET

journal = "Journal of Communication"
doi = "10.1371/journal.pone.0268038"
title = "25-hydroxyvitamin D is a predictor of COVID-19 severity of hospitalized patients"

authors = [
    {
    "last_name": "Mohamed",
    "given_name": "Nada A.",
    "title": "",
    "affiliation": "Department of Linguistics and Basque Studies, Universidad del País Vasco/Euskal Herriko Unibertsitatea (UPV/EHU), Vitoria-Gasteiz, Spain",
    "orcid": "https://orcid.org/0000-0002-6232-7530",
    "role": [""]
    },
    {
        "last_name": "Chan",
        "given_name": "Chung-hong",
        "title": "",
        "affiliation": "Universität Wien, Vienna, Austria",
        "orcid": "",
        "role": [""]
    }]

unique_affiliations = list(set([author["affiliation"] for author in authors]))
unique_affiliations.sort()

affiliation_ids = list(range(0, len(unique_affiliations)))

def gen_author_node(last_name, given_name, orcid):
    x = ET.Element("contrib", {"contrib-type": "author", "xlink:type": "simple"})
    if orcid:
        contribid_tag = ET.SubElement(x, "contrib-id", {"authenticated": "true", "contrib-id-type": "orcid"})
        contribid_tag.text = orcid
    name_tag = ET.SubElement(x, "name", {"name-style": "western"})
    surname_tag = ET.SubElement(name_tag, "surname")
    surname_tag.text = last_name
    given_names_tag = ET.SubElement(name_tag, "given-names")
    given_names_tag.text = given_name
    return(x)


root_node = ET.Element("article",attrib = {"article-type": "research-article", "dtd-version": "1.1d3", "xml:lang": "en"})

# Front matter
front_node = ET.SubElement(root_node, "front")

# front > journal meta
journalmeta_node = ET.SubElement(front_node, "journal-meta")

# populate Journal Title

jid_nlmta_node = ET.SubElement(journalmeta_node, "journal-id", attrib = {"journal-id-type": "nlm-ta"})
jid_nlmta_node.text = journal
journaltitlegroup_node = ET.SubElement(journalmeta_node, "journal-title-group")
journaltitle_node = ET.SubElement(journaltitlegroup_node, "journal-title")
journaltitle_node.text = journal

# front > article_meta

articlemeta_node  = ET.SubElement(front_node, "article-meta")

# DOI: front > article_meta > article-id

aid_node = ET.SubElement(articlemeta_node, "article-id", attrib = {"pub-id-type": "doi"})
aid_node.text = doi

# title: front > article_meta > title-group > article-title
title_group_node = ET.SubElement(articlemeta_node, "title-group")
article_title_node = ET.SubElement(title_group_node, "article-title")
article_title_node.text = title

# authors: front > article_meta > contrib-group
contrib_group_node = ET.SubElement(articlemeta_node, "contrib-group")

for author in authors:
    contrib_group_node.append(gen_author_node(author["last_name"], author["given_name"], author["orcid"]))
