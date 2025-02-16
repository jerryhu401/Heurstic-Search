import heapq

class PQ:
    def __init__(self):
        self.heap = []
        self.count = 0
        self.entry_finder = {}
        self.REMOVED = '<removed-task>' 

    def peek(self):
        return self.heap[0]

    def isEmpty(self):
        return len(self.heap) == 0

    def push(self, item, priority):
        entry = [priority, self.count, item]
        heapq.heappush(self.heap, entry)
        self.entry_finder[item] = entry
        self.count += 1

    def pop(self):
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        val = self.entry_finder.get(item, 0)
        if val != 0:
            [p, c, i] = val
            if p > priority:
                entry = self.entry_finder.pop(i)
                entry[-1] = self.REMOVED
                PQ.push(self, item, priority)
        else:
            PQ.push(self, item, priority)