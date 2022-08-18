#! /usr/bin/env python3

class ArithmeticSequenceIterator:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __next__(self):
        if (self.end is not None) and ((self.start - self.end) * self.step >= 0):
            raise StopIteration # went past the end
        self.start += self.step
        return self.start - self.step


class ArithmeticSequenceIterable:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        return ArithmeticSequenceIterator(self.start, self.end, step=self.step)

class LazyListIterator:
    def __next__(self):
        raise StopIteration

class LazyList:
    def __init__(self, func):
        self.func = func

    def __iter__(self):
        return self.func()

    def take(self, num):
        value = []
        iterator = iter(self)

        if num is None:
            while(True):
                try:
                    value.append(next(iterator))
                except StopIteration:
                    break
        else:
            for i in range(num):
                try:
                    value.append(next(iterator))
                except StopIteration:
                    break

        return value


def lazyMapIterator(f, lazylistIterator):
    # helper function to create a new lazy list iterator of f applied to each element of lazylist

    class mapIterator:
        def __init__(self, f, lazylistIterator):
            self.f = f
            self.lazylistIterator = lazylistIterator

        def __next__(self):
            try:
                element = next(self.lazylistIterator)
            except StopIteration:
                raise StopIteration
            return self.f(element)

    return mapIterator(f, lazylistIterator)

def lazyMap(f, lazylist):
    return LazyList(lambda : lazyMapIterator(f, iter(lazylist)))


def square(x):
    return x * x

#my_iterable = ArithmeticSequenceIterable(1, 10)
my_iterable = lazyMap(square, LazyList(lambda : ArithmeticSequenceIterator(1, 10)))

print(my_iterable.take(10))


