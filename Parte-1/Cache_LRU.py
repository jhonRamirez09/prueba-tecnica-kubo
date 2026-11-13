class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} 
        
        # Nodos ficticios
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Elimina un nodo de la lista doblemente enlazada."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        """Inserta un nodo justo después de la cabeza (lo marca como más recientemente usado)."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)    

lru = LRUCache(2)

lru.put(1, 1) # caché es {1=1}
lru.put(2, 2) # caché es {1=1, 2=2}
print(lru.get(1))    # devuelve 1 (el 1 pasa a ser el más recientemente usado)
lru.put(3, 3) # evapora la clave 2 porque alcanzó la capacidad, caché es {1=1, 3=3}
print(lru.get(2))    # devuelve -1 (no encontrado)
lru.put(4, 4) # evapora la clave 1, caché es {3=3, 4=4}
print(lru.get(1))    # devuelve -1
print(lru.get(3))    # devuelve 3
print(lru.get(4))    # devuelve 4