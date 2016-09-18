# -*- coding: utf-8
# Главный модуль программы для рассчета по уравнениям состояния газа

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from termod import termod


class MyWindow (QtWidgets.QMainWindow):
    def __init__(self,parent= None):
        """
        Инициализация главного окна программы
        :rtype: MyWindow
        :param parent:
        """
        QtWidgets.QMainWindow.__init__(self,parent)
        self.window = uic.loadUi("termod\\termod1.ui",self)  # Подключаем графический интерфейс
        self.gas = termod.GasLaws()  # Инициализация расчетного модуля
        self.result = ""
        self.chekEqv()  # Проверка выбора уравнения для расчета
        self.chekVariable()  # Проверка выбора рассчитываемого параметра
        self.setFormValue()  # Значения переменных в форме

    def btnClear(self):
        """
        Выполняется при клике на кнопку btnClear
        Метод выполняемый при очистке формы и установке
        значений параметров в полях ввода на значения по умолчанию
        """
        self.window.SBpressure.setValue(self.gas.standartpressure)
        self.window.SBtemperature.setValue(self.gas.standarttemperature)
        self.window.SBvolume.setValue(self.gas.standartvolume)
        self.window.SBmoll.setValue(self.gas.standartmoll)
        self.window.SBa.setValue(self.gas.standarta)
        self.window.SBa.setValue(self.gas.standartb)

    def chekEqv(self):
        """
        Выполняется при установке чекбоксов выбора уравнения для расчета (chbMend, chbVander)
        Метод проверки выбранного уравнения для расчета
        (Менделеева-Клапейрона или Ван-Дер-Ваальса)
        Установка видимости необходимых для расчета полей ввода и пояснений
        """
        # список QRadioButton формы
        radio = [self.window.rb_temperature, self.window.rb_pressure, self.window.rb_volume, self.window.rb_moll]
        # Поля ввода параметра a 
        a = [self.window.lb_a, self.window.SBa]
        # Поля ввода параметра b
        b = [self.window.lb_b, self.window.SBb]
        # Список скрываемых полей
        el_hiden = []
        # Список показываемых полей
        el_show = []
        # Формирование списков в зависимости от выбранного чекбокса
        if self.window.chbMend.isChecked():
            el_hiden.extend(a)
            el_hiden.extend(b)
            el_show.extend(radio)
            # Установка значений расчетного модуля
            self.gas.a = 0
            self.gas.b = 0
            # Установка значений поляей в форме из данных расчетного модуля
            self.setFormValue()
        elif self.window.chbVander.isChecked():
            el_show.extend(a)
            el_show.extend(b)
            el_hiden.extend([self.window.rb_volume, self.window.rb_moll])
        # Установка невидимости соответствующих элементов на форме
        for el in el_hiden:
            el.hide()
            el.setDisabled(True)
        # Установка видимости соответствующих элементов на форме
        for el in el_show:
            el.show()
            el.setDisabled(False)

    def setFormValue(self):
        """
        Метод установки значений полей формы на основании данных расчетного модуля
        """
        self.window.SBpressure.setValue(self.gas.pressure)
        self.window.SBtemperature.setValue(self.gas.temperature)
        self.window.SBvolume.setValue(self.gas.volume)
        self.window.SBmoll.setValue(self.gas.moll)
        self.window.SBa.setValue(self.gas.a)
        self.window.SBa.setValue(self.gas.b)

    def btnCalc(self):
        """
        Метод выполняется при клике на кнопку btnCalc
        """
        # Установка параметров в расчетном модуле на основании
        # введеных пользователем
        self.gas.pressure = self.window.SBpressure.value()
        self.gas.volume = self.window.SBvolume.value()
        self.gas.temperature = self.window.SBtemperature.value()
        self.gas.moll = self.window.SBmoll.value()
        self.gas.a = self.window.SBa.value()
        self.gas.b = self.window.SBb.value()
        # Расчет результата в зависимости от выбранного уравнения
        res = None
        if self.window.chbMend.isChecked():
            res = self.gas.MendKlapeiron()
        elif self.window.chbVander.isChecked():
            res = self.gas.VanDerVaals()
        if res is None:
            self.window.lb_result.setText("Ошибка")
        else:
            self.window.lb_result.setText(self.result % res)

    def chekVariable(self):
        """
        Выполняется при установке чекбокса рассчитываемого параметра 
        (rb_temperature, rb_pressure, rb_volume, rb_moll)
        Метод задает в зависимости от выбора пользователя 
        параметр, который необходимо рассчитать. (переменная self.gas.variable),
        формирует строку результата (переменная self.result)
        Метод переключает соответствующую группу элементов в неактивное состояние при выборе параметра для расчета.
        """
        #
        temperature = [self.window.lb_temperatur, self.window.SBtemperature]
        pressure = [self.window.lb_pressure,self.window.SBpressure]
        volume = [self.window.lb_volume, self.window.SBvolume]
        moll = [self.window.lb_moll, self.window.SBmoll]
        all = temperature + pressure + volume + moll
        elements = []
        # Выбор скрываемой группы элементов
        if self.window.rb_temperature.isChecked():
            elements = temperature
            self.result = "Температура: %f K"
            self.gas.variable = "T"
        elif self.window.rb_pressure.isChecked():
            elements = pressure
            self.result = "Давление: %f Па"
            self.gas.variable = "P"
        elif self.window.rb_volume.isChecked():
            elements = volume
            self.result = "Объем: %f м<sup>3</sup>"
            self.gas.variable = "V"
        elif self.window.rb_moll.isChecked():
            elements = moll
            self.result = "Количество вещества: %f моль"
            self.gas.variable = "N"
        # Установка видимости всех элементов
        for el in all:
            el.show()
            el.setDisabled(False)
        # Установка невидимости выбранной группы элементов
        for el in elements:
            el.hide()
            el.setDisabled(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())