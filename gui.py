from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import engine as en

DB_NAME = 'name'
USER_NAME = 'viktor'
USER_PASSWORD = 'viktor'

cursor = None

try:
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)
except:
    print('database not exists')


# Button's commands
def btnCommand_createDB():
    global cursor
    en.create_database(DB_NAME, USER_NAME)
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)


def btnCommand_deleteDB():
    global cursor
    if cursor is not None:
        en.disconnect_user(cursor)
        en.drop_database(DB_NAME)
        cursor = None


def btnCommand_clearTablesDB():
    if cursor is None:
        return

    def btnCommand_clearTables():
        en.clear_all_tables(cursor)
        root1.destroy()

    root1 = Toplevel()
    root1.title('Подтведите действие')
    root1.geometry("300x70+550+200")
    Label(root1, text="Вы уверены, что хотите очистить все таблицы?").pack(side=TOP)
    btn_yes = Button(root1, text="Да", command=btnCommand_clearTables)
    btn_no = Button(root1, text="Нет", command=root1.destroy)
    btn_yes.pack()
    btn_no.pack()


def btnCommand_printTableProvider():
    root2 = Toplevel()
    root2.title('Таблица "Провайдеры"')
    root2.geometry("+30+100")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="name")
    tree.heading("two", text="district")
    tree.heading("three", text="discount")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_provider(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
    tree.pack()


def btnCommand_printTableWorker():
    root2 = Toplevel()
    root2.title('Таблица "Работники"')
    root2.geometry("+800+100")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="Имя")
    tree.heading("two", text="Адрес")
    tree.heading("three", text="Зарплата")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_worker(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
    tree.pack()


def btnCommand_printTableFlower():
    root2 = Toplevel()
    root2.title('Таблица "Цветы"')
    root2.geometry("+30+500")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
    tree.column("#0", width=40, minwidth=40, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')
    tree.column("four", anchor='center')
    tree.column("five", anchor='center')
    tree.column("six", anchor='center')
    tree.column("seven", anchor='center')

    tree.heading("#0", text="id")
    tree.heading("one", text="Название")
    tree.heading("two", text="Поставщик")
    tree.heading("three", text="Цвет")
    tree.heading("four", text="Работник")
    tree.heading("five", text="Количество")
    tree.heading("six", text="Стоимость")
    tree.heading("seven", text="Общая стоимость")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_flower(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[7] = values[7][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3],
                                                                    values[4], values[5], values[6],
                                                                    values[7]))
    tree.pack()


def btnCommand_printTablesDB():
    if cursor is None:
        return
    btnCommand_printTableProvider()
    btnCommand_printTableWorker()
    btnCommand_printTableFlower()


def btnCommand_workWithTableProvider():
    if cursor is None:
        return

    def btnCommand_clearTable():
        en.clear_provider(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_provider(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='Имя')
        label.grid(row=0, column=1)
        label = Label(root2, text='Район')
        label.grid(row=0, column=2)
        label = Label(root2, text='Скидка')
        label.grid(row=0, column=3)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.grid(row=1, column=0)
        result = en.print_table_provider(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.insert(0, str(var+1))
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '')
        entry4 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '0')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=2)

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_provider_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.pack()

    root1 = Toplevel()
    root1.title('Таблица "Провайдеры"')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableProvider)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLine = Button(root1, text="Удалить запись (по id)", command=btnCommand_deleteLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLine.pack()


def btnCommand_workWithTableWorker():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_worker(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_worker(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("630x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='Имя')
        label.grid(row=0, column=1)
        label = Label(root2, text='Адрес')
        label.grid(row=0, column=2)
        label = Label(root2, text='Зарплата')
        label.grid(row=0, column=3)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        result = en.print_table_worker(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.insert(0, str(var+1))
        entry1.grid(row=1, column=0)
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '1')
        entry3 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '1')
        entry4 = Entry(root2, width=7, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=2)

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_worker_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.pack()

    root1 = Toplevel()
    root1.title('Таблица "Работники"')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableWorker)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLine = Button(root1, text="Удалить запись (по id)", command=btnCommand_deleteLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLine.pack()


def btnCommand_workWithTableFlower():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_flower(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_flower(cursor, entry1.get(), entry2.get(), entry3.get(),
                             entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("830x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='Название')
        label.grid(row=0, column=1)
        label = Label(root2, text='Поставщик')
        label.grid(row=0, column=2)
        label = Label(root2, text='Цвет')
        label.grid(row=0, column=3)
        label = Label(root2, text='Работник')
        label.grid(row=0, column=4)
        label = Label(root2, text='Количество')
        label.grid(row=0, column=5)
        label = Label(root2, text='Стоимость')
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        result = en.print_table_flower(cursor)
        var = 0
        if len(result) != 0:
            var = int(result[len(result) - 1][0].split(',')[0][1:])
        entry1.grid(row=1, column=0)
        entry1.insert(0, str(var + 1))
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '1')
        entry4 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '')
        entry5 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '1')
        entry6 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '1')
        entry7 = Entry(root2, width=7, fg='blue', font=('Arial', 16, 'bold'))
        entry7.grid(row=1, column=6)
        entry7.insert(0, '1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=3)

    def btnCommand_deleteLineById():
        def btnAccept():
            en.delete_flower_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.pack()

    def btnCommand_deleteLineByName():
        def btnAccept():
            en.delete_flower_by_name(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите имя')
        label.pack()
        entry1 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=20)
        btn_accept.pack()
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.pack()

    def btnCommand_findLine():
        def btnAccept():
            result = en.search_flower_by_name(cursor, entry1.get())

            root3 = Toplevel()
            tree = ttk.Treeview(root3, selectmode='browse')

            tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven")
            tree.column("#0", width=40, minwidth=40)
            tree.column("one")
            tree.column("two")
            tree.column("three")
            tree.column("four")
            tree.column("five")
            tree.column("six")
            tree.column("seven")

            tree.heading("#0", text="id")
            tree.heading("one", text="Название")
            tree.heading("two", text="Поставщик")
            tree.heading("three", text="Цвет")
            tree.heading("four", text="Работник")
            tree.heading("five", text="Количество")
            tree.heading("six", text="Стоимость")
            tree.heading("seven", text="Общая стоимость")

            values = result[0][0].split(',')
            values[0] = values[0][1:]
            values[7] = values[7][:-1]
            tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3],
                                                                        values[4], values[5], values[6],
                                                                        values[7]))
            tree.pack()

        root2 = Toplevel()
        root2.geometry("600x250+550+200")
        label = Label(root2, text='Введите имя')
        label.pack()
        entry1 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '')
        entry1.pack()

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.pack()

    def btnCommand_updateLine():
        def btnAccept():
            en.update_flower(cursor, entry1.get(), entry2.get(), entry3.get(),
                             entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("830x250+550+200")
        label = Label(root2, text='id')
        label.grid(row=0, column=0)
        label = Label(root2, text='Название')
        label.grid(row=0, column=1)
        label = Label(root2, text='Поставщик')
        label.grid(row=0, column=2)
        label = Label(root2, text='Цвет')
        label.grid(row=0, column=3)
        label = Label(root2, text='Работник')
        label.grid(row=0, column=4)
        label = Label(root2, text='Количество')
        label.grid(row=0, column=5)
        label = Label(root2, text='Стоимость')
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.grid(row=1, column=0)
        entry1.insert(0, '-1')
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '-1')
        entry4 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '')
        entry5 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '-1')
        entry6 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '-1')
        entry7 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry7.grid(row=1, column=6)
        entry7.insert(0, '-1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=20)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=20)
        btn_no.grid(row=2, column=3)

    root1 = Toplevel()
    root1.title('Таблица "Цветы"')
    root1.geometry("400x250+550+200")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableFlower)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLineById = Button(root1, text="Удалить запись (по id)", command=btnCommand_deleteLineById)

    btn_deleteLineByName = Button(root1, text="Удалить запись (по имени)", command=btnCommand_deleteLineByName)

    btn_findLine = Button(root1, text="Найти запись (по имени)", command=btnCommand_findLine)

    btn_updateLine = Button(root1, text="Обновить запись (по имени)", command=btnCommand_updateLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLineById.pack()
    btn_deleteLineByName.pack()
    btn_findLine.pack()
    btn_updateLine.pack()


if __name__ == '__main__':
    # Creating GUI
    root = Tk()
    root.title('Магазин цветов - склад')
    root.geometry("400x250+550+200")

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
