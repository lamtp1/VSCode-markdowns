## Cách fix lỗi Connect timeout khi cài agent dạng docker trên centos 6 (6.6)

1. Sửa docker-compose phần `net` từ `bridge` sang `host` như sau:

![host](../img/host.png)

2. Xóa bất kỳ container cũ nào nếu còn:

        docker stop [container_name/id]

        docker rm [container_name/id]

3. Xóa image cũ để tránh docker-compose sẽ tự lấy image cũ nó vừa build vì có tag (latest) như nhau. Image cũ có thể sẽ không có thông tin định thêm trong Dockerfile

        docker rmi [image_id]

4. Build lại:

        docker-compose up -d


## Cách thêm gói vào trong container khi cài agent dạng docker trên centos 6 (6.6)

1. Copy package (vd:traceroute.dpkg) định cài vào thư mục gem đã giải nén trong hướng dẫn, do hệ điều hành trong container là debian nên cài gói dpkg.

![gem](../img/gem.png)

2. Sửa Dockerfile như trên để run container bằng user root trong container, phải chạy = root thì mới cài được gói và dùng lệnh được:

![Dockerfile1](../img/Dockerfile1.png)

` Lưu ý `: nhớ chỉnh lại user root = fluent khi test xong kẻo BO ứng dụng cho ăn hành

3. Xóa container và image cũ như HD trên.

4. Build lại

Sau khi build xong có thể tự do dùng user root trong container và su root container từ user UD bên ngoài host:

        docker exec -it -u 0 [container_name/id] bash

![traceroute_pkg](../img/traceroute_pkg.png)

