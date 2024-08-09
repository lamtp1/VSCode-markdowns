SELECT
    'VTN_CNTT_BSS_074' app_code,
    v2.date2 update_time,
    CASE
        WHEN v1.baduser IS NULL THEN ROUND (0 / v2.total * 100, 2) ---xu ly logic tu so null tra ra gia tri 0 cho KQI
        ELSE ROUND (v1.baduser / v2.total * 100, 2)
    END kqi,
    CASE
        WHEN v1.baduser IS NULL THEN 0
        ELSE v1.baduser
    END user_fail,
    v2.total users
FROM
    (
        SELECT
            COUNT (*) baduser,
            date1
        FROM
            (
                SELECT
                    user_call,
                    COUNT (*),
                    TRUNC (import_time) date1
                FROM
                    (
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name in (
                                'saleForMobile',
                                'reportChannelCareDetailBusiness',
                                'updateStaff',
                                'doUpdateCustomer.DKTT'
                            )
                            AND (
                                duration >= 10000
                                or result_value like '%Exception%'
                            ) --giao dich fail do vuot nguong responsetime hoac co ma loi
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name in (
                                'updateLocation',
                                'countVisitedNumber',
                                'changePass',
                                'activeAccountAgent',
                                'searchAccount',
                                'getAccountBookBankPlusInfo'
                            )
                            AND (
                                duration >= 5000
                                or result_value like '%Exception%'
                            )
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name in (
                                'reportChannelCareBusiness',
                                'searchCustIdentity',
                                'approveOrderStaff'
                            )
                            AND (
                                duration >= 6000
                                or result_value like '%Exception%'
                            )
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name = 'searchIsdn'
                            AND (
                                duration >= 9000
                                or result_value like '%Exception%'
                            )
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name = 'connectMobilePostPaid'
                            AND (
                                duration >= 13000
                                or result_value like '%Exception%'
                            )
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name = 'connectMobilePrePaid'
                            AND (
                                duration >= 13000
                                or result_value like '%Exception%'
                            )
                        union
                        ALL
                        SELECT
                            import_time,
                            user_call,
                            method_name,
                            duration
                        FROM
                            mbccs.log_method
                        WHERE
                            1 = 1
                            AND import_time >= ?
                            AND import_time < ?
                            AND method_name in (
                                'reportChannelCareBusinessAllProvince',
                                'loginEnd'
                            )
                            AND (
                                duration >= 22000
                                or result_value like '%Exception%'
                            )
                    )
                GROUP BY
                    user_call,
                    TRUNC (import_time)
                HAVING
                    COUNT (*) >= 2
            )
        GROUP BY
            date1
    ) v1
    RIGHT JOIN (
        SELECT
            COUNT (DISTINCT (user_call)) total,
            TRUNC (import_time) date2
        FROM
            mbccs.log_method
        WHERE
            1 = 1
            AND import_time >= ?
            AND import_time < ?
        GROUP BY
            TRUNC (import_time)
    ) v2 ON v1.date1 = v2.date2
ORDER BY
    date1 ASC