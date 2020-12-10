from tkinter import *
from tkinter import messagebox as mb


# Button's commands
def btnCommand_createDB():
    pass


def btnCommand_deleteDB():
    pass


def btnCommand_printTablesDB():
    pass


def btnCommand_clearTablesDB():
    def btnCommand_clearTables():
        pass

    root1 = Toplevel()
    root1.title('Подтведите действие')
    root1.geometry("300x70+400+400")
    Label(root1, text="Вы уверены, что хотите очистить все таблицы?").pack(side=TOP)
    btn_yes = Button(root1, text="Да", command=btnCommand_clearTables)
    btn_no = Button(root1, text="Нет", command=root1.destroy)
    btn_yes.pack()
    btn_no.pack()


def btnCommand_workWithTableProvider():
    def btnCommand_clearTable():
        pass

    root1 = Toplevel()
    root1.title('Таблица "Провайдеры"')
    root1.geometry("400x250+400+400")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_clearTable.pack()


def btnCommand_workWithTableWorker():
    root1 = Toplevel()
    root1.title('Таблица "Работники"')
    root1.geometry("400x250+400+400")


def btnCommand_workWithTableFlower():
    root1 = Toplevel()
    root1.title('Таблица "Цветы"')
    root1.geometry("400x250+400+400")


# Creating GUI
root = Tk()
root.title('Магазин цветов - склад')
root.geometry("400x250+400+400")

button_createDB = Button(text="Создать базу данных", command=btnCommand_createDB)
button_deleteDB = Button(text="Удалить базу данных", command=btnCommand_deleteDB)

button_printTables = Button(text="Вывести все таблицы", command=btnCommand_printTablesDB)
button_clearTables = Button(text="Очистить все таблицы", command=btnCommand_clearTablesDB)

button_workWithTableProvider = Button(text="Таблица 'Поставщики'", command=btnCommand_workWithTableProvider)
button_workWithTableWorker = Button(text="Таблица 'Работники'", command=btnCommand_workWithTableWorker)
button_workWithTableFlower = Button(text="Таблица 'Цветы'", command=btnCommand_workWithTableFlower)

button_createDB.pack()
button_deleteDB.pack()
button_printTables.pack()
button_clearTables.pack()
button_workWithTableProvider.pack()
button_workWithTableWorker.pack()
button_workWithTableFlower.pack()

root.mainloop()
