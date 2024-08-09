select
' VTS_IT_MSS_124 ' app_code,
update_time,
round(sum(case when solan >=2 then 1 else 0 end)/count(1)*100,2) as KQI,
sum(case when solan >=2 then 1 else 0 end) user_fail,
count(1) users
from
(
select username, trunc(starttime) as update_time , sum(is_fail) solan
from (
select starttime, username,servicecode, duration, transactionstatus,
case when transactionstatus = ' 0 ' -- success
then (
case -- fail kpi
when servicecode = ' MOBILESERVER_SYNDATACONTROLLER_CREATESQLITEFILE ' and duration>= 120000 then 1 -- mobile server: thoi gian tai du lieu lan dau (chua tao file) cua nvbh
when servicecode = ' WEB_SALE_PRODUCT_PRINT_ORDER_SEARCHORDER ' and duration>= 5000 then 1 -- web: tim kiem theo don hang
when servicecode = ' MOBILESERVER_SYNDATACONTROLLERDAY_CREATESQLITEFILE ' and duration>= 30000 then 1 -- mobile server: dong bo du lieu trong ngay
when servicecode = ' WEB_COMMONS_VIEW_INFO ' and duration>= 5000 then 1 -- web: xem chi tiet don hang
when servicecode = ' WEB_SALE_PRODUCT_CREATE_ORDER_ORDER ' and duration>= 120000 then 1 -- web: tao don hang
when servicecode = ' WEB_SALE_PRODUCT_SEARCH_SALE_APPROVED ' and duration>= 40000 then 1 -- web: duyet don hang
when servicecode = ' WEB_LOGIN ' and duration>= 10000 then 1 -- web: dang nhap
else 0
end
)
when transactionstatus = ' 1 ' and errordescription like ' % Exception % ' then 1 -- fail
else 0
end is_fail
from kpi_log
where starttime >= trunc(?)
and starttime < trunc(?)
and servicecode in (' MOBILESERVER_SYNDATACONTROLLER_CREATESQLITEFILE ',' WEB_SALE_PRODUCT_PRINT_ORDER_SEARCHORDER ',' MOBILESERVER_SYNDATACONTROLLERDAY_CREATESQLITEFILE ',' WEB_COMMONS_VIEW_INFO ',' WEB_SALE_PRODUCT_CREATE_ORDER_ORDER ',' WEB_SALE_PRODUCT_SEARCH_SALE_APPROVED ',' WEB_LOGIN ')
and username is not null
)
group by username, trunc(starttime)
) group by update_time
order by update_time asc