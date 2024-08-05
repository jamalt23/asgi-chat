
class Test:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __dict__(self):
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c
        }
    
    def __str__(self) -> str:
        return f'{self.a} {self.b} {self.c}'


print(dict(Test(1, 2, 3).__dict__()))


