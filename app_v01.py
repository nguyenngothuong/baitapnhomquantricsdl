import pyodbc
import pandas as pd

#check drive odbc trên máy
conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                    SERVER=THUONGSPC\SQLEXPRESS; \
                    Database=quanlybanhang_chillax;\
                    UID=btn_qtcsdl;PWD=btn_qtcsdl;') #KO báo lỗi j tức là connect thành công








def f_donvivanchuyen():
    print('1 - Shopee express')
    print('2 - Giao hàng nhanh')
    print('3 - Giao hàng tiết kiệm')
    print('4 - Vnpost')
    user_input = int(input('Nhập số chọn đơn vị vận chuyển: '))
    if user_input == 1:
        return 'Shopee express'
    elif user_input == 2:
        return 'Giao hàng nhanh'    
    elif user_input == 3:
        return 'Giao hàng tiết kiệm'
    else:
        return 'Vnpost'
def f_trangthaidonhang():
    print('1 - Chờ xác nhận')
    print('2 - Chờ giao hàng')
    print('3 - Đang giao')
    print('4 - Hoàn thành')
    user_input = int(input('Nhập số tương ứng với trạng thái đơn hàng: '))
    if user_input == 1:
        return 'Chờ xác nhận'
    elif user_input == 2:
        return 'Chờ giao hàng'    
    elif user_input == 3:
        return 'Đang giao'
    elif user_input == 4:
        return 'Hoàn thành'
    elif user_input == 0:
        return 'Đã hủy'
    else:
        return 'Không xác định'
def kiemtratontai(table,column,value): #kiểm tra sự tồn tại của dữ liệu truyền vào
    conx.commit()
    cursor = conx.cursor()
    cursor.execute(f"SELECT {column} FROM {table}")
    # iterate over the result
    list_nguoimua = []
    for row in cursor:
        list_nguoimua.append(row[0])
    # print(list_nguoimua)
    # conx.close()
    if value in list_nguoimua:
        return 'Đã tồn tại'
    else:
        return 'Chưa tồn tại'

def themdulieu():
#   - input: mã đơn hàng, người mua, mã vận đơn, sku sản phẩm, sku phân loại, số lượng, đơn vị vận chuyển (chọn số), trạng thái đơn hàng (chọn số)
#   - Procress: insert into vào các bảng có chứa những thứ mà khách hàng input vào, ở đây bao gồm: 
#     - giaohang (madonhang, donvivanchuyen, null).
#     - đơn hàng: mã đơn hàng, ngày đặt hàng là ngày hôm nay, người mua, thạng thái đơn hàng
#     - đơn hàng chi tiết: mã đơn hàng, sku sản phẩm, sku phân loại, số lượng
#     - người mua: người mua, địa chỉ, tên người mua, sdt, gioi tinh
# - Ouput:
#   - thông bão đã cập nhật thông tin
    cursor = conx.cursor()


    manguoimua = str(input('Nhập mã người mua: '))
    madonhang = str(input('Nhập mã đơn hàng: '))
    # mavandon = str(input('Nhập mã vận đơn: '))
    skusanpham = str(input('Nhập mã sku sản phẩm: '))
    skuphanloaihang = str(input('Nhập mã sku phân loại hàng: '))
    soluong = int(input("Nhập số lượng: "))

    tendonvivanchuyen = f_donvivanchuyen() #nhập đơn vị vận chuyển
    trangthaidonhang = f_trangthaidonhang() #nhập trạng thái đơn hàng

    if trangthaidonhang == "Đã hủy":
        lydohuy = str(input('Nhập lý do hủy: '))
        cursor.execute("insert donhang (madonhang,nguoimua,trangthaidonhang,lydohuy) values (?,?,?,?)",madonhang,manguoimua,trangthaidonhang,lydohuy)

    elif trangthaidonhang == "Hoàn thành":
        thoigianhoanthanhdonhang = str(input("Nhập ngày hoàn thành đơn hàng: "))
        cursor.execute("insert giaohang (madonhang,thoigianhoanthanhdonhang,donvivanchuyen) values (?,?,?)",madonhang,thoigianhoanthanhdonhang,tendonvivanchuyen)

    else:
        cursor.execute("insert giaohang (madonhang,donvivanchuyen) values (?,?)",madonhang,tendonvivanchuyen) #không nhập vào thoigianhoanthanh don hang
        cursor.execute("insert donhang (madonhang,nguoimua,trangthaidonhang) values (?,?,?)",madonhang,manguoimua,trangthaidonhang)


    if kiemtratontai('nguoimua','nguoimua',manguoimua) == 'Đã tồn tại':
        print(f"Người mua {manguoimua} đã có trong hệ thống!")
        cursor = conx.cursor()

        sql_query = '''
        select sodienthoai from view_full_info 
        where nguoimua = ?
        '''
        cursor.execute(sql_query, manguoimua)
        data = cursor.fetchall()
        sodienthoai = data[0][0]
    else:
        print(f"Người mua {manguoimua} chưa từng phát sinh đơn hàng. Vui lòng nhập thông tin người mua")
        #kiểm tra xem ngườ
        diachinhanhang = str(input("Nhập địa chỉ nhận hàng: "))
        tennguoinhan = str(input("Nhập tên người nhận hàng: "))
        sodienthoai = str(input("Nhập số điện thoại nhận hàng: "))
        gioitinh = str(input("Giới tính: "))
        cursor.execute("insert nguoimua values(?,?,?,?,?)",manguoimua,diachinhanhang,tennguoinhan,sodienthoai,gioitinh)
    
        



    cursor.execute("insert donhangchitiet (madonhang,skusanpham,skuphanloaihang,soluong) values (?,?,?,?)",madonhang,skusanpham,skuphanloaihang,soluong)



    # cursor.fetchall()
    rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
    if rc > 0:
        print("Thêm dữ liệu thành công!")
        print("Dữ liệu mới nhập vào là")
        timkiemdulieu_v03(sodienthoai)
        # main() #chạy tiếp chương trình
        # print("%d"%rc) #số hàng bị ảnh hưởng

    conx.commit() #phải commit cho nó thì mới insert đc. ko như ssms thông thường.
    conx.close()

def suadulieu(): #update du lieu
    cursor = conx.cursor()
    print('Thay đổi thông tin nhận hàng của khách hàng')
    madonhang = str(input('Nhập mã đơn hàng cần sửa: '))
    ten_nguoi_nhan_moi = str(input('Tên người nhận mới: '))
    dia_chi_moi = str(input('Địa chỉ nhận hàng: '))
    so_dien_thoai_moi = str(input('Nhập số điện thoại: '))
    gioi_tinh_moi = str(input("Giới tính: "))

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

    cursor.execute(sql_query, dia_chi_moi, ten_nguoi_nhan_moi, so_dien_thoai_moi, gioi_tinh_moi, madonhang)
    rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
    if rc > 0:
        print("Sửa dữ liệu thành công!")
        # print("%d"%rc) #số hàng bị ảnh hưởng
        print("Thông tin người nhận mới là")
        timkiemdulieu_v03(so_dien_thoai_moi)
        # main() #chạy tiếp chương trình
    conx.commit()
    conx.close()

def xoadulieu(): #update du lieu
    cursor = conx.cursor()
    madonhang = str(input('Nhập mã đơn hàng cần xóa: '))
    tables = ['donhang','giaohang','donhangchitiet']
    for table in tables:
        sql_query = f'''
        delete {table}
        where madonhang = ?
    '''    
        cursor.execute(sql_query, madonhang)

    rc = cursor.rowcount #KIỂM TRA SỐ LƯỢNG HÀNG BỊ ẢNH HƯỞNG BỞI CÂU LỆNH TRÊN
    if rc > 0:
        print("Xóa dữ liệu thành công!")
        print("%d"%rc) #số hàng bị ảnh hưởng
        # main() #chạy tiếp chương trình
    else:
        print("Thất bại, vui lòng thử lại!")
    conx.commit()
    conx.close()

def timkiemdulieu(): #định danh theo sdt khách hàng 
    cursor = conx.cursor()

    sodienthoai = str(input('Nhập sđt khách hàng cần tìm: '))

    sql_query = '''
        select * from view_full_info 
        where sodienthoai = ?
    '''

    cursor.execute(sql_query, sodienthoai)
    print("tìm kiếm dữ liệu thành công!")
    data = cursor.fetchall()
    print(data)
    conx.commit()
    conx.close()


def timkiemdulieu_v04(): #suwr dungj cho code main.py
    import pyodbc
    import pandas as pd

    #check drive odbc trên máy
    conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER=THUONGSPC\SQLEXPRESS; \
                        Database=quanlybanhang_chillax;\
                        UID=btn_qtcsdl;PWD=btn_qtcsdl;') #KO báo lỗi j tức là connect thành công
    cursor = conx.cursor()

    sodienthoai = str(input('Nhập sđt khách hàng cần tìm: '))

    sql_query = '''
        select * from view_full_info 
        where sodienthoai = ?
    '''

    cursor.execute(sql_query, sodienthoai)
    print("tìm kiếm dữ liệu thành công!")
    data = cursor.fetchall()
    print(data)
    conx.commit()
    conx.close()



def timkiemdulieu_v03(sodienthoai): #xem dưới dạng pandas
    sql_query = "select * from view_full_info where sodienthoai = " + "'" + str(sodienthoai) +"'"
    df = pd.read_sql(sql_query,conx)
    print(df)    
    conx.commit()


def timkiemdulieu_v02(): #update du lieu
    madonhang = str(input('Nhập mã đơn hàng cần tìm: '))

    # nguoimua =  "' or 1 = 1--"
    print("tìm kiếm dữ liệu thành công!")
    sql_query = "select * from donhang where madonhang = " + "'" + str(madonhang) +"'"
    df = pd.read_sql(sql_query,conx)
    print(df)    
    conx.commit()


def main():
    print('---QUẢN TRỊ CƠ SỞ DỮ LIỆU BÁN HÀNG CHILLAX---')
    print('Nhập 1 - thêm dữ liệu')
    print('Nhập 2 - sửa dữ liệu')
    print('Nhập 3 - xóa dữ liệu')
    print('Nhập 4 - tìm kiếm dữ liệu')
    print('Nhập 0 - kết thúc trương trình')
    input_func = int(input('Nhập số: '))
    return input_func


if __name__ == "__main__":
    func = main()

    if func == 1:
        print('Thực hiện chức năng thêm dữ liệu....')
        themdulieu()
    elif func == 2: 
        print('Thực hiện chức năng sửa dữ liệu....')
        suadulieu()
    elif func == 3:
        print('Thực hiện chức năng xóa dữ liệu....')
        xoadulieu()
    elif func == 4:
        print('Thực hiện tìm kiếm dữ liệu....')
        # timkiemdulieu()
        sodienthoai = str(input('Nhập sđt khách hàng cần tìm: '))
        timkiemdulieu_v03(sodienthoai)

    else:
        print('kết thúc chương trình')
