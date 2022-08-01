Redis dựa trên ý tưởng một cache cũng có thể là một database ổn định với mục đích là có thể gửi dữ liệu tới người dùng nhanh hơn RDBMS làm được, tạo ra một hệ thống mà dữ liệu có thể được modified trên RAM, nhanh hơn nhiều so với cách làm truyền thống là lấy trên ổ cứng, cùng lúc ấy nó sẽ lưu dữ liệu trên ổ cứng.

mỗi datapoint trong db là một key, theo sau là các kiểu cấu trúc như string, bitmap, bitfield, hash, list

dùng làm cache để khiến relational db nhanh hơn. tuy nhiên redis hoàn toàn phù hợp để làm một primary db và giảm đáng kể sự phức tạp bởi làm cho mọi thứ hoạt động nhanh hơn ở quy mô lớn là lý do ban đầu gây ra sự phức tạp, còn với redis thì db của bạn đã nhanh sẵn rồi, không cần phải tạo một lớp caching phức tạp