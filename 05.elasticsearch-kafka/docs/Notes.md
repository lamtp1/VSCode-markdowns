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