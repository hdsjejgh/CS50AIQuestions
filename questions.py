import nltk
from nltk.corpus import stopwords
import sys
import os
from string import ascii_lowercase
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)

    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    d = {}

    for file in os.listdir(directory):
        path = os.path.join(directory,file)
        with open(path,"r", encoding="utf8") as f:
            text = f.read()
            d[file] = text
    return d
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    s= [char for char in document.lower() if char in ascii_lowercase+' ']
    s = (''.join(s)).split()

    s = [word for word in s if not word in stopwords.words('english')]

    return s
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    d = {}
    for doc in documents.values():
        for word in doc:
            if not word in d.keys():
                s = 0
                for doc2 in documents.values():
                    s += 1 if word in doc2 else 0
                d[word] = log(len(documents.values())/s)
    return d
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    query=set(query)
    top = {}
    for file in files:
        s=0
        for word in query:
            s+=idfs.get(word,0) if word in files[file] else 0
        top[file] = s
    items = list(top.items())
    items.sort(key=lambda x:x[1],reverse=True)
    return [i[0] for i in items[0:n]]

    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    query = set(query)
    top = {}
    density = {}
    for sentence in sentences:
        s = 0
        for word in query:
            s += idfs.get(word, 0) if word in sentences[sentence] else 0
        top[sentence] = s

        density[sentence] = len([i for i in sentences[sentence] if i in query])/len(sentences[sentence])
    sent = list(sentences.keys())
    sent.sort(key=lambda x:(top[x],density[x]),reverse=True)

    return sent[0:n]

    #raise NotImplementedError


if __name__ == "__main__":
    main()
