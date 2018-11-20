# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-11-5 下午4:38

from neo4j.v1 import GraphDatabase

def following(tx, name1, name2):
    tx.run("MERGE (a:Person {name: $name1})"

           "MERGE(c:Person{name:$name2})"

           "CREATE UNIQUE (a)-[:following]->(c)", name1=name1, name2=name2)


driver = GraphDatabase.driver("bolt://xxxxxx:7687", auth=("neo4j", "xxxxxx"))

with driver.session() as session:
    session.write_transaction(following, "xxxxxx", "xxxxxx")
