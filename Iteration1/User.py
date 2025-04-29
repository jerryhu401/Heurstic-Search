
def checkStop(frontier):
    return frontier.queue.priority.valid()

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
    
    frontier.queue.priority.update()

def checkStopMulti(frontier):
    return frontier.anchor.queue.priority.valid() and all(f.queue.priority.valid() for f in frontier.inads)

def updateMulti(frontier):
    frontier.picker.update()
    updateGeneric(frontier.anchor)
    for F in frontier.inads:
        updateGeneric(F)
    frontier.picker.update()