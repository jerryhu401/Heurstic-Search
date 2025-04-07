
def checkStop(frontier):
    return frontier.priority.valid()

def updateGeneric(frontier):
    open = []
    for p,node in frontier.queue.heap:
        open.append(node)
    incons = frontier.DC.get_incons()
    new_open = open + incons
    frontier.queue.clear()
    frontier.DC.clear()
    
    for node in new_open:
        frontier.insert(node)
    
    frontier.priority.update()