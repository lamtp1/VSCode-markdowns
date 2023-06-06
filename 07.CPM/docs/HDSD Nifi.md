> Dùng PutDatabaseRecord processor trong nifi thì khi insert data vào, id của bảng sẽ không tự sinh như khi dùng python với thư viện mysql-connector-python. Bị lỗi khi insert: không có id_table trong kết quả câu query dùng để insert.

> Phải có primary key mới insert được, thông thường primary key sẽ là id_table nhưng do ko có id_table sẵn trong kết quả query nên phải dùng trường khác.

> Câu sql không có dấu `;` ở cuối.