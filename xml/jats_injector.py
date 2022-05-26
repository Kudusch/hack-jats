import xml.etree.ElementTree as ET
import json

# journal = "Journal of Communication"
# doi = "10.1371/journal.pone.0268038"
# title = "25-hydroxyvitamin D is a predictor of COVID-19 severity of hospitalized patients"

# authors = [
#     {
#     "last_name": "Mohamed",
#     "given_name": "Nada A.",
#     "title": "",
#     "affiliation": "Department of Linguistics and Basque Studies, Universidad del País Vasco/Euskal Herriko Unibertsitatea (UPV/EHU), Vitoria-Gasteiz, Spain",
#     "orcid": "https://orcid.org/0000-0002-6232-7530",
#     "role": [""]
#     },
#     {
#         "last_name": "Chan",
#         "given_name": "Chung-hong",
#         "title": "",
#         "affiliation": "Universität Wien, Vienna, Austria",
#         "orcid": "",
#         "role": [""]
#     }]

# abstract = "this is a stupid article. Don't read it."

def gen_affiliation_dict(authors):
    unique_affiliations = list(set([author["affiliation"] for author in authors]))
    unique_affiliations.sort()
    affiliation_ids = list(range(0, len(unique_affiliations)))
    aff_dict = dict()
    for aid, aff in zip(affiliation_ids, unique_affiliations):
        aff_dict[aff] = (aid + 1, 'aff' + '{:0>3}'.format(aid + 1))
    return(aff_dict)
    
def gen_author_node(last_name, given_name, orcid, affiliation, aff_dict):
    """generate a html node based on author info"""
    ##    x = ET.Element("contrib", {"contrib-type": "author", "xlink:type": "simple"})
    x = ET.Element("contrib", {"contrib-type": "author"})
    if orcid:
        contribid_tag = ET.SubElement(x, "contrib-id", {"authenticated": "true", "contrib-id-type": "orcid"})
        contribid_tag.text = orcid
    name_tag = ET.SubElement(x, "name", {"name-style": "western"})
    surname_tag = ET.SubElement(name_tag, "surname")
    surname_tag.text = last_name
    given_names_tag = ET.SubElement(name_tag, "given-names")
    given_names_tag.text = given_name
    aff_info = aff_dict[affiliation]
    xref = ET.SubElement(x, "xref", {"ref-type": "aff", "rid": aff_info[1]})
    sup = ET.SubElement(xref, "sup")
    sup.text = str(aff_info[0])
    return(x)

def gen_front_node(authors, journal, doi, title, abstract):
    aff_dict = gen_affiliation_dict(authors)
    front_node = ET.Element("front")
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
        contrib_group_node.append(gen_author_node(author["last_name"], author["given_name"], author["orcid"], author["affiliation"], aff_dict))
    for aff_key in aff_dict:
        aff_info = aff_dict[aff_key]
        aff_node = ET.SubElement(articlemeta_node, "aff", {"id": aff_info[1]})
        label_node = ET.SubElement(aff_node, "label")
        label_node.text = str(aff_info[0])
        addr_node = ET.SubElement(aff_node, "addr-line")
        addr_node.text = aff_key
    abstract_node = ET.SubElement(articlemeta_node, "abstract")
    _ = ET.SubElement(abstract_node, "p")
    _.text = abstract
    return(front_node)

def gen_body_node(text):
    """text should be a list of sections"""
    cur_section_id = 1
    body_node = ET.Element("body")
    for section in text:
        par = {"id": '{:0>3}'.format(cur_section_id)}
        if cur_section_id == 1:
            par['sec-type'] = "intro"
        sec_node = ET.SubElement(body_node, "sec", par)
        title_node = ET.SubElement(sec_node, "title")
        title_node.text = section['sec_title']
        _ = ET.SubElement(sec_node, "p")
        _.text = section['sec_content']
        cur_section_id = cur_section_id + 1
    return(body_node)

def convert_jats(data):
    root_node = ET.Element("article",attrib = {"article-type": "research-article", "dtd-version": "1.1d3"})
    front_node = gen_front_node(data['authors'], data['journal'][0], data['doi'], data['title'], data['abstract'])
    body_node = gen_body_node(data['text'])
    root_node.append(front_node)
    root_node.append(body_node)
    return(ET.tostring(root_node).decode('utf-8'))
    
