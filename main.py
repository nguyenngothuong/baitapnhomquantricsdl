#************************** man hinh loai 1 *************************
import pyodbc
import pandas as pd
import sys
# pip install pyqt5
# from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem, QMainWindow
)
from gui_v03 import Ui_MainWindow
from app_v01 import kiemtratontai, timkiemdulieu
#check drive odbc trên máy
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                            SERVER=THUONGSPC\SQLEXPRESS; \
                            Database=quanlybanhang_chillax;\
                            UID=btn_qtcsdl;PWD=btn_qtcsdl;') #KO báo lỗi j tức là connect thành công



class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow() #thay thế cho class Ui_MainWindow(), chỉ cần gọi uic là màn hình ra, uio chỉ là cái biến thôi.
        self.uic.setupUi(self.main_win)
        self.uic.button_search.clicked.connect(self.show_result_view_search)
        self.uic.button_delete.clicked.connect(self.show_result_view_delete)
        self.uic.button_ok_edit.clicked.connect(self.show_result_edit)
        self.uic.button_create.clicked.connect(self.show_result_create)
        self.uic.check_khach_hang.clicked.connect(self.checktontai)

    def checktontai(self):
        manguoimua = str(self.uic.ma_khach_hang_create.text())
        if kiemtratontai('nguoimua','nguoimua',manguoimua) == 'Đã tồn tại':
            self.uic.kiem_tra_khach_hang.setText(f"Khách hàng {manguoimua} đã tồn tại, không cần nhập thông tin người nhận!")
        else:
            self.uic.kiem_tra_khach_hang.setText(f"Người mua {manguoimua} chưa từng phát sinh đơn hàng. Vui lòng nhập thông tin người mua")

        
            


    def show_result_create(self):
    #   - input: mã đơn hàng, người mua, mã vận đơn, sku sản phẩm, sku phân loại, số lượng, đơn vị vận chuyển (chọn số), trạng thái đơn hàng (chọn số)
    #   - Procress: insert into vào các bảng có chứa những thứ mà khách hàng input vào, ở đây bao gồm: 
    #     - giaohang (madonhang, donvivanchuyen, null).
    #     - đơn hàng: mã đơn hàng, ngày đặt hàng là ngày hôm nay, người mua, thạng thái đơn hàng
    #     - đơn hàng chi tiết: mã đơn hàng, sku sản phẩm, sku phân loại, số lượng
    #     - người mua: người mua, địa chỉ, tên người mua, sdt, gioi tinh
    # - Ouput:
    #   - thông bão đã cập nhật thông tin
        cursor = conx.cursor()


        manguoimua = str(self.uic.ma_khach_hang_create.text())
        madonhang = str(self.uic.ma_don_hang_create.text())
        # mavandon = str(input('Nhập mã vận đơn: '))
        skusanpham = str(self.uic.sku_san_pham_create.text())
        skuphanloaihang = str(self.uic.sku_phan_loai_hang_create.text())
        soluong = int(self.uic.so_luong_create.text())
        tendonvivanchuyen = str(self.uic.don_vi_van_chuyen_create.currentText())
        trangthaidonhang = str(self.uic.trang_thai_don_hang_create.currentText())

        if trangthaidonhang == "Đã hủy":
            lydohuy = str(self.uic.ly_do_huy_create.text())
            cursor.execute("insert donhang (madonhang,nguoimua,trangthaidonhang,lydohuy) values (?,?,?,?)",madonhang,manguoimua,trangthaidonhang,lydohuy)

        elif trangthaidonhang == "Hoàn thành":
            thoigianhoanthanhdonhang = str(self.uic.thoi_gian_hoan_thanh_don_hang_create.currentSection())
            cursor.execute("insert giaohang (madonhang,thoigianhoanthanhdonhang,donvivanchuyen) values (?,?,?)",madonhang,thoigianhoanthanhdonhang,tendonvivanchuyen)

        else:
            cursor.execute("insert giaohang (madonhang,donvivanchuyen) values (?,?)",madonhang,tendonvivanchuyen) #không nhập vào thoigianhoanthanh don hang
            cursor.execute("insert donhang (madonhang,nguoimua,trangthaidonhang) values (?,?,?)",madonhang,manguoimua,trangthaidonhang)

        # self.uic.button_create.clicked.connect(self.show_result_create)

        if kiemtratontai('nguoimua','nguoimua',manguoimua) == 'Đã tồn tại':
            # self.uic.kiem_tra_khach_hang.setText("Khách hàng đã tồn tại, không cần nhập thông tin người nhận!")
            cursor = conx.cursor()
            sql_query = '''
            select sodienthoai from view_full_info 
            where nguoimua = ?
            '''
            cursor.execute(sql_query, manguoimua)
            data = cursor.fetchall()
            sodienthoai = data[0][0]
        else:
            # self.uic.kiem_tra_khach_hang.setText(f"Người mua {manguoimua} chưa từng phát sinh đơn hàng. Vui lòng nhập thông tin người mua")
            #kiểm tra xem ngườ
            diachinhanhang = str(self.uic.dia_chi_nhan_hang_create.text())
            tennguoinhan = str(self.uic.ten_nguoi_nhan_create.text())
            sodienthoai = str(self.uic.so_dien_thoai_create_2.text())
            gioitinh = str(self.uic.gioi_tinh_create.currentText())
            cursor.execute("insert nguoimua values(?,?,?,?,?)",manguoimua,diachinhanhang,tennguoinhan,sodienthoai,gioitinh)
        
            



        cursor.execute("insert donhangchitiet (madonhang,skusanpham,skuphanloaihang,soluong) values (?,?,?,?)",madonhang,skusanpham,skuphanloaihang,soluong)

        conx.commit()
        rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
        if rc > 0:
            self.uic.noti_result_create.setText("Trạng thái: Thành công")
            # print("%d"%rc) #số hàng bị ảnh hưởng
            cursor = conx.cursor()
            sql_query = '''
                select * from view_full_info 
                where madonhang = ?
            '''
            cursor.execute(sql_query, madonhang)
            result = cursor.fetchall()

            self.uic.tableWidget_create.setRowCount(0)
            #ghi duwx lieu
            for row_number, row_data in enumerate(result):
                self.uic.tableWidget_create.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.uic.tableWidget_create.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            self.uic.noti_result_create.setText("Trạng thái: Thất bại, vui lòng thử lại!")

            # main() #chạy tiếp chương trình




    def show_result_edit(self): #update du lieu
        cursor = conx.cursor()

        # sodienthoai = str(self.uic.so_dien_thoai.text())
        ma_don_hang_moi = str(self.uic.ma_don_hang_edit.text())
        ten_nguoi_nhan_moi = str(self.uic.ten_nguoi_nhan_edit.text())
        dia_chi_moi = str(self.uic.dia_chi_nhan_hang_edit.text())
        so_dien_thoai_moi = str(self.uic.so_dien_thoai_edit.text())
        gioi_tinh_moi = str(self.uic.gioi_tinh_edit.currentText())

        sql_query = '''
            update nguoimua 
            set diachinhanhang = ?
                ,tennguoinhan = ?
                ,sodienthoai = ?
                ,gioitinh = ?
            where nguoimua = (
                select
                    nguoimua.nguoimua
                from donhang
                    left join nguoimua on donhang.nguoimua = nguoimua.nguoimua
                where madonhang = ?
            )
        '''

        cursor.execute(sql_query, dia_chi_moi, ten_nguoi_nhan_moi, so_dien_thoai_moi, gioi_tinh_moi, ma_don_hang_moi)
        conx.commit()
        rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
        if rc > 0:
            self.uic.noti_result_edit.setText("Trạng thái: Thành công")
            print("Sửa dữ liệu thành công!")
            # print("%d"%rc) #số hàng bị ảnh hưởng
            cursor = conx.cursor()
            sql_query = '''
                select * from view_full_info 
                where madonhang = ?
            '''
            cursor.execute(sql_query, ma_don_hang_moi)
            result = cursor.fetchall()

            self.uic.tableWidget_edit.setRowCount(0)
            #ghi duwx lieu
            for row_number, row_data in enumerate(result):
                self.uic.tableWidget_edit.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.uic.tableWidget_edit.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            self.uic.noti_result_edit.setText("Trạng thái: Thất bại, vui lòng thử lại!")

            # main() #chạy tiếp chương trình



    def show_result_view_search(self):
        cursor = conx.cursor()
        sodienthoai = str(self.uic.so_dien_thoai.text())
        sql_query = '''
            select * from view_full_info 
            where sodienthoai = ?
            order by ngaydathang,madonhang
        '''

        cursor.execute(sql_query, sodienthoai)
        result = cursor.fetchall()
        conx.commit()

        self.uic.tableWidget_search.setRowCount(0)
        #ghi duwx lieu
        for row_number, row_data in enumerate(result):
            self.uic.tableWidget_search.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.uic.tableWidget_search.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        
        # conx.close() #ko dong ket noi, de no xoa may cai khac
        #show sdt tim kiem
        # sdt_kq = self.so_dien_thoai
        # self.uic.tableWidget.showColumn(self.so_dien_thoai.text())
        # self.uic.show.setText("hello ba gia ngheo kho giua troi dong co don")
        # self.uic.tableView("a,b,c")

    def show_result_view_delete(self): #update du lieu
        cursor = conx.cursor()
        madonhang = str(self.uic.ma_don_hang_xoa.text())
        # print(madonhang)
        tables = ['donhang','giaohang','donhangchitiet']
        for table in tables:
            sql_query = f'''
            delete {table}
            where madonhang = ?
        '''    
            cursor.execute(sql_query, madonhang)

        rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
        if rc > 0:
            self.uic.result_screen_delete.setText(str("Xóa dữ liệu thành công!"))
            # print("%d"%rc) #số hàng bị ảnh hưởng
            # main() #chạy tiếp chương trình
            conx.commit()
            # conx.close()
        else:
            self.uic.result_screen_delete.setText(str("Thất bại, vui lòng thử lại!"))

            # print("Thất bại, vui lòng thử lại!")


    def show(self):
        # command to run
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


