/*
Code by: Nguyễn Ngô Thượng
Last update: 02/12/2022
Mô tả: 
    Do dữ liệu nhiều nên nhóm import data từ file csv vào để tạo bảng. Rồi sau đó select into ra từng bảng riêng phục vụ cho môn học.
*/

use quanlybanhang_chillax



insert into donhang
    (madonhang, nguoimua, trangthaidonhang,lydohuy)
values
    ('test001', 'nguoimua001', N'Đã hủy', N'không thích')

DELETE DONHANG
WHERE madonhang = 'TEST001'



--xóa bảng đơn hàng
drop table donhang

--tạo bảng đơn hàng
select
    madonhang
    , nguoimua
    , ngaydathang
    , trangthaidonhang
    , lydohuy
into donhang
from v04

select *
from donhang


--xóa các giá trị trùng lặp
with cte_clean_donhang as (
    select *
        , RN = row_number() over(PARTITION by madonhang order by madonhang)
from donhang
)
delete cte_clean_donhang
where RN > 1

select *
from donhang
order by nguoimua



--tạo bảng đơn hàng chi tiết
select
    madonhang
    , skusanpham
	, skuphanloaihang
	, soluong
into donhangchitiet
from v04

select *
from donhangchitiet



-- tạo bảng người mua
select
    nguoimua
    , diachinhanhang
    , tennguoinhan
    , sodienthoai
    , gioitinh
into nguoimua
from v04

select *
from nguoimua

--xóa giá trị trừng lặp
with cte_clean_nguoimua as (
select
    *
    , RN = row_number() over(PARTITION by nguoimua ORDER by nguoimua desc)
from nguoimua
)
delete cte_clean_nguoimua
where RN > 1



select *
from nguoimua



drop table giaohang
--tạo bảng giao hàng
select
    madonhang
	, thoigianhoanthanhdonhang
	, donvivanchuyen
into giaohang
from v04


--xóa mã đơn hàng trùng
with cte_clean_giaohang as (
    select *
        , RN = row_number() over(PARTITION by madonhang order by madonhang)
from giaohang
)
delete cte_clean_giaohang
where RN > 1


select *
from giaohang





-- tạo bảng sản phẩm chi tiết
select
    skusanpham
    , skuphanloaihang
    , tenphanloaihang
    , giaban
into sanphamchitiet
from v04

--tạo bảng sản phẩm (chứa sku sản phẩm và tên sp)
drop table sanpham

select
    skusanpham
    , tensanpham
into sanpham
from v04
order by skusanpham



select *
from sku_table
select *
from sanpham

--xóa trùng lặp
with  cte_clean_sanpham as
(
    select * 
        , RN = ROW_NUMBER() OVER(PARTITION BY skusanpham order by skusanpham)
from sanpham
)
delete cte_clean_sanpham
where rn > 1

--xóa trùng lặp sku phân loại hàng
with
    cte_clean_sanphamchitiet
    as
    (
        select * 
        , RN = ROW_NUMBER() OVER(PARTITION BY skuphanloaihang order by skuphanloaihang)
        from sanphamchitiet
    )
delete cte_clean_sanphamchitiet
where rn > 1


----

select *
from giaohang
    join donhang on giaohang.madonhang = donhang.madonhang
    join nguoimua on donhang.nguoimua = nguoimua.nguoimua
    join donhangchitiet on donhangchitiet.madonhang = donhang.madonhang
    join sanphamchitiet on  donhangchitiet.skuphanloaihang = sanphamchitiet.skuphanloaihang
    join sanpham on sanpham.skusanpham = sanphamchitiet.skusanpham
order by donhang.madonhang
go

create view view_full_info
as
    SELECT
        donhang.*
        , donhangchitiet.skusanpham
        , donhangchitiet.skuphanloaihang
        , donhangchitiet.soluong
        , sanphamchitiet.giaban
        , sanphamchitiet.tenphanloaihang
        , sanpham.tensanpham
        , giaohang.thoigianhoanthanhdonhang
        , giaohang.donvivanchuyen
        , nguoimua.diachinhanhang
        , nguoimua.sodienthoai
        , nguoimua.gioitinh

    FROM donhangchitiet
        left join sanphamchitiet on donhangchitiet.skuphanloaihang = sanphamchitiet.skuphanloaihang
        join sanpham on sanpham.skusanpham = sanphamchitiet.skusanpham
        join donhang on donhangchitiet.madonhang = donhang.madonhang
        join nguoimua on donhang.nguoimua = nguoimua.nguoimua
        join giaohang on donhang.madonhang = giaohang.madonhang
go

select *
from view_full_info


select *
from donhang




select *
from donhang
order by ngaydathang desc

select *
from sanpham



select *
from donhangchitiet




--tạo index cho bảng giao hàng (madonhang) vì mình cần toàn vẹn dữ liệu ko cho trùng lặp
create unique index ind_giaohang on giaohang (madonhang)


select *
from nguoimua

--tạo index cho bảng giao hàng (madonhang) vì mình cần toàn vẹn dữ liệu ko cho trùng lặp
create unique index ind_nguoimua on nguoimua (nguoimua)



go
create trigger tg_ngaydathang
on donhang
for insert
as
    declare @madonhang nvarchar(50)
begin
    select @madonhang = madonhang
    from inserted
    update donhang
    set ngaydathang = getdate()
    where madonhang = @madonhang
end