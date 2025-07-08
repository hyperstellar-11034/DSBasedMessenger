'''
class Node:
    def __init__(node, data):
        node.data= data
        node.next= None #not defined yet
'''

class Node: #self is this current instance of Node
    def __init__(self, data):
        self.data= data
        self.next= None #not defined yet
#btw, next points to the one below you

class Stack: #self is this current instance of Stack
    def __init__(self):
        self.top = None #empty stack in the beginning

    def is_empty(self):
        if self.top == None:
           return True
        else:
            return False
    '''
    def is_empty(self):
        return self.top is None
    '''
    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def push(self, data):
        new_node = Node(data)
        new_node.next= self.top
        self.top=new_node
        
    def pop(self):
        if self.is_empty():
            return None
        popped_data = self.top.data
        self.top = self.top.next
        return popped_data
