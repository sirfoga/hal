# !/usr/bin/python3
# coding: utf-8

""" Various utilities to deal with MondoDB databases """

from pymongo import MongoClient


class DbBrowser:
    def __init__(self, db_name):
        """
        :param db_name:
        """

        self.client = MongoClient()
        self.db = self.client[db_name]

    def get_documents_count(self):
        """
        :param db_name: str
            Name of db
        :return: int
            Number of documents in db
        """

        client = MongoClient()  # mongodb client
        database = client[db_name]  # db to scan
        db_collections = [
            database[c] for c in database.collection_names()
        ]  # list of all collections in database
        return sum([c.count() for c in db_collections])  # sum


def get_documents_in_collection(db_name, collection_name, with_id=True):
    """
    :param db_name: str
        Name of db
    :param collection_name: str
        Name of collection
    :param with_id: bool
        True iff each document should also come with its id
    :return: [] of {}
        List of documents in collection in database
    """

    client = MongoClient()  # mongodb client
    database = client[db_name]  # db to scan
    documents_iterator = database[collection_name].find()
    documents = [
        d for d in documents_iterator
    ]  # list of all documents in collection in database

    if not with_id:
        for doc in documents:
            doc.pop("_id")  # remove id key

    client.close()
    return documents


def get_documents_in_database(db_name, with_id=True):
    """
    :param db_name: str
        Name of db
    :param with_id: bool
        True iff each document should also come with its id
    :return: [] of {}
        List of documents in collection in database
    """

    documents = []
    client = MongoClient()  # mongodb client
    database = client[db_name]  # db to scan
    for coll in database.collection_names():
        documents += get_documents_in_collection(
            db_name,
            coll,
            with_id=with_id
        )

    client.close()
    return documents