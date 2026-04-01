import tkinter as tk
from tkinter import messagebox, ttk
from btree_engine import BTree

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh viên - Cây Chỉ Mục")
        self.tree_index = BTree(m=3) 
        self.data_list = []
        self.labels = ["Mã SV", "Họ Tên", "Giới tính", "Khoa", "Năm học"]
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.LabelFrame(self.root, text=" Quản lý Dữ liệu ", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        for i, text in enumerate(self.labels):
            tk.Label(input_frame, text=text).grid(row=0, column=i*2)
            
            if text == "Giới tính":
                ent = ttk.Combobox(input_frame, values=["Nam", "Nữ"], width=9, state="readonly")
                ent.set("Nam")
            else:
                ent = tk.Entry(input_frame, width=12)
                
            ent.grid(row=0, column=i*2+1, padx=5)
            self.entries[text] = ent

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Thêm Sinh Viên", command=self.add_sv, bg="#e1f5fe").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Xóa Sinh Viên (theo Mã)", command=self.del_sv, bg="#ffebee").pack(side="left", padx=5)

        search_frame = tk.LabelFrame(self.root, text=" Tra cứu Sinh viên ", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Nhập từ khóa (Mã SV hoặc Tên):").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(search_frame, text="Tìm theo Mã SV", command=self.find_sv_msv, bg="#fffde7").pack(side="left", padx=5)
        tk.Button(search_frame, text="Tìm theo Tên", command=self.find_sv_name, bg="#e8f5e9").pack(side="left", padx=5)

        display_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        display_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(display_frame, columns=self.labels, show="headings")
        for lb in self.labels: 
            self.table.heading(lb, text=lb)
            self.table.column(lb, width=80 if lb in ["Mã SV", "Năm học", "Giới tính"] else 120)
        display_frame.add(self.table)

        self.tree_view = tk.Text(display_frame, width=45, font=("Consolas", 11), bg="#f5f5f5")
        display_frame.add(self.tree_view)

    def add_sv(self):
        info = {lb: self.entries[lb].get().strip() for lb in self.labels}
        
        if not all(info.values()):
            messagebox.showwarning("Lỗi", "Vui lòng điền đủ 5 thông tin")
            return
            
        if not info["Mã SV"].isdigit() or not (1 <= int(info["Mã SV"]) <= 100):
            messagebox.showwarning("Lỗi", "Mã SV phải là SỐ từ 1 đến 100!")
            return
            
        if not info["Năm học"].isdigit() or not (1 <= int(info["Năm học"]) <= 7):
            messagebox.showwarning("Lỗi", "Năm học phải là SỐ từ 1 đến 7!")
            return
            
        msv_int = int(info["Mã SV"])
        
        if any(s["Mã SV"] == str(msv_int) for s in self.data_list):
            messagebox.showwarning("Lỗi", "Mã Sinh viên này đã tồn tại!")
            return

        info["Mã SV"] = str(msv_int)
        self.data_list.append(info)
        
        self.tree_index.insert(msv_int)
        self.update_ui(f"[+] Đã thêm sinh viên: {info['Mã SV']}")
        
        for text, ent in self.entries.items(): 
            if text != "Giới tính":
                ent.delete(0, tk.END)

    def del_sv(self):
        msv_str = self.entries["Mã SV"].get().strip()
        if not msv_str.isdigit():
            messagebox.showwarning("Lỗi", "Vui lòng nhập đúng Mã SV ở khu vực Quản lý để xóa")
            return
            
        msv_int = int(msv_str)
        if not any(s["Mã SV"] == str(msv_int) for s in self.data_list):
            messagebox.showwarning("Lỗi", "Không tồn tại Mã SV này để xóa!")
            return

        self.data_list = [s for s in self.data_list if s["Mã SV"] != str(msv_int)]
        self.tree_index.delete(msv_int)
        self.update_ui(f"[-] Đã xóa sinh viên: {msv_int}")

    def find_sv_msv(self):
        query = self.search_entry.get().strip()
        if not query.isdigit(): 
            messagebox.showwarning("Lỗi", "Vui lòng nhập Mã SV (là số) vào ô Tra cứu!")
            return
        
        msv_int = str(int(query))
        result = next((s for s in self.data_list if s["Mã SV"] == msv_int), None)
        
        if result:
            msg = f"Mã SV: {result['Mã SV']}\nHọ Tên: {result['Họ Tên']}\nGiới tính: {result['Giới tính']}\nKhoa: {result['Khoa']}\nNăm học: {result['Năm học']}"
            messagebox.showinfo("Kết quả tra cứu", msg)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy Mã SV này!")

    def find_sv_name(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Lỗi", "Vui lòng nhập Tên cần tìm vào ô Tra cứu!")
            return
            
        results = [s for s in self.data_list if query in s["Họ Tên"].lower()]
        
        if results:
            msg = ""
            for s in results:
                msg += f"[{s['Mã SV']}] {s['Họ Tên']} - {s['Giới tính']} - Khoa {s['Khoa']} (Năm {s['Năm học']})\n"
            messagebox.showinfo("Kết quả tra cứu", f"Tìm thấy {len(results)} sinh viên:\n\n{msg}")
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy sinh viên nào có tên '{query}'!")

    def update_ui(self, log_msg=""):
        for i in self.table.get_children(): 
            self.table.delete(i)
        for s in self.data_list: 
            self.table.insert("", "end", values=list(s.values()))
            
        self.tree_view.delete("1.0", tk.END)
        if log_msg:
            self.tree_view.insert(tk.END, f"{log_msg}\n")
        self.tree_view.insert(tk.END, "--- CẤU TRÚC CÂY CHỈ MỤC ---\n\n")
        self.tree_view.insert(tk.END, self.tree_index.get_visual())

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()