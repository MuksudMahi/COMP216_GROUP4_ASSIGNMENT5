import matplotlib.pyplot as plt
import random


class DataGenerator(object):
    def __init__(self, x_max=40, x_min=-20):
        self.__max = x_max
        self.__min = x_min
        self.__scale = int(f'1{"0" * len(str(x_min))}')
        self.__base = x_min / self.__scale  # the base value, add or subtract from this
        self.__delta = 0.005  # the change to add or subtract from the above
        self.__cycle = 4  # this is the length of a cycle.

    # # Private method
    # def __generator(self):
    #     self.__cycle -= 1
    #     if self.__cycle == 0:
    #         self.__cycle = random.randint(5, 12)
    #         self.__delta = random.randint(-5, 5) / 1000
    #         # self.__base = random.randint(0, 10) / 10
    #
    #     # Keeping value between 0 and 1
    #     if self.__base + self.__delta < 0 or self.__base + self.__delta > 1:
    #         self.__base = random.randint(0, 10) / 10
    #         return self.__base
    #
    #     self.__base += self.__delta
    #     #print(f'Generated {self.__base}')
    #     return self.__base
    #
    # # Public property
    # @property
    # def val(self):
    #     x = self.__generator() + random.randint(-5, 5) / 1000
    #     return (self.__max - self.__min) * x + self.__min
    # Private method
    def __generator(self):
        return random.random()

    # Public property
    @property
    def val(self):
        x = self.__generator() + random.randint(-5, 5) / 1000
        return (self.__max - self.__min) * self.__generator() + self.__min
        # return self.__generator();


def main():
    # Creating instance and accessing private method through public property
    dataGenerator = DataGenerator()
    y_data = [dataGenerator.val for _ in range(365)]

    # Plotting
    plt.figure(figsize=(20, 5))
    plt.title("Temperature this year")
    plt.xlabel("Days")
    plt.ylabel("Temperature (Celsius)")
    plt.plot(y_data, 'g')
    plt.show()


if __name__ == '__main__':
    main()
