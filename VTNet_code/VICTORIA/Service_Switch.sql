select
    y.Service_ID,
    y.Service_name,
    y.Instance_ID,
    y.Primary_ip4,
    z.Switch_ID,
    z.Name,
    z.Interface_name,
    case
        when z.Name like '%data%leaf%' then 'Datalake'
        when z.Name like '%cloud%leaf%' then 'Cloud'
        ELSE 'Khac'
    END AS Loai_ha_tang,
    y.insert_time
from
    (
        select
            x.Service_ID,
            x.Service_name,
            x.Instance_ID,
            i.Primary_ip4,
            x.insert_time
        from
            (
                select
                    s.Service_ID,
                    s.Service_name,
                    su.Instance_ID,
                    s.insert_time
                from
                    Service s
                    inner join Service_User su on su.Service_ID = s.Service_ID
            ) as x
            inner join `Instance` i on i.Instance_ID = x.Instance_id
    ) as y
    inner join -- dieu kien cua inner join nay la o dong 13: on z.Neighbor...  
    (
        select
            *
        from
            (
                select
                    sw.Switch_ID,
                    sw.Name,
                    sd.Interface_name,
                    sd.Neighbor_instance_ID
                from
                    Switch sw
                    inner join Switch_DiractMAC sd on sd.Sw_ID = sw.Switch_ID
            ) as k
    ) as z on z.Neighbor_instance_ID = y.Instance_ID
WHERE
    DATE(y.insert_time) = DATE_SUB(CURDATE(), INTERVAL 0 DAY)
order by
    y.Service_name