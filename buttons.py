# buttons

def ButtonEx():
    documents = collection.find()
    for document in documents:
        print(document.author)