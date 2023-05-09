def prepareQuery(query_str):
    ''' process search string for url '''
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    search_term = search_term.replace(' ', '+')
    
    return template.format(search_term)