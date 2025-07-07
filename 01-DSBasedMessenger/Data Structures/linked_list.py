class Node:
    def __init__(self, reply):
        self.reply = reply 
        self.next = None   

class ReplyList:
    def __init__(self):
        self.head = None  
        self.tail = None  

    def add_reply(self, reply): #to the end of the list
        new_node = Node(reply)
        if not self.head:  # is an empty list
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node    #update to new tail

    def get_all_replies(self): 
        replies = []
        p = self.head #from oldest to newest message
        while p:
            replies.append(p.reply)
            p = p.next
        return replies
