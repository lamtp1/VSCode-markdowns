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
