import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
    if file_path:
        global df, checkbox_vars, rename_entries
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().replace('，', ',')  # 将中文逗号替换为英文逗号
                data = json.loads(f"[{content}]")  # 将所有对象放入一个列表中
                df = pd.DataFrame(data)

            # 清除旧的复选框和输入框
            for widget in column_frame.winfo_children():
                widget.destroy()
            checkbox_vars = []
            rename_entries = []

            # 创建新的复选框和对应的输入框
            for i, column in enumerate(df.columns):
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(column_frame, text=column, variable=var, command=lambda i=i: toggle_entry(i))
                checkbox.grid(row=i, column=0, sticky='w', padx=5, pady=2)
                checkbox_vars.append(var)
                
                entry = tk.Entry(column_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry.grid_remove()  # 默认隐藏输入框
                rename_entries.append(entry)

            messagebox.showinfo("成功", "文件加载成功。请选择要提取的列并输入新列名（可选）。")
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {e}")
    else:
        messagebox.showwarning("警告", "未选择文件。")

def toggle_entry(index):
    if checkbox_vars[index].get():
        rename_entries[index].grid()  # 显示输入框
    else:
        rename_entries[index].grid_remove()  # 隐藏输入框

def extract_and_save():
    selected_columns = [df.columns[i] for i, var in enumerate(checkbox_vars) if var.get()]
    renames = [entry.get().strip() for entry in rename_entries if entry.winfo_ismapped()]
    
    if not df.empty:
        try:
            if not selected_columns:
                messagebox.showwarning("警告", "未选择任何列。")
                return
            
            extracted_data = df[selected_columns]

            # 检查是否有对应的重命名
            if renames and len(renames) == len(selected_columns):
                extracted_data.columns = renames

            output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel文件", "*.xlsx")])
            if output_file:
                extracted_data.to_excel(output_file, index=False)
                messagebox.showinfo("成功", "数据提取并保存成功。")
        except Exception as e:
            messagebox.showerror("错误", f"提取并保存数据失败: {e}")
    else:
        messagebox.showwarning("警告", "未加载数据。")

# 初始化界面设置
root = tk.Tk()
root.title("数据提取器")
root.geometry("500x400")

frame = tk.LabelFrame(root, text="步骤1：加载数据文件", padx=10, pady=10)
frame.pack(fill="x", padx=10, pady=5)

load_button = tk.Button(frame, text="加载文件", command=load_file)
load_button.pack()

column_frame = tk.LabelFrame(root, text="步骤2：选择要提取的列并重命名（可选）", padx=10, pady=10)
column_frame.pack(fill="x", padx=10, pady=5)

save_frame = tk.Frame(root)
save_frame.pack(pady=10)

save_button = tk.Button(save_frame, text="提取并保存", command=extract_and_save)
save_button.pack()

root.mainloop()
