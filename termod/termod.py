# -*- coding: utf-8
# Рассчетный модуль.
# Позволяет выполнять расчеты по уравнениям Менделеева-Клапейрона и Ван-Дер-Ваальса
#


def check_int(value) ->bool:
    """
    Проверка целого значения
    :param value:
    :return: bool
    """
    return isinstance(value, int)


def check_float(value) ->bool:
    """
    Проверка значения float
    :type value:
    :return: bool
    """
    return isinstance(value, float)


def check_positive(value) -> bool:
    """
    Проверяет, является ли положительным параметр.
    :param value: 
    :return: bool
    """
    if check_float(value) or check_int(value):
        return value > 0
    else:
        return False


class GasLaws(object):
    def __init__(self):
        """
        Рассчетный модуль программы
        :return: GasLaws
        """
        self.R = 8.31
        # Стандартные значения параметров
        self._stpressure = 100000
        self._sttemperature = 298
        self._stvolume = 1
        self._stmoll = 1
        self._sta = 0
        self._stb = 0
        # Текущие значения параметров
        self._pressure = 100000
        self._temperature = 298
        self._volume = 1
        self._moll = 1
        self._a = 0
        self._b = 0
        # Список параметров
        self._params = ("T", "P", "V", "N")
        # выбранная переменная
        self._param = self._params[0]

    @property
    def variable(self):
        """
        Переменная для рассчета в методах MendKlapeiron() и VanDerVaals()
        """
        return self._param

    @variable.setter
    def variable(self, value):
        """
        Выбор переменной для рассчетав методах MendKlapeiron() и VanDerVaals()
        """
        if value in self._params:
            self._param = value
        elif value in range(len(self._params)):
            self._param = self._params[value]

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self,value):
        if check_positive(value):
            self._temperature = value
        elif value is None:
            self._param = "T"

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        if check_positive(value):
            self._pressure = value
        elif value is None:
            self._param = "P"

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if check_positive(value):
            self._volume = value
        elif value is None:
            self._param = "V"

    @property
    def moll(self):
        return self._moll

    @moll.setter
    def moll(self,value):
        if check_positive(value):
            self._moll = value
        elif value is None:
            self._param = "N"

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self,value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self,value):
        self._b = value

    def MendKlapeiron(self):
        """
        Рассчет по уравнению Менделеева-Клапейрона
        :return: float
        """
        res = {"P": self.moll * self.R * self.temperature / self.volume,
               "V": self.moll * self.R * self.temperature / self.pressure,
               "T": self.pressure * self.volume / self.moll / self.R,
               "N": self.pressure * self.volume / self.temperature / self.R}
        return res.get(self.variable)

    def VanDerVaals(self):
        """
        Рассчет по уравнению Ван-Дер-Ваальса
        :return: float
        """
        Vm = self.volume / self.moll
        res = {"P": self.R * self.temperature / (Vm - self.b) - self.a**2 / Vm**2,
               "T": (Vm - self.b) * (self.pressure + self.a**2 / Vm**2) / self.R}
        return res.get(self.variable)

    @property
    def standartpressure(self):
        return self._stpressure

    @property
    def standarttemperature(self):
        return self._sttemperature

    @property
    def standartvolume(self):
        return self._stvolume

    @property
    def standartmoll(self):
        return  self._stmoll

    @property
    def standarta(self):
        return self._sta

    @property
    def standartb(self):
        return self._stb
