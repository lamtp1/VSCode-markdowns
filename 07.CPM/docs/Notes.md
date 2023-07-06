## Chuyển file từ server này sang server kia:

        scp python.zip vt_admin@nifi02:/home/vt_admin

trong đó, `vt_admin@nifi02 ` là account và tên domain hoặc ip định copy sang, /home/vt_admin là thư mục sẽ paste file của host nifi02.

## Nén và giải nén:

- Nén file và tất cả thư mục con: zip -r [filename.zip] [file sẽ đc zip]

        zip -r python_1606.zip python

- Giải nén và ghi đè:

        unzip python_1606.zip

Chọn A nếu muốn ghi đè.

## Lệnh để chmod tất cả các file trong folder:

                find /path/to/folder -type f -exec chmod 775 {} \;

Trong đó:
 The {} is a placeholder that represents each file found, and \; indicates the end of the -exec command