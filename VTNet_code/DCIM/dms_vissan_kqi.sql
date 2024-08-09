SELECT
    'VTN_CNTT_MSS_215' app_code,
    IFNULL(v1.date1, DATE(SYSDATE())) update_time,
    IFNULL(round(v1.baduser / v2.tong * 100, 2), 0) as KQI,
    IFNULL(v1.baduser, 0) user_fail,
    IFNULL(v2.tong, 0) users
from
(
        select
            count(b2.USER_NAME) baduser,
            b2.date1
        FROM
(
                select
                    user_name,
                    count(1) solan,
                    DATE(start_time) as date1
                FROM
                    (
                        SELECT
                            'VTN_CNTT_MSS_215' APP_NAME,
                            DATE(a.StartTime) START_TIME,
                            a.UserName USER_NAME,
                            a.ActionName URL_REQUEST,
                            a.Duration,
                            a.TransactionStatus RESPONSE_CODE
                        FROM
                            actionaudits a
                        WHERE
                            a.ActionName = 'AuthModule.Login'
                            AND a.Duration > 5000
                            AND a.TransactionStatus = 1
                            AND TO_DAYS(a.StartTime) >= ?
                            AND TO_DAYS(a.StartTime) < ?
                        UNION
                        ALL
                        SELECT
                            'VTN_CNTT_MSS_215' APP_NAME,
                            DATE(a.StartTime) START_TIME,
                            a.UserName USER_NAME,
                            a.ActionName URL_REQUEST,
                            a.Duration,
                            a.TransactionStatus RESPONSE_CODE
                        FROM
                            actionaudits a
                        WHERE
                            a.ActionName = 'BookCategoryModule.Search'
                            AND a.Duration > 10000
                            AND a.TransactionStatus = 1
                            AND TO_DAYS(a.StartTime) >= ?
                            AND TO_DAYS(a.StartTime) < ?
                        UNION
                        ALL
                        SELECT
                            'VTN_CNTT_MSS_215' APP_NAME,
                            DATE(a.StartTime) START_TIME,
                            a.UserName USER_NAME,
                            a.ActionName URL_REQUEST,
                            a.Duration,
                            a.TransactionStatus RESPONSE_CODE
                        FROM
                            actionaudits a
                        WHERE
                            a.ActionName = 'eDoc_SigningBookModule_Create'
                            AND a.Duration > 10000
                            AND a.TransactionStatus = 1
                            AND TO_DAYS(a.StartTime) >= ?
                            AND TO_DAYS(a.StartTime) < ?
                        UNION
                        ALL
                        SELECT
                            'VTN_CNTT_MSS_215' APP_NAME,
                            DATE(a.StartTime) START_TIME,
                            a.UserName USER_NAME,
                            a.ActionName URL_REQUEST,
                            a.Duration,
                            a.TransactionStatus RESPONSE_CODE
                        FROM
                            actionaudits a
                        WHERE
                            a.ActionName = 'StatisticsReportModule.ExportExcelDetailSign'
                            AND a.Duration > 10000
                            AND a.TransactionStatus = 1
                            AND TO_DAYS(a.StartTime) >= ?
                            AND TO_DAYS(a.StartTime) < ?
                        UNION
                        ALL
                        SELECT
                            'VTN_CNTT_MSS_215' APP_NAME,
                            DATE(a.StartTime) START_TIME,
                            a.UserName USER_NAME,
                            a.ActionName URL_REQUEST,
                            a.Duration,
                            a.TransactionStatus RESPONSE_CODE
                        FROM
                            actionaudits a
                        WHERE
                            a.ActionName = 'RoleModule.Create'
                            AND a.Duration > 5000
                            AND a.TransactionStatus = 1
                            AND TO_DAYS(a.StartTime) >= ?
                            AND TO_DAYS(a.StartTime) < ?
                    ) b
                GROUP BY
                    b.USER_NAME,
                    b.START_TIME
                HAVING
                    count(1) >= 2
            ) b2
        GROUP BY
            b2.date1
    ) v1
    RIGHT JOIN(
        select
            COUNT(distinct(USERNAME)) tong,
            DATE(StartTime) AS date2
        FROM
            actionaudits
        where
            StartTime >= ?
            and DATE(StartTime) < ?
            and ActionName in(
                'BookCategoryModule.Search',
                'SigningBookModule.Create',
                'StatisticsReportModule.ExportExcelDetail'
            )
        group by
            TO_DAYS(StartTime)
    ) v2 ON v1.date1 = v2.date2
order by
    v1.date1 asc