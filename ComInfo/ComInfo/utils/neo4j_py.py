# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-11-5 下午5:02

from py2neo import Graph,Node,Relationship

# test_graph = Graph(
#     "http://xxxxxx:7474",
#     username="neo4j",
#     password="xxxxxx"
# )
#
#
# test_node_1 = Node(name="test_node_1")
# test_node_2 = Node(name="test_node_2")
# test_graph.create(test_node_1)
# test_graph.create(test_node_2)
#
# node_1_call_node_2 = Relationship(test_node_1,'CALL',test_node_2)
# node_1_call_node_2['count'] = 1
# node_2_call_node_1 = Relationship(test_node_2,'CALL',test_node_1)
# node_2_call_node_1['count'] = 2
# test_graph.create(node_1_call_node_2)
# test_graph.create(node_2_call_node_1)



# a = Node('Person', name='Alice')
# b = Node('Person', name='Bob')
# r = Relationship(a, 'KNOWS', b)
# print(a, b, r)


graph = Graph("http://xxxxxx:7474",username="neo4j",password="xxxxxx")
tx = graph.begin()

worker_1 = {"name":'Alice'}
worker_2 = {"name":'ccjjj'}
node_1 = Node("Person",**worker_1)
node_2 = Node("Person",**worker_2)
rel_1_2 = Relationship(node_1,"KNOWS",node_2)
tx.merge(node_1)
tx.merge(node_2)
tx.merge(rel_1_2)
tx.commit()
