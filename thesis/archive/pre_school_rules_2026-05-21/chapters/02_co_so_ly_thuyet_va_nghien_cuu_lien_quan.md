---
status: imported
last_updated: 2026-05-21
chapter: "02 - Cơ sở lý thuyết và nghiên cứu liên quan"
related_memory: THESIS_MEMORY.md
source_chapters:
  - "Hotel booking service/Thesis-report/chapters/chuong-2-phuong-phap-thuc-hien.md"
---

# Chương 2 — Cơ sở lý thuyết và nghiên cứu liên quan

<!-- Nội dung dưới đây được nhập từ các mục 2.1 và 2.2 của chương 2 cũ. Các nhận định về hệ thống tương tự và công nghệ cần bổ sung nguồn trước khi dùng cho bản cuối. -->

## 2.1 Các hệ thống tương tự

Trong quá trình xây dựng website đặt phòng khách sạn theo mô hình Marketplace, việc nghiên cứu và phân tích các nền tảng hiện có là một bước quan trọng. Hoạt động này giúp nhận diện các ưu điểm cần học hỏi, các nhược điểm cần khắc phục và định hình chiến lược phát triển sản phẩm. Dưới đây là phần phân tích hai hệ thống tiêu biểu trong ngành là Booking.com và Traveloka, cả hai đều vận hành thành công mô hình Marketplace, kết nối hiệu quả khách hàng với các nhà cung cấp dịch vụ lưu trú.

### 2.1.1 Booking.com

Booking.com là một trong những nền tảng đặt phòng trực tuyến hàng đầu thế giới. Hoạt động dựa trên mô hình Marketplace, hệ thống cung cấp một danh mục đa dạng các loại hình lưu trú, từ khách sạn, căn hộ đến homestay trên phạm vi toàn cầu. Nguồn doanh thu chính của Booking.com đến từ việc thu phí hoa hồng (thường dao động từ 15-20%) trên mỗi giao dịch thành công từ các đối tác lưu trú.

Ưu điểm:

- Danh mục sản phẩm phong phú: Booking.com sở hữu một mạng lưới đối tác khổng lồ với hàng triệu lựa chọn lưu trú tại hơn 200 quốc gia, đáp ứng được hầu hết các phân khúc khách hàng, từ cao cấp đến bình dân.

- Công cụ tìm kiếm và bộ lọc hiệu quả: Giao diện tìm kiếm được thiết kế trực quan, cho phép người dùng dễ dàng lọc kết quả theo các tiêu chí như giá, tiện nghi, điểm đánh giá, và vị trí, mang lại trải nghiệm nhanh chóng và chính xác.

- Chính sách đặt/hủy phòng linh hoạt: Nền tảng hỗ trợ đa dạng các chính sách như hủy phòng miễn phí hoặc không hoàn tiền, cùng với tùy chọn thanh toán trực tuyến hoặc thanh toán tại nơi lưu trú, tối ưu hóa sự thuận tiện cho khách hàng.

- Hệ thống đánh giá đáng tin cậy: Chỉ những khách hàng đã hoàn tất quá trình đặt và sử dụng dịch vụ mới có quyền đánh giá, đảm bảo tính khách quan và xác thực của các nhận xét.

- Nền tảng quản lý đối tác chuyên nghiệp: Booking.com cung cấp hệ thống Extranet, một công cụ quản trị mạnh mẽ cho phép đối tác dễ dàng cập nhật tình trạng phòng, điều chỉnh giá và quản lý đơn đặt phòng.

Nhược điểm:

- Mức phí hoa hồng cao: Tỷ lệ hoa hồng từ 15-20% được xem là một thách thức tài chính đối với các cơ sở lưu trú quy mô nhỏ.

- Hạn chế trong việc địa phương hóa: Tại thị trường Việt Nam, hệ thống còn thiếu sự tích hợp các phương thức thanh toán phổ biến như VietQR hay ví điện tử MoMo.

- Mức độ cạnh tranh cao: Các đối tác nhỏ lẻ gặp khó khăn trong việc cạnh tranh và hiển thị nổi bật do thuật toán thường ưu tiên các chuỗi khách sạn lớn hoặc những đơn vị tham gia chương trình khách hàng thân thiết Genius.

- Trải nghiệm giao diện người dùng: Giao diện bị một số người dùng đánh giá là phức tạp và chứa quá nhiều thông tin, làm giảm tính thân thiện.

- Thiếu cơ chế kiểm soát gian lận: Hệ thống chưa có cơ chế chấm điểm và xử phạt công khai đối với các đối tác vi phạm chính sách (ví dụ: tự ý hủy đơn), dẫn đến nguy cơ không đồng đều về chất lượng dịch vụ.

- Hỗ trợ khách hàng chưa được tự động hóa: Việc thiếu chatbot để giải đáp tự động các câu hỏi về chính sách khiến khách hàng phải phụ thuộc vào các kênh hỗ trợ thủ công, có thể gây chậm trễ.

### 2.1.2 Traveloka

Traveloka là một nền tảng du lịch trực tuyến hàng đầu tại khu vực Đông Nam Á, được thành lập vào năm 2012. Tương tự Booking.com, Traveloka vận hành theo mô hình Marketplace, cung cấp các dịch vụ đặt phòng khách sạn, vé máy bay và các tiện ích du lịch khác. Nền tảng này tập trung mạnh vào các thị trường trọng điểm như Indonesia, Việt Nam và Thái Lan, với mức phí hoa hồng cho đối tác dao động từ 10-15%.

Ưu điểm:

- Am hiểu thị trường địa phương: Traveloka thể hiện sự thấu hiểu sâu sắc nhu cầu của người dùng Đông Nam Á thông qua việc hỗ trợ đa dạng ngôn ngữ, tiền tệ và các phương thức thanh toán quen thuộc như ví điện tử và chuyển khoản ngân hàng.

- Chương trình khuyến mãi và ưu đãi: Nền tảng thường xuyên triển khai các chương trình giảm giá, tích điểm thành viên và ưu đãi độc quyền để thu hút và giữ chân khách hàng.

- Giao diện thân thiện và tối giản: Thiết kế giao diện, đặc biệt là trên ứng dụng di động, được đánh giá là đơn giản và dễ sử dụng, phù hợp với cả những người dùng không thành thạo công nghệ.

- Dịch vụ hỗ trợ khách hàng hiệu quả: Traveloka cung cấp dịch vụ chăm sóc khách hàng 24/7 thông qua nhiều kênh (chat, điện thoại, email), đảm bảo giải quyết các vấn đề một cách nhanh chóng.

- Hệ thống quản lý đối tác tiện lợi: Đối tác có thể quản lý giá, tình trạng phòng và các đơn đặt chỗ một cách linh hoạt thông qua ứng dụng Partner chuyên biệt.

- Hỗ trợ đa dạng phương thức thanh toán: Nền tảng tích hợp nhiều cổng thanh toán từ nội địa đến quốc tế, mang lại sự thuận tiện tối đa cho người dùng.

Nhược điểm:

- Phạm vi hoạt động quốc tế còn giới hạn: Do tập trung chủ yếu vào thị trường Đông Nam Á, số lượng lựa chọn lưu trú tại các khu vực như châu Âu hay châu Mỹ còn khá hạn chế.

- Thiếu cơ chế đánh giá đối tác: Tương tự Booking.com, hệ thống thiếu một cơ chế chấm điểm và xếp hạng công khai để ghi nhận và xử lý các đối tác có hành vi gian lận hoặc chất lượng dịch vụ kém.

- Quy trình hỗ trợ còn thủ công: Việc giải đáp các thắc mắc về chính sách vẫn phụ thuộc vào nhân viên hỗ trợ, có thể dẫn đến tình trạng quá tải và chậm trễ trong các khung giờ cao điểm.

## 2.2 Công nghệ sử dụng

### 2.2.1 Phía Frontend

React.js: Là một thư viện JavaScript mạnh mẽ do Facebook phát triển, được sử dụng để xây dựng giao diện người dùng (UI) theo kiến trúc dựa trên các thành phần (component). Điều này giúp mã nguồn được tái sử dụng cao, dễ quản lý và bảo trì.

React Router: Thư viện được sử dụng để quản lý việc định tuyến (routing) phía client, cho phép tạo ra một ứng dụng đơn trang (Single-Page Application - SPA) với trải nghiệm điều hướng mượt mà giữa các trang khác nhau mà không cần tải lại toàn bộ trang web.

Tailwind CSS: Là một framework CSS theo triết lý "utility-first", cung cấp các lớp tiện ích cấp thấp để xây dựng giao diện một cách nhanh chóng và tùy biến cao trực tiếp trong mã HTML/JSX. Toàn bộ giao diện của dự án được tạo kiểu bằng Tailwind CSS.

Axios: Là một thư viện HTTP client dựa trên Promise, được sử dụng để thực hiện các yêu cầu API từ frontend đến backend một cách dễ dàng và mạnh mẽ. Axios được cấu hình để tự động đính kèm token xác thực vào mỗi yêu cầu.

### 2.2.2 Phía Backend

#### 2.2.2.1 Java

Ngôn ngữ lập trình Java là một ngôn ngữ hướng đối tượng, được sử dụng rộng rãi trong việc phát triển phần mềm, trang web, game và ứng dụng di động. Một trong những tiêu chí quan trọng của Java là “Viết một lần, thực thi khắp nơi” (Write once, run anywhere), có nghĩa là chương trình viết bằng Java có thểchạy trên nhiều nền tảng khác nhau.

Java có nhiều đặc điểm nổi bật, bao gồm:

- Tương tự C++, nhưng dễ học và sử dụng hơn.

- Độc lập với phần cứng và hệ điều hành, cho phép chương trình chạy tốt trên nhiều môi trường.

- Ngôn ngữ thông dịch, có nghĩa là mã nguồn được biên dịch thành bytecode, sau đó bytecode được môi trường thực thi chạy.

- Cơ chế thu gom rác tự động, giúp loại bỏ các đối tượng không sử dụng và tiết kiệm bộ nhớ.

- Đa luồng, cho phép thực hiện nhiều tác vụ cùng một lúc.

- Tính an toàn và bảo mật cao.

- Java cũng được sử dụng để phát triển nhiều loại ứng dụng khác nhau, từ ứng dụng web, desktop cho đến mobile

#### 2.2.2.2 Spring Boot

- Spring Boot là một dự án con của framework Spring, được thiết kế để giúp phát triển ứng dụng Java một cách nhanh chóng và dễ dàng. Dưới đây là một số đặc điểm nổi bật và tính ưu việt của Spring Boot:

- Thuận tiện cấu hình (Convenient configuration): Spring Boot giúp tựđộng cấu hình môi trường ứng dụng một cách đơn giản thông qua việc sử dụng các giá trị mặc định và các cấu hình thông minh. Điều này giảm đáng kể khối lượng công việc cần thiết cho việc cấu hình.

- Embeddable web server: Spring Boot đi kèm với các web server như Tomcat, Jetty hoặc Undertow được tích hợp sẵn trong ứng dụng, giảm thiểu sự phức tạp trong việc triển khai ứng dụng.

- Dependency Injection (DI): Spring Boot sử dụng cơ chế DI mạnh mẽ của Spring Framework, giúp quản lý và tự động kết nối các thành phần của ứng dụng

- Standalone: Ứng dụng Spring Boot có thể chạy độc lập mà không cần các cấu hình phức tạp, điều này giúp tiết kiệm thời gian và công sức khi triển khai.

- Tích hợp tốt với Spring Ecosystem: Spring Boot tương thích và tích hợp tốt với nhiều dự án khác của Spring như Spring Data, Spring Security, Spring Cloud, giúp phát triển ứng dụng một cách linh hoạt và mạnh mẽ.

- Tự động cập nhật Dependency: Spring Boot hỗ trợ tính năng tự động cập nhật các phiên bản dependency, giúp dễ dàng duy trì và cập nhật ứng dụng.

- Annotation-Based configuration: Sử dụng các chú thích (annotation) để cấu hình thay vì sử dụng các file cấu hình XML, giúp mã nguồn trở nên gọn gàng và dễ đọc.

- Microservices development: Spring Boot được sử dụng rộng rãi trong phát triển ứng dụng dạng Microservices do tính linh hoạt và dễ triển khai. Những đặc điểm này khiến Spring Boot trở thành một lựa chọn phổ biến trong cộng đồng phát triển Java, đặc biệt là cho việc xây dựng các ứng dụng web, dịch vụ và các hệ thống phức tạp.

#### 2.2.2.3 MySQL

- MySQL là một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) mã nguồn mở, phổ biến và mạnh mẽ. Dưới đây là một số điểm nổi bật về MySQL:

- Mã nguồn mở: MySQL được phát triển và duy trì dưới dạng mã nguồn mở, cho phép người dùng tự do sử dụng, tùy chỉnh và phân phối lại theo các điều khoản của Giấy phép Công cộng GNU (GPL).

- Hiệu suất cao: MySQL được tối ưu hóa để cung cấp hiệu suất cao trong việc xử lý các truy vấn và giao tiếp với cơ sở dữ liệu, làm cho nó trở thành lựa chọn phổ biến cho các ứng dụng yêu cầu xử lý dữ liệu nhanh chóng.

- Đa nền tảng: MySQL hỗ trợ nhiều nền tảng, có thể chạy trên nhiều hệ điều hành như Linux, Windows, macOS, và nhiều loại kiến trúc khác nhau.

- Tính an toàn và bảo mật: MySQL cung cấp các tính năng an toàn và bảo mật như quản lý người dùng, phân quyền, mã hóa dữ liệu, và khả năng sao lưu và khôi phục dữ liệu.

- Dễ sử dụng: MySQL có một cộng đồng lớn và tích hợp nhiều công cụ quản lý cơ sở dữ liệu như MySQL Workbench, giúp người quản trị và phát triển dễ dàng tương tác với cơ sở dữ liệu

- Hỗ trợ chuẩn SQL: MySQL tuân thủ chuẩn SQL, giúp người phát triển dễ dàng chuyển đổi giữa các hệ thống quản trị cơ sở dữ liệu hỗ trợ SQL mà không gặp nhiều vấn đề tương thích.

- Phù hợp với ứng dụng nhỏ đến lớn: Từ các ứng dụng web nhỏ đến các hệ thống doanh nghiệp lớn, MySQL phù hợp với mọi quy mô ứng dụng.

- MySQL là một giải pháp đáng tin cậy và linh hoạt cho việc quản lý cơ sở dữ liệu, và sự phổ biến của nó đã đưa MySQL trở thành một trong những hệ quản trị cơ sở dữ liệu hàng đầu trên thế giới
