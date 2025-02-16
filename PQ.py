import heapq
import logging

class PQ:
    def __init__(self):
        self.heap = []
        self.count = 0
        self.entry_finder = {}
        self.REMOVED = '<removed-task>' 
        self.log_filename = "queue_log.txt"

        open(self.log_filename, "w").close()

        logging.basicConfig(
            filename=self.log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

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

    def log_queue(self):
        queue_elements = {entry[2] for entry in self.heap if entry[2] != self.REMOVED}
        
        with open(self.log_filename, "a") as log_file:
            log_file.write(f"Current Queue Set: {queue_elements}\n")
        
        logging.info(f"Priority queue contents logged as set: {queue_elements}")