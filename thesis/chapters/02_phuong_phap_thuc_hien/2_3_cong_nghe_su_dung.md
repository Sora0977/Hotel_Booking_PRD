---
status: imported_chunk
last_updated: 2026-05-21
chapter: "02 - Phương pháp thực hiện"
chunk: "2.3"
source_file: "../02_phuong_phap_thuc_hien.md"
related_memory: ../../THESIS_MEMORY.md
school_rules: ../../SCHOOL_RULES.md
---
<!-- Mảnh file được tạo từ 02_phuong_phap_thuc_hien.md. Theo MEGA-DOCUMENT PROTOCOL, chỉnh sửa mặc định phải thực hiện tại mảnh này, không chỉnh file chương gốc. -->

## 2.3 Công nghệ sử dụng

### 2.3.1 Phía Frontend

React.js: Là một thư viện JavaScript mạnh mẽ do Facebook phát triển, được sử dụng để xây dựng giao diện người dùng (UI) theo kiến trúc dựa trên các thành phần (component). Điều này giúp mã nguồn được tái sử dụng cao, dễ quản lý và bảo trì.

React Router: Thư viện được sử dụng để quản lý việc định tuyến (routing) phía client, cho phép tạo ra một ứng dụng đơn trang (Single-Page Application - SPA) với trải nghiệm điều hướng mượt mà giữa các trang khác nhau mà không cần tải lại toàn bộ trang web.

Tailwind CSS: Là một framework CSS theo triết lý "utility-first", cung cấp các lớp tiện ích cấp thấp để xây dựng giao diện một cách nhanh chóng và tùy biến cao trực tiếp trong mã HTML/JSX. Toàn bộ giao diện của dự án được tạo kiểu bằng Tailwind CSS.

Axios: Là một thư viện HTTP client dựa trên Promise, được sử dụng để thực hiện các yêu cầu API từ frontend đến backend một cách dễ dàng và mạnh mẽ. Axios được cấu hình để tự động đính kèm token xác thực vào mỗi yêu cầu.

### 2.3.2 Phía Backend

#### 2.3.2.1 Java

Ngôn ngữ lập trình Java là một ngôn ngữ hướng đối tượng, được sử dụng rộng rãi trong việc phát triển phần mềm, trang web, game và ứng dụng di động. Một trong những tiêu chí quan trọng của Java là “Viết một lần, thực thi khắp nơi” (Write once, run anywhere), có nghĩa là chương trình viết bằng Java có thểchạy trên nhiều nền tảng khác nhau.

Java có nhiều đặc điểm nổi bật, bao gồm:

- Tương tự C++, nhưng dễ học và sử dụng hơn.

- Độc lập với phần cứng và hệ điều hành, cho phép chương trình chạy tốt trên nhiều môi trường.

- Ngôn ngữ thông dịch, có nghĩa là mã nguồn được biên dịch thành bytecode, sau đó bytecode được môi trường thực thi chạy.

- Cơ chế thu gom rác tự động, giúp loại bỏ các đối tượng không sử dụng và tiết kiệm bộ nhớ.

- Đa luồng, cho phép thực hiện nhiều tác vụ cùng một lúc.

- Tính an toàn và bảo mật cao.

- Java cũng được sử dụng để phát triển nhiều loại ứng dụng khác nhau, từ ứng dụng web, desktop cho đến mobile

#### 2.3.2.2 Spring Boot

- Spring Boot là một dự án con của framework Spring, được thiết kế để giúp phát triển ứng dụng Java một cách nhanh chóng và dễ dàng. Dưới đây là một số đặc điểm nổi bật và tính ưu việt của Spring Boot:

- Thuận tiện cấu hình (Convenient configuration): Spring Boot giúp tựđộng cấu hình môi trường ứng dụng một cách đơn giản thông qua việc sử dụng các giá trị mặc định và các cấu hình thông minh. Điều này giảm đáng kể khối lượng công việc cần thiết cho việc cấu hình.

- Embeddable web server: Spring Boot đi kèm với các web server như Tomcat, Jetty hoặc Undertow được tích hợp sẵn trong ứng dụng, giảm thiểu sự phức tạp trong việc triển khai ứng dụng.

- Dependency Injection (DI): Spring Boot sử dụng cơ chế DI mạnh mẽ của Spring Framework, giúp quản lý và tự động kết nối các thành phần của ứng dụng

- Standalone: Ứng dụng Spring Boot có thể chạy độc lập mà không cần các cấu hình phức tạp, điều này giúp tiết kiệm thời gian và công sức khi triển khai.

- Tích hợp tốt với Spring Ecosystem: Spring Boot tương thích và tích hợp tốt với nhiều dự án khác của Spring như Spring Data, Spring Security, Spring Cloud, giúp phát triển ứng dụng một cách linh hoạt và mạnh mẽ.

- Tự động cập nhật Dependency: Spring Boot hỗ trợ tính năng tự động cập nhật các phiên bản dependency, giúp dễ dàng duy trì và cập nhật ứng dụng.

- Annotation-Based configuration: Sử dụng các chú thích (annotation) để cấu hình thay vì sử dụng các file cấu hình XML, giúp mã nguồn trở nên gọn gàng và dễ đọc.

- Microservices development: Spring Boot được sử dụng rộng rãi trong phát triển ứng dụng dạng Microservices do tính linh hoạt và dễ triển khai. Những đặc điểm này khiến Spring Boot trở thành một lựa chọn phổ biến trong cộng đồng phát triển Java, đặc biệt là cho việc xây dựng các ứng dụng web, dịch vụ và các hệ thống phức tạp.

#### 2.3.2.3 MySQL

- MySQL là một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) mã nguồn mở, phổ biến và mạnh mẽ. Dưới đây là một số điểm nổi bật về MySQL:

- Mã nguồn mở: MySQL được phát triển và duy trì dưới dạng mã nguồn mở, cho phép người dùng tự do sử dụng, tùy chỉnh và phân phối lại theo các điều khoản của Giấy phép Công cộng GNU (GPL).

- Hiệu suất cao: MySQL được tối ưu hóa để cung cấp hiệu suất cao trong việc xử lý các truy vấn và giao tiếp với cơ sở dữ liệu, làm cho nó trở thành lựa chọn phổ biến cho các ứng dụng yêu cầu xử lý dữ liệu nhanh chóng.

- Đa nền tảng: MySQL hỗ trợ nhiều nền tảng, có thể chạy trên nhiều hệ điều hành như Linux, Windows, macOS, và nhiều loại kiến trúc khác nhau.

- Tính an toàn và bảo mật: MySQL cung cấp các tính năng an toàn và bảo mật như quản lý người dùng, phân quyền, mã hóa dữ liệu, và khả năng sao lưu và khôi phục dữ liệu.

- Dễ sử dụng: MySQL có một cộng đồng lớn và tích hợp nhiều công cụ quản lý cơ sở dữ liệu như MySQL Workbench, giúp người quản trị và phát triển dễ dàng tương tác với cơ sở dữ liệu

- Hỗ trợ chuẩn SQL: MySQL tuân thủ chuẩn SQL, giúp người phát triển dễ dàng chuyển đổi giữa các hệ thống quản trị cơ sở dữ liệu hỗ trợ SQL mà không gặp nhiều vấn đề tương thích.

- Phù hợp với ứng dụng nhỏ đến lớn: Từ các ứng dụng web nhỏ đến các hệ thống doanh nghiệp lớn, MySQL phù hợp với mọi quy mô ứng dụng.

- MySQL là một giải pháp đáng tin cậy và linh hoạt cho việc quản lý cơ sở dữ liệu, và sự phổ biến của nó đã đưa MySQL trở thành một trong những hệ quản trị cơ sở dữ liệu hàng đầu trên thế giới
