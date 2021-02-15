def author(document):
    if 'author' in document:
        if document['author']:
            document['author'] = document['author'].replace('\n', ' ').replace('\\', '')
        else:
            document['author'] = None
    else:
        document['author'] = None
    return document


def title(document):
    if 'title' in document:
        if document['title']:
            document['title'] = document['title'].replace('\n', ' ').lower()
        else:
            document['title'] = None
    else:
        document['title'] = None
    return document


def unique_id(document):
    if 'unique-id' in document:
        if document['unique-id']:
            document['unique-id'] = document['unique-id'].split(':')[-1]
        else:
            document['unique-id'] = None
    else:
        document['unique-id'] = None
    return document


def doi(document):
    if 'doi' in document:
        if document['doi']:
            document['doi'] = document['doi'].replace('\n', ' ')
        else:
            document['doi'] = None
    else:
        document['doi'] = None
    return document


def journal(document):
    if 'journal' in document:
        if document['journal']:
            document['journal'] = document['journal'].replace('\n', ' ')
        else:
            document['journal'] = None
    else:
        document['journal'] = None
    return document
