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


def btnCommand_printTablesDB():
    pass


def btnCommand_clearTablesDB():
    def btnCommand_clearTables():
        if cursor is not None:
            en.clear_all_tables(cursor)
        root1.destroy()

    root1 = Toplevel()
    root1.title('Подтведите действие')
    root1.geometry("300x70+400+400")
    Label(root1, text="Вы уверены, что хотите очистить все таблицы?").pack(side=TOP)
    btn_yes = Button(root1, text="Да", command=btnCommand_clearTables)
    btn_no = Button(root1, text="Нет", command=root1.destroy)
    btn_yes.pack()
    btn_no.pack()


def btnCommand_printTableProvider():
    root2 = Toplevel()
    root2.title('Таблица "Провайдеры"')

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0")
    tree.column("one")
    tree.column("two")
    tree.column("three")

    # tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
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


def btnCommand_workWithTableProvider():
    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_provider(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_provider(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.geometry("600x250+400+400")
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
        entry1.insert(0, '1')
        entry2 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '1')
        entry3 = Entry(root2, width=20, fg='blue', font=('Arial', 16, 'bold'))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '1')
        entry4 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '1')

        btn_accept = Button(root2, text="Принять", command=btnAccept, width=25)
        btn_accept.grid(row=2, column=1)
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=25)
        btn_no.grid(row=2, column=2)

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_provider_by_id(cursor, entry1.get())
            root2.destroy()
        root2 = Toplevel()
        root2.geometry("600x250+400+400")
        label = Label(root2, text='Введите id')
        label.pack()
        entry1 = Entry(root2, width=4, fg='blue', font=('Arial', 16, 'bold'))
        entry1.insert(0, '0')
        entry1.pack()

        btn_accept = Button(root2, text="Удалить", command=btnAccept, width=25)
        btn_accept.pack()
        btn_no = Button(root2, text="Отмена", command=root2.destroy, width=25)
        btn_no.pack()

    root1 = Toplevel()
    root1.title('Таблица "Провайдеры"')
    root1.geometry("400x250+400+400")
    btn_clearTable = Button(root1, text="Очистить таблицу", command=btnCommand_clearTable)

    btn_printTable = Button(root1, text="Вывести таблицу", command=btnCommand_printTableProvider)

    btn_addNewLine = Button(root1, text="Добавить новую запись", command=btnCommand_addNewLine)

    btn_deleteLine = Button(root1, text="Удалить запись (по id)", command=btnCommand_deleteLine)

    btn_clearTable.pack()
    btn_printTable.pack()
    btn_addNewLine.pack()
    btn_deleteLine.pack()


def btnCommand_workWithTableWorker():
    root1 = Toplevel()
    root1.title('Таблица "Работники"')
    root1.geometry("400x250+400+400")


def btnCommand_workWithTableFlower():
    root1 = Toplevel()
    root1.title('Таблица "Цветы"')
    root1.geometry("400x250+400+400")


if __name__ == '__main__':
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
