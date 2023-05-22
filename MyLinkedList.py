class Element:
    def __init__(self, data=None, nextE=None):
        self.data = data
        self.nextE = nextE


class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        result = ""
        current = self.head
        while current is not None:
            result += str(current.data) + " -> "
            current = current.nextE
        result += "None"
        return result

    def get(self, e):
        current = self.head
        while current is not None:
            if current.data == e:
                return current
            current = current.nextE
        return None

    def delete(self, e):
        current = self.head
        previous = None
        while current is not None:
            if current.data == e:
                if previous is not None:
                    previous.nextE = current.nextE
                else:
                    self.head = current.nextE
                if current.nextE is None:
                    self.tail = previous
                self.size -= 1
                return
            previous = current
            current = current.nextE

    def append(self, e, func=None):
        new_element = Element(e)

        if self.head is None:
            self.head = new_element
            self.tail = new_element
            self.size += 1
        elif func is None:
            if self.tail.data <= e:
                self.tail.nextE = new_element
                self.tail = new_element
                self.size += 1
            elif self.head.data >= e:
                new_element.nextE = self.head
                self.head = new_element
                self.size += 1
            else:
                current = self.head
                previous = None
                while current is not None:
                    if current.data >= e:
                        previous.nextE = new_element
                        new_element.nextE = current
                        self.size += 1
                        return
                    previous = current
                    current = current.nextE
        else:
            current = self.head
            previous = None
            while current is not None:
                if func(current.data, e):
                    if previous is not None:
                        previous.nextE = new_element
                    else:
                        self.head = new_element
                    new_element.nextE = current
                    self.size += 1
                    return
                previous = current
                current = current.nextE
            self.tail.nextE = new_element
            self.tail = new_element
            self.size += 1


if __name__ == "__main__":
    ll = MyLinkedList()
    ll.append(2)
    ll.append(4)
    ll.append(6)
    ll.append(1)

    ll.delete(4)

    print("Linked list: " + str(ll))
