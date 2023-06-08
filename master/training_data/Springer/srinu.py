import re
def remove_special_characters_between_quotes(text):
    pattern = r'\"(.*?)\"'  # Matches anything between double quotes
    result = re.sub(pattern, lambda x: re.sub(r'[^\w\s]', '', x.group(1)), text)
    return result

def join_quotes_with_commas(text):
    quotes = re.findall(r'\"(.*?)\"', text)  # Extracts text between double quotes
    result = '", "'.join(quotes)
    return f'"{result}"'

# Read text from file
filename = 'n.csv'
with open(filename, 'r',encoding='utf-8') as file:
    text = file.read()

# Process the text
clean_text = remove_special_characters_between_quotes(""""NETNOMICS: Economic Research and Electronic Networking","NETNOMICS: Economic Research and Electronic Networking, Economic Theory/Quantitative Economics/Mathematical Methods, Data Structures and Information Theory, IT in Business, Economic Growth, e-Commerce/e-business"," We regret to inform you that   NETNOMICS: Economic Research and Electronic Networking  will not be published by Springer beyond 2021. For this reason, we are no longer receiving submissions for the journal. If you have a paper in peer-review, you will be informed about the next steps. If you are preparing a revision of a former submission, please get in contact with the Editor-in-Chief.   All articles published in the journal during its time with Springer will remain fully searchable through our websites.    The journal Netnomics is intended to be an outlet for research in electronic networking as well as in network economics. As more and more transactions are carried out electronically, important economic issues and problems arise. A network-based real-time macroeconomy has emerged with its own set of economic characteristics, creating a wealth of opportunities for economic research as well as important linkages to information systems. Topics that could be addressed are pricing schemes for electronic services, electronic trading systems, data mining and high-frequency online data as well as big data, real-time forecasting, filtering, economic software agents, distributed database applications, electronic money and tickets, and many more. Evidently, this is only the tip of the iceberg. Moreover, we attempt to disclose important research questions in the field of network economics. This may reflect networks in their widest sense regarding, for instance, telecommunications, electronic networks, supply chain networks, networks in traffic and transportation such as the airline and maritime shipping industries, or even electricity networks and smart grids. Papers of Netnomics describe cutting edge research and applications in these areas. Officially cited as:  Netnomics  Addresses new economic issues and problems that are arising as more and more transactions are conducted electronically  Explores the emerging network-based, real-time macroeconomy with its own set of economic characteristics  Covers such topics as pricing schemes for electronic services, electronic trading systems, data mining and high-frequency data, real-time forecasting, filtering, etc". """)
joined_quotes = join_quotes_with_commas(clean_text)
print(joined_quotes)
