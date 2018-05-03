# Scraping Psychological Science
# input : a psychological science issue's url
# output: a list of published articles in the issue

def CrawlPsychSci(url):
    
    import requests
    from bs4 import BeautifulSoup

    bs_psych = BeautifulSoup(requests.get(url).text, 'html.parser')

    f = open('paper_list.txt', 'w')

    # get abstracts and authors

    dois = bs_psych.find_all('a', {"class": "ref nowrap"})

    for doi in dois:

        article_url = 'http://journals.sagepub.com' + doi['href']
        bs_article = BeautifulSoup(requests.get(article_url).text, 'html.parser')

        temp = bs_article.find_all('meta', {'name': 'dc.Title'})
        if len(temp) > 0:
            title = temp[0]['content']
        else:
            title = ''
        temp = bs_article.find_all('meta', {'name': 'dc.Description'})
        if len(temp) > 0:
            abstract = temp[0]['content']
        else:
            abstract = ''

        a_authors = bs_article.find_all('a', {'class':'entryAuthor'})
        author_list = set()
        for author in a_authors:
            author_list.add(author.text)

        temp = list(author_list)
        author_list = []
        for x in temp:
            if "\r\n" not in x and "See all" not in x:
                author_list.append(x)

        f.write(title + '\n')

        for author in author_list:
            if author == author_list[0]:
                f.write(author[1:] + ',')
            elif author != author_list[-1]:
                f.write(author + ',')
            else:
                f.write(' &'+author[:len(author)-2])
        f.write('\n\n')

        f.write('Abstract\n')
        f.write(abstract + '\n\n')
    f.close()
