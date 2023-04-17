- Các nodes trong Elasticsearch mặc định vừa là `ingest` vừa là `coordinating` node, có khả năng transform docs để đánh index và cân bằng tải.

<h2 style="color:gold">Zookeepr ports</h2>

Giả sử bạn có 3 server cho zookeepr ... Bạn cần đề cập trong cấu hình như sau:

    clientPort=2181
        server.1=zookeeper1:2888:3888
        server.2=zookeeper2:2888:3888
        server.3=zookeeper3:2888:3888

Trong số những server này, một server sẽ là `Master` và tất cả còn lại sẽ là `Slave`.

Server lắng nghe trên ba cổng: 2181 cho các kết nối máy Client; 2888 cho các kết nối follower, nếu Kafka trên server này đóng vai trò là `Master` ; và 3888 cho các kết nối với Server khác trong giai đoạn tiến cử `Master`.

## ` Elasticsearch documents`

elasticsearch documents cũng tương tự row (record) trong CSDL rdbms thường gặp

![elasticsearch_row](../img/elasticsearch_row.png)

## ` Đối chiếu Elasticsearch và SQL`

![elasticsearch_mapping](../img/elasticsearch_mapping.png)

>phần quan trong của mỗi dự án là khả năng truy cập cơ sở dữ liệu. `INDEXING` là quá trình giúp ta có thể có kết quả từ Database một cách hiệu quả

>*Càng nhiều Elasticsearach node thì tốc độ tìm kiếm càng nhanh và tăng khả năng lưu trữ của Cluster*

>Băng thông (Bandwidth): ảnh hưởng đến khả năng truyền dữ liệu giữa các node trong Cluster

>Các node elasticsearch có 2 network interfaces, một cho client gửi request tới API của ES qua `HTTP interface`, một cho các node trong cluster giao tiếp với nhau thông qua `transport interface`.

>Chúng ta có thể phân phối docs thông qua các shard. Shards chia số lượng lớn các docs thành các pieces và để chúng được xử lý bởi các node khác nhau. Chúng ta không thể configure để dữ liệu đc gửi đến một node nhất định, nhưng ta có thể config để store một nhóm các data tương tự vào một shard bằng routing.

>` Lý do phải chia thành các shard:` Shards là đơn vị mà Elasticsearch phân phối dữ liệu trong Cluster. Tốc độ mà Elasticsearch có thể di chuyển các shard khi cân bằng lại dữ liệu (rebalancing data), ví dụ: sau một lỗi, sẽ phụ thuộc vào kích thước và số lượng shard cũng như hiệu suất mạng và ổ đĩa.

>` Lý do phải chia thành các segment:` 




## *Đa phần index trong elastic của hệ thống log tt là shrink index (80%)* 

Lệnh check xem port này đang chạy exporter gì

        curl –XGET http://10.254.138.3:20451/metrics

đây là check exporter của ES, còn Kafka và zk là port 20551 và 20651

còn port 20125 khi dùng docker ps -a là port của docker exporter mình tự thêm

![exporter1](../img/exporter1.jpg)

lệnh hiển thị các exporter 

        ps -ef | grep exporter


sau đó dùng kill -15 [PID] để kill exporter process 

kiểm tra lại file /var/log/td-agent/BCCS Payment.pos để xem đã đẩy log lên chưa.

- Trường Start_time: là thời điểm có người tác động vào DLNC.
- Trường End_time: là thời điểm kết thúc tác động vào DLNC.

` * Lưu ý khi tạo index trên Log tập trung`
`I.` Các bước cần làm phía đẩy log
1. Kiểm tra môi trường trước khi cài đặt td-agent (HĐH)
2. install agent theo HD v10 (gửi format log, log mẫu cho người ta cấu hình - file cem.txt)
3. Gửi log cho mình để xem đã đúng chuẩn (33 trường vs UD thường, 15 với log tổng đài, các trường Start/End_time chuẩn iso 8601)
4. Làm PYC mở kết nối (đã lưu mail) tới log tt
5. Báo lại khi log đã đúng chuẩn và gửi lên.

`II.` Các bước cần làm phía nhận log
1. Tạo topic cho hệ thống.
2. Kiểm tra Log đã lên kafka = lệnh kafka consumer, nếu log sai trường Start/End_time mà đơn vị vẫn muốn log lên bằng được => tạo index template theo HD rồi lên elastic sửa lại phần mapping thay type của trường Start/End_time từ Date => text.
3. Tạo kafka connect (phải tạo connect sau index template để tránh elastic tự tạo 1 default index gồm 1 primary shard và 1 replica shard khi kafka connect đẩy log)
4. Kiểm tra trên elastic xem đã tồn tại indices chưa: Management/Stack Management/Data/index management/indices.
5. Tạo chart để view: ../index management/Kibana/index patterns.

`III. ` Các lỗi hay gặp và lưu ý:

1. Quên chưa sửa template từ date -> text nhưng vẫn có 1 indice chuẩn gồm 8 primary shard - 1 replica shard, tuy nhiên indices này ko có log hoặc có 1 hoặc 2 log. 
==> chỉnh lại Start/End_time của template này thành type text. Sau đó xóa indice cũ rồi F5 xem có log chưa. 
` * Trường start time quan trọng và phải chuẩn do là thời điểm tác động vào dữ liệu nhạy cảm, cần trường này để trace vết. `

2. Log của 16 hệ thống VTT ban đầu để sai Start/End_time => phải lưu tạm dưới dạng text => cần sửa lại để tháng sau lưu định dạng mới. Hiện tại Log của VTT đang dùng policy riêng, sau 1 tháng là xóa log. Nếu index_template ban đầu lưu Start time dạng text sau đó sửa thành date => log mới lên sẽ KHÔNG ăn theo template mới này mà vẫn lưu dưới dạng cũ (Kể cả Datetime đúng chuẩn thì lên elastic Discover log vẫn là dạng text) trừ khi xóa index hiện tại đi thì mới ăn theo định dạng mới. 

![StartTime](../img/StartTime.png)

==> làm vậy sẽ mất log, đằng nào 1 tháng nữa cx bị delete nên sửa trước template và đợi log cũ bị rotate và ăn theo template mới