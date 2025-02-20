import sys
import json
from tkinter import (
    Tk, Toplevel, Label, Button, Listbox, Entry, messagebox, font, simpledialog, StringVar, END, ACTIVE, Menu
)
from tkinter.ttk import Combobox, Treeview
from tkcalendar import DateEntry
from datetime import datetime


# قاموس للغات (عربي وإنجليزي)
LANGUAGES = {
    "English": {
        "Main Menu": "Main Menu",
        "Student": "Student",
        "Work": "Work",
        "Homework": "Homework",
        "Review": "Review",
        "Study": "Study",
        "Leisure Time": "Leisure Time",
        "Exercise": "Exercise",
        "Personal Tasks": "Personal Tasks",
        "Projects": "Projects",
        "Shopping": "Shopping",
        "Entertainment": "Entertainment",
        "Other": "Other",
        "Task Description": "Task Description",
        "Priority": "Priority",
        "Date": "Date",
        "Add Task": "Add Task",
        "Mark as Done": "Mark as Done",
        "Search Task": "Search Task",
        "Tasks": "Tasks",
        "Search Task Placeholder": "Enter task description...",
        "Task Not Found": "Task not found!",
        "High": "High",
        "Medium": "Medium",
        "Low": "Low",
        "Add Submenu": "Add Submenu",
        "Submenu Name": "Submenu Name",
        "Delete Task": "Delete Task",
        "Completion Rate": "Completion Rate",
        "Uncompleted Tasks": "Uncompleted Tasks",
        "Completed Tasks": "Completed Tasks",
        "Sort By": "Sort By",
        "Date": "Date",
        "Priority": "Priority",
        "Alphabetical": "Alphabetical",
        "Reset": "Reset",
        "Confirm Reset": "Are you sure you want to reset all data?"
    },
    "Arabic": {
        "Main Menu": "القائمة الرئيسية",
        "Student": "طالب",
        "Work": "عمل",
        "Homework": "واجب منزلي",
        "Review": "مراجعة",
        "Study": "دراسة",
        "Leisure Time": "وقت راحة",
        "Exercise": "رياضة",
        "Personal Tasks": "مهام شخصية",
        "Projects": "مشاريع",
        "Shopping": "تسوق",
        "Entertainment": "ترفيه",
        "Other": "أخرى",
        "Task Description": "وصف المهمة",
        "Priority": "الأولوية",
        "Date": "التاريخ",
        "Add Task": "إضافة مهمة",
        "Mark as Done": "تمت المهمة",
        "Search Task": "بحث عن المهمة",
        "Tasks": "المهام",
        "Search Task Placeholder": "أدخل وصف المهمة...",
        "Task Not Found": "المهمة غير موجودة!",
        "High": "عالي",
        "Medium": "متوسط",
        "Low": "منخفض",
        "Add Submenu": "إضافة قائمة فرعية",
        "Submenu Name": "اسم القائمة الفرعية",
        "Delete Task": "حذف المهمة",
        "Completion Rate": "نسبة الإنجاز",
        "Uncompleted Tasks": "المهام الغير منجزة",
        "Completed Tasks": "المهام المنجزة",
        "Sort By": "فرز بواسطة",
        "Date": "التاريخ",
        "Priority": "الأولوية",
        "Alphabetical": "الأبجدي",
        "Reset": "إعادة ضبط",
        "Confirm Reset": "هل أنت متأكد من رغبتك في إعادة ضبط جميع البيانات؟"
    }
}

# عقدة المهمة (TaskNode)
class TaskNode:
    def __init__(self, description, priority, date, completed=False, next_node=None):
        self.description = description  # وصف المهمة
        self.priority = priority  # الأولوية
        self.date = date  # التاريخ
        self.completed = completed  # حالة الإكمال (افتراضيًا غير مكتملة)
        self.next = next_node  # العقدة التالية

# قائمة مرتبطة لإدارة المهام (TaskList)
class TaskList:
    def __init__(self):
        self.head = None  # بداية القائمة

    def add_task(self, description, priority, date, completed=False):
        """إضافة مهمة جديدة إلى القائمة."""
        new_task = TaskNode(description, priority, date, completed)
        if not self.head:
            self.head = new_task
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_task

    def get_all_tasks(self):
        """الحصول على جميع المهام في القائمة."""
        tasks = []
        current = self.head
        while current:
            tasks.append((current.description, current.priority, current.date, current.completed))
            current = current.next
        return tasks

    def mark_task_as_done(self, description):
        """تحديد المهمة كمكتملة بناءً على الوصف."""
        current = self.head
        while current:
            if current.description == description:
                current.completed = True
                break
            current = current.next

    def delete_task(self, description):
        """حذف مهمة بناءً على الوصف."""
        if not self.head:
            return
        if self.head.description == description:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.description == description:
                current.next = current.next.next
                break
            current = current.next

    def sort_by_date(self):
        """فرز المهام بناءً على التاريخ."""
        tasks = self.get_all_tasks()
        tasks.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"))
        self.head = None
        for task in tasks:
            self.add_task(task[0], task[1], task[2], task[3])

    def sort_by_priority(self):
        """فرز المهام بناءً على الأولوية."""
        priority_order = {
            LANGUAGES["Arabic"]["High"]: 3,
            LANGUAGES["Arabic"]["Medium"]: 2,
            LANGUAGES["Arabic"]["Low"]: 1,
            LANGUAGES["English"]["High"]: 3,
            LANGUAGES["English"]["Medium"]: 2,
            LANGUAGES["English"]["Low"]: 1
        }
        tasks = self.get_all_tasks()
        tasks.sort(key=lambda x: priority_order[x[1]], reverse=True)
        self.head = None
        for task in tasks:
            self.add_task(task[0], task[1], task[2], task[3])

    def sort_alphabetically(self):
        """فرز المهام بناءً على الأبجدية."""
        tasks = self.get_all_tasks()
        tasks.sort(key=lambda x: x[0])
        self.head = None
        for task in tasks:
            self.add_task(task[0], task[1], task[2], task[3])


# نافذة إضافة مهمة (AddTaskDialog)
class AddTaskDialog(simpledialog.Dialog):
    def __init__(self, parent, language):
        self.language = language
        super().__init__(parent, LANGUAGES[self.language]["Add Task"])

    def body(self, master):
        """إنشاء واجهة نافذة إضافة مهمة."""
        self.title(LANGUAGES[self.language]["Add Task"])
        self.task_label = Label(master, text=LANGUAGES[self.language]["Task Description"])
        self.task_label.grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = Entry(master)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.priority_label = Label(master, text=LANGUAGES[self.language]["Priority"])
        self.priority_label.grid(row=1, column=0, padx=5, pady=5)
        self.priority_combobox = Combobox(master, values=[
            LANGUAGES[self.language]["High"],
            LANGUAGES[self.language]["Medium"],
            LANGUAGES[self.language]["Low"]
        ])
        self.priority_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.date_label = Label(master, text=LANGUAGES[self.language]["Date"])
        self.date_label.grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(master, selectmode='day')
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        return self.task_entry  # التركيز الأولي على مدخل وصف المهمة

    def apply(self):
        """الحصول على بيانات المهمة المدخلة من المستخدم."""
        description = self.task_entry.get()
        priority = self.priority_combobox.get()
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        self.result = (description, priority, date)


# نافذة إدارة القائمة الفرعية (SubMenuDialog)
class SubMenuDialog(Toplevel):
    def __init__(self, parent, submenu_name, language):
        super().__init__(parent)
        self.language = language
        self.title(submenu_name)
        self.submenu_name = submenu_name
        self.geometry("400x400")
        self.configure(bg='white')

        self.tasks_label = Label(self, text=LANGUAGES[self.language]["Tasks"], font=('Arial', 12))
        self.tasks_label.pack(pady=5)

        self.tasks_tree = Treeview(self, columns=("Description", "Priority", "Date", "Status"), show="headings", height=10)
        self.tasks_tree.heading("Description", text=LANGUAGES[self.language]["Task Description"])
        self.tasks_tree.heading("Priority", text=LANGUAGES[self.language]["Priority"])
        self.tasks_tree.heading("Date", text=LANGUAGES[self.language]["Date"])
        self.tasks_tree.heading("Status", text=LANGUAGES[self.language]["Completion Rate"])
        self.tasks_tree.column("Description", width=150)
        self.tasks_tree.column("Priority", width=80)
        self.tasks_tree.column("Date", width=100)
        self.tasks_tree.column("Status", width=100)
        self.tasks_tree.pack(pady=5)

        self.add_task_button = Button(self, text=LANGUAGES[self.language]["Add Task"], command=self.add_new_task, font=('Arial', 10), bg='white', fg='black', relief='raised', bd=2)
        self.add_task_button.pack(pady=5)

        self.delete_task_button = Button(self, text=LANGUAGES[self.language]["Delete Task"], command=self.delete_selected_task, font=('Arial', 10), bg='white', fg='black', relief='raised', bd=2)
        self.delete_task_button.pack(pady=5)

        self.mark_done_button = Button(self, text=LANGUAGES[self.language]["Mark as Done"], command=self.mark_task_as_done, font=('Arial', 10), bg='white', fg='black', relief='raised', bd=2)
        self.mark_done_button.pack(pady=5)

        self.completion_rate_label = Label(self, text="", font=('Arial', 10))
        self.completion_rate_label.pack(pady=5)

        self.sort_menu = Menu(self, tearoff=0)
        self.sort_menu.add_command(label=LANGUAGES[self.language]["Date"], command=self.sort_by_date)
        self.sort_menu.add_command(label=LANGUAGES[self.language]["Priority"], command=self.sort_by_priority)
        self.sort_menu.add_command(label=LANGUAGES[self.language]["Alphabetical"], command=self.sort_alphabetically)

        self.sort_button = Button(self, text=LANGUAGES[self.language]["Sort By"], command=self.show_sort_menu, font=('Arial', 10), bg='white', fg='black', relief='raised', bd=2)
        self.sort_button.pack(pady=5)

        self.load_tasks()

    def load_tasks(self):
        """تحميل المهام الخاصة بالقائمة الفرعية."""
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        tasks = self.master.get_tasks_for_submenu(self.submenu_name)
        for task in tasks:
            status = "مكتملة" if task[3] else "قيد التنفيذ"
            self.tasks_tree.insert("", END, values=(task[0], task[1], task[2], status))
        self.update_completion_rate()

    def add_new_task(self):
        """إضافة مهمة جديدة إلى القائمة الفرعية."""
        dialog = AddTaskDialog(self, language=self.language)
        if dialog.result:
            description, priority, date = dialog.result
            if description:
                self.master.add_task(self.submenu_name, description, priority, date)
                self.load_tasks()

    def delete_selected_task(self):
        """حذف المهمة المحددة من القائمة الفرعية."""
        selected_item = self.tasks_tree.selection()
        if not selected_item:
            messagebox.showwarning(self, "تنبيه", LANGUAGES[self.language]["Task Not Found"])
            return
        task_description = self.tasks_tree.item(selected_item, "values")[0]
        self.master.delete_task(self.submenu_name, task_description)
        self.load_tasks()

    def mark_task_as_done(self):
        """تحديد المهمة كمكتملة في القائمة الفرعية."""
        selected_item = self.tasks_tree.selection()
        if not selected_item:
            messagebox.showwarning(self, "تنبيه", LANGUAGES[self.language]["Task Not Found"])
            return
        task_description = self.tasks_tree.item(selected_item, "values")[0]
        self.master.mark_task_as_done(self.submenu_name, task_description)
        self.load_tasks()

    def update_completion_rate(self):
        """تحديث نسبة إنجاز المهام في القائمة الفرعية."""
        tasks = self.master.get_tasks_for_submenu(self.submenu_name)
        if not tasks:
            self.completion_rate_label.config(text=f"{LANGUAGES[self.language]['Completion Rate']}: 0%")
            return
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task[3])
        completion_rate = (completed_tasks / total_tasks) * 100
        self.completion_rate_label.config(text=f"{LANGUAGES[self.language]['Completion Rate']}: {completion_rate:.2f}%")

    def show_sort_menu(self):
        """عرض قائمة فرز المهام."""
        try:
            self.sort_menu.tk_popup(self.sort_button.winfo_rootx(), self.sort_button.winfo_rooty() + self.sort_button.winfo_height())
        finally:
            self.sort_menu.grab_release()

    def sort_by_date(self):
        """فرز المهام بناءً على التاريخ."""
        self.master.task_lists[self.submenu_name].sort_by_date()
        self.load_tasks()

    def sort_by_priority(self):
        """فرز المهام بناءً على الأولوية."""
        self.master.task_lists[self.submenu_name].sort_by_priority()
        self.load_tasks()

    def sort_alphabetically(self):
        """فرز المهام بناءً على الأبجدية."""
        self.master.task_lists[self.submenu_name].sort_alphabetically()
        self.load_tasks()


# نافذة إضافة قائمة فرعية (AddSubmenuDialog)
class AddSubmenuDialog(simpledialog.Dialog):
    def __init__(self, parent, language):
        self.language = language
        super().__init__(parent, LANGUAGES[self.language]["Add Submenu"])

    def body(self, master):
        """إنشاء واجهة نافذة إضافة قائمة فرعية."""
        self.title(LANGUAGES[self.language]["Add Submenu"])
        self.submenu_label = Label(master, text=LANGUAGES[self.language]["Submenu Name"])
        self.submenu_label.grid(row=0, column=0, padx=5, pady=5)
        self.submenu_entry = Entry(master)
        self.submenu_entry.grid(row=0, column=1, padx=5, pady=5)

        return self.submenu_entry  # التركيز الأولي على مدخل اسم القائمة الفرعية

    def apply(self):
        """الحصول على اسم القائمة الفرعية المدخل من المستخدم."""
        self.result = self.submenu_entry.get()


# نافذة مهام الطالب (StudentTasksDialog)
class StudentTasksDialog(Toplevel):
    def __init__(self, parent, language):
        super().__init__(parent)
        self.language = language
        self.title(LANGUAGES[self.language]["Student"])  # عنوان النافذة
        self.geometry("300x300")
        self.configure(bg='white')

        # تخطيط عمودي
        self.layout = Tk.Frame(self)

        # إضافة خيارات المهام الخاصة بالطالب
        options = [
            LANGUAGES[self.language]["Homework"],
            LANGUAGES[self.language]["Review"],
            LANGUAGES[self.language]["Study"],
            LANGUAGES[self.language]["Leisure Time"],
            LANGUAGES[self.language]["Exercise"]
        ]

        for i, option in enumerate(options):
            button = Button(self.layout, text=option, bg='white', fg='black', relief='raised', bd=2)  # إنشاء زر لكل خيار
            button.config(command=lambda opt=option: self.open_add_task_dialog(opt))  # فتح نافذة إضافة مهمة
            button.pack(pady=5)  # إضافة الزر إلى التخطيط

        self.layout.pack(expand=True, fill='both')  # تعيين التخطيط

    def open_add_task_dialog(self, option):
        """فتح نافذة إضافة مهمة."""
        dialog = AddTaskDialog(self, language=self.language)
        if dialog.result:
            description, priority, date = dialog.result
            if description:  # التأكد من أن الوصف ليس فارغًا
                self.master.add_task(LANGUAGES[self.language]["Student"], description, priority, date)


# نافذة مهام العمل (WorkTasksDialog)
class WorkTasksDialog(Toplevel):
    def __init__(self, parent, language):
        super().__init__(parent)
        self.language = language
        self.title(LANGUAGES[self.language]["Work"])  # عنوان النافذة
        self.geometry("300x300")
        self.configure(bg='white')

        # تخطيط عمودي
        self.layout = Tk.Frame(self)

        # إضافة خيارات المهام الخاصة بالعمل
        options = [
            LANGUAGES[self.language]["Personal Tasks"],
            LANGUAGES[self.language]["Projects"],
            LANGUAGES[self.language]["Shopping"],
            LANGUAGES[self.language]["Exercise"],
            LANGUAGES[self.language]["Entertainment"],
            LANGUAGES[self.language]["Other"]
        ]

        for i, option in enumerate(options):
            button = Button(self.layout, text=option, bg='white', fg='black', relief='raised', bd=2)  # إنشاء زر لكل خيار
            button.config(command=lambda opt=option: self.open_add_task_dialog(opt))  # فتح نافذة إضافة مهمة
            button.pack(pady=5)  # إضافة الزر إلى التخطيط

        self.layout.pack(expand=True, fill='both')  # تعيين التخطيط

    def open_add_task_dialog(self, option):
        """فتح نافذة إضافة مهمة."""
        dialog = AddTaskDialog(self, language=self.language)
        if dialog.result:
            description, priority, date = dialog.result
            if description:  # التأكد من أن الوصف ليس فارغًا
                self.master.add_task(LANGUAGES[self.language]["Work"], description, priority, date)


# واجهة التطبيق الرئيسي (ToDoApp)
class ToDoApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List Manager")
        self.geometry("700x700")
        self.configure(bg='lightblue')

        self.language = "Arabic"
        self.font = font.Font(family="Arial", size=12)

        self.language_label = Label(self, text=LANGUAGES[self.language]["Main Menu"], font=self.font, bg='lightblue')
        self.language_label.pack(pady=5)

        self.language_combobox = Combobox(self, values=list(LANGUAGES.keys()), font=self.font)
        self.language_combobox.set(self.language)
        self.language_combobox.bind("<<ComboboxSelected>>", self.update_language)
        self.language_combobox.pack(pady=5)

        self.main_menu_label = Label(self, text=LANGUAGES[self.language]["Tasks"], font=self.font, bg='lightblue')
        self.main_menu_label.pack(pady=5)

        self.main_menu_list = Listbox(self, font=self.font, height=5, bg='lightgray', selectbackground='lightblue')
        self.main_menu_list.bind('<<ListboxSelect>>', self.open_sub_menu)
        self.main_menu_list.pack(pady=5)

        self.add_submenu_button = Button(self, text=LANGUAGES[self.language]["Add Submenu"], command=self.add_new_submenu, font=self.font, bg='white', fg='black', relief='raised', bd=2)
        self.add_submenu_button.pack(pady=5)

        self.tasks_label = Label(self, text=LANGUAGES[self.language]["Tasks"], font=self.font, bg='lightblue')
        self.tasks_label.pack(pady=5)

        self.tasks_tree = Treeview(self, columns=("Description", "Priority", "Date", "Status"), show="headings", height=15)
        self.tasks_tree.heading("Description", text=LANGUAGES[self.language]["Task Description"])
        self.tasks_tree.heading("Priority", text=LANGUAGES[self.language]["Priority"])
        self.tasks_tree.heading("Date", text=LANGUAGES[self.language]["Date"])
        self.tasks_tree.heading("Status", text=LANGUAGES[self.language]["Completion Rate"])
        self.tasks_tree.column("Description", width=200)
        self.tasks_tree.column("Priority", width=100)
        self.tasks_tree.column("Date", width=100)
        self.tasks_tree.column("Status", width=100)
        self.tasks_tree.pack(pady=5)

        self.mark_done_button = Button(self, text=LANGUAGES[self.language]["Mark as Done"], command=self.mark_task_as_done, font=self.font, bg='white', fg='black', relief='raised', bd=2)
        self.mark_done_button.pack(pady=5)

        self.search_label = Label(self, text=LANGUAGES[self.language]["Search Task"], font=self.font, bg='lightblue')
        self.search_label.pack(pady=5)

        self.search_box = Entry(self, font=self.font)
        self.search_box.insert(0, LANGUAGES[self.language]["Search Task Placeholder"])
        self.search_box.bind("<KeyRelease>", self.search_task)
        self.search_box.pack(pady=5)

        # Ensure the Reset button is packed correctly
        self.reset_button = Button(self, text=LANGUAGES[self.language]["Reset"], command=self.confirm_reset, font=self.font, bg='white', fg='black', relief='raised', bd=2)
        self.reset_button.pack(pady=5)

        self.task_lists = {}
        self.load_from_json()

        # إضافة قائمة فرعية لمهام الغير منجزة والمهام المنجزة
        self.main_menu_list.insert(END, LANGUAGES[self.language]["Uncompleted Tasks"])
        self.main_menu_list.insert(END, LANGUAGES[self.language]["Completed Tasks"])

    def update_language(self, event):
        """تحديث اللغة لأجزاء الواجهة."""
        self.language = self.language_combobox.get()
        self.language_label.config(text=LANGUAGES[self.language]["Main Menu"])
        self.main_menu_label.config(text=LANGUAGES[self.language]["Tasks"])
        self.tasks_label.config(text=LANGUAGES[self.language]["Tasks"])
        self.mark_done_button.config(text=LANGUAGES[self.language]["Mark as Done"])
        self.search_label.config(text=LANGUAGES[self.language]["Search Task"])
        self.search_box.delete(0, END)
        self.search_box.insert(0, LANGUAGES[self.language]["Search Task Placeholder"])
        self.add_submenu_button.config(text=LANGUAGES[self.language]["Add Submenu"])
        self.reset_button.config(text=LANGUAGES[self.language]["Reset"])

        self.main_menu_list.delete(0, END)
        for key in self.task_lists:
            self.main_menu_list.insert(END, key)
        self.main_menu_list.insert(END, LANGUAGES[self.language]["Uncompleted Tasks"])
        self.main_menu_list.insert(END, LANGUAGES[self.language]["Completed Tasks"])

    def add_new_submenu(self):
        """إضافة قائمة فرعية جديدة."""
        dialog = AddSubmenuDialog(self, language=self.language)
        if dialog.result:
            submenu_name = dialog.result.strip()
            if submenu_name and submenu_name not in self.task_lists:
                self.task_lists[submenu_name] = TaskList()
                self.main_menu_list.insert(END, submenu_name)
                self.save_to_json(submenu_name)
                messagebox.showinfo("نجاح", f"تم إضافة القائمة الفرعية '{submenu_name}' بنجاح!")
            else:
                messagebox.showwarning("تحذير", "اسم القائمة الفرعية موجود بالفعل أو فارغ!")

    def open_sub_menu(self, event):
        """فتح القائمة الفرعية المحددة."""
        selected_index = self.main_menu_list.curselection()
        if selected_index:
            selected_item = self.main_menu_list.get(selected_index)
            if selected_item in self.task_lists:
                dialog = SubMenuDialog(self, selected_item, language=self.language)
                dialog.mainloop()
            elif selected_item == LANGUAGES[self.language]["Uncompleted Tasks"]:
                self.show_uncompleted_tasks()
            elif selected_item == LANGUAGES[self.language]["Completed Tasks"]:
                self.show_completed_tasks()

    def load_tasks_for_submenu(self, submenu):
        """تحميل المهام الخاصة بالقائمة الفرعية."""
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        if submenu in self.task_lists:
            tasks = self.task_lists[submenu].get_all_tasks()
            for task in tasks:
                status = "مكتملة" if task[3] else "قيد التنفيذ"
                self.tasks_tree.insert("", END, values=(task[0], task[1], task[2], status))

    def add_task(self, submenu, description, priority, date, completed=False):
        """إضافة مهمة جديدة إلى القائمة الفرعية المحددة."""
        self.task_lists[submenu].add_task(description, priority, date, completed)
        self.load_tasks_for_submenu(submenu)
        self.save_to_json(submenu)

    def mark_task_as_done(self):
        """تحديد المهمة كمكتملة."""
        selected_item = self.tasks_tree.selection()
        if not selected_item:
            messagebox.showinfo("تنبيه", LANGUAGES[self.language]["Task Not Found"])
            return
        task_description = self.tasks_tree.item(selected_item, "values")[0]
        for submenu, task_list in self.task_lists.items():
            task_list.mark_task_as_done(task_description)
        self.load_tasks_for_submenu(self.main_menu_list.get(ACTIVE))
        self.save_to_json(self.main_menu_list.get(ACTIVE))

    def delete_task(self, submenu, description):
        """حذف مهمة من القائمة الفرعية المحددة."""
        self.task_lists[submenu].delete_task(description)
        self.load_tasks_for_submenu(submenu)
        self.save_to_json(submenu)

    def search_task(self, event):
        """بحث عن مهمة باستخدام الكلمات المفتاحية."""
        search_text = self.search_box.get().strip().lower()
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        if search_text:
            found = False
            for submenu, task_list in self.task_lists.items():
                tasks = task_list.get_all_tasks()
                for task in tasks:
                    if search_text in task[0].lower():
                        self.load_tasks_for_submenu(submenu)
                        self.tasks_tree.delete(*self.tasks_tree.get_children())
                        status = "مكتملة" if task[3] else "قيد التنفيذ"
                        self.tasks_tree.insert("", END, values=(task[0], task[1], task[2], status))
                        found = True
                        break
                if found:
                    break
            if not found:
                messagebox.showinfo("بحث", LANGUAGES[self.language]["Task Not Found"])

    def load_from_json(self):
        """تحميل البيانات من ملف JSON."""
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for submenu, tasks in data.items():
                    self.task_lists[submenu] = TaskList()
                    for task in tasks:
                        self.task_lists[submenu].add_task(task['description'], task['priority'], task['date'], task['completed'])
                    self.main_menu_list.insert(END, submenu)
        except FileNotFoundError:
            pass

    def save_to_json(self, submenu):
        """حفظ البيانات في ملف JSON."""
        data = {}
        for key, task_list in self.task_lists.items():
            tasks = task_list.get_all_tasks()
            data[key] = [{'description': task[0], 'priority': task[1], 'date': task[2], 'completed': task[3]} for task in tasks]
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_tasks_for_submenu(self, submenu):
        """الحصول على جميع المهام في القائمة الفرعية المحددة."""
        if submenu in self.task_lists:
            return self.task_lists[submenu].get_all_tasks()
        return []

    def show_uncompleted_tasks(self):
        """عرض جميع المهام الغير منجزة."""
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for submenu, task_list in self.task_lists.items():
            tasks = task_list.get_all_tasks()
            for task in tasks:
                if not task[3]:
                    status = "قيد التنفيذ"
                    self.tasks_tree.insert("", END, values=(task[0], task[1], task[2], status))

    def show_completed_tasks(self):
        """عرض جميع المهام المنجزة."""
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for submenu, task_list in self.task_lists.items():
            tasks = task_list.get_all_tasks()
            for task in tasks:
                if task[3]:
                    status = "مكتملة"
                    self.tasks_tree.insert("", END, values=(task[0], task[1], task[2], status))

    def confirm_reset(self):
        """تأكيد إعادة ضبط جميع البيانات."""
        response = messagebox.askyesno("تأكيد إعادة الضبط", LANGUAGES[self.language]["Confirm Reset"])
        if response:
            self.reset_data()

    def reset_data(self):
        """إعادة ضبط جميع البيانات."""
        self.task_lists = {}
        self.main_menu_list.delete(0, END)
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        self.save_to_json("reset")
        messagebox.showinfo("نجاح", "تم إعادة ضبط جميع البيانات بنجاح!")


if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
