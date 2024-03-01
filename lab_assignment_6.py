import matplotlib.pyplot as plt
import random

class DataGenerator:
    def __init__(self):
        self.data = []
        
    def _generate_random_value(self):
        return random.uniform(0, 1)
    

    @property
    def random_value(self):
        value = self._generate_random_value()
        if len(self.data) < 2:
            self.data.append(value)
        else:
            m = max(self.data) - min(self.data)
            c = min(self.data)
            value = m * value + c
            self.data.append(value)
        print(f'Generated value: {value}')
        
    
    def plot_data(self):
        plt.plot(self.data, 'r-')
        plt.title('Random Numbers')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.show()


if __name__ == "__main__":
    rng = DataGenerator()
    for i in range(10):
        rng.random_value
    rng.plot_data()


