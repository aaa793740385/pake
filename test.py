# -*- coding: utf-8 -*-

l = [{'name':'zhang',  'age':18, 'asd':18}, {'name':'zhang', 'age':18, 'asd':18}, {'name':'li', 'age':18, 'asd':18}]
print [dict(t) for t in set([tuple(d.items()) for d in l])]