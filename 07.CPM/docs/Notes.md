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

 ### 1. Thêm user vào group docker và sudo

- Để thêm user vào docker group thì chạy lệnh sau

        usermod -aG docker vt_admin

- Để thêm user vào sudoers group thì dùng lệnh tương tự, thay `docker` = `sudo`, hoặc vào file `visudo` :

        sudo visudo

Thêm user mình muốn thêm vào đoạn dưới:

![cpm_note1](../img/cpm_note1.png)

### 2. Fix lỗi docker service không start được:

- Vào file daemon.json ở /etc/docker để sửa, sao cho format giống như hình dưới:

        vim /etc/docker/daemon.json

![cpm_note2](../img/cpm_note2.png)

Sau đó nhớ save file và restart lại docker.

`Lưu ý:` user thực hiện các lệnh trên là user root 

### Copy tất cả file từ một directory đến 1 directory khác:

                shopt -s dotglob
                cp source_folder/* /path/to/destination_folder/

Lệnh `shopt -s dotglob` sẽ copy được cả file ẩn (bắt đầu bằng dấu chấm: .env)

Từ IP compute --> IP instance --> ID instance --> Device ID --> IP MGT, serial

## Cài phần mềm không cần user vanphong:

1. Rút dây mạng (nếu không muốn bị ăn ticket ATTT)
2. Cắm usb cài win mini vào và vào BIOS (F9, F12) rồi chọn usb.
3. Tìm kiếm từ khóa password
4. Sau đó chọn ổ cài win (ổ C), và bỏ tích phần `disabled user` và tích `clear user password` để unlock user bởi bình thường kaspersky sẽ quét toàn bộ user trong ổ (trong đó có admin) và disabled tất, trừ user lamtp1, vì vậy trước đấy phải ngắt dây mạng để kaspersky không quét. clear password để khi đăng nhập bằng user admin thì sẽ không bị hỏi password.
5. Restart máy. 
6. Login lại bằng user admin: nhập `.\administrator`
7. Cài đặt phần mềm muốn cài.
8. Switch user lamtp1 và tận hưởng. Nếu vẫn chưa cắm dây mạng thì vẫn switch sang user admin mà không cần nhập password được