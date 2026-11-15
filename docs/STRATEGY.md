# FyndRadar: chiến lược sản phẩm, kỹ thuật và kinh doanh

*Cập nhật 2026-11-15*

## 1. Định vị

Thị trường Bắc Âu đã có so sánh giá hàng mới (Prisjakt, PriceRunner), chợ đồ cũ giữa cá nhân (Blocket, Tradera, Finn, DBA) và sàn giá rẻ (Fyndiq). Khoảng trống FyndRadar nhắm vào là **hàng "cơ hội thứ hai" do chính nhà bán lẻ bán**: outlet, demo, mở hộp, hàng trả lại, B-stock, refurbished. Loại hàng này có bảo hành và quyền đổi trả như hàng mới (Elgiganten, Proshop, Thomann đều nói rõ điều đó trên trang của họ), nhưng nằm rải rác trong các mục "Fyndhörnan", "Outlet", "Demovarer" mà người mua phải tự lục từng trang.

Lời hứa với người dùng: *mở một trang, thấy ngay hàng thật gần mình hoặc giao tận nhà, giá thật, mức giảm thật, link thẳng tới sản phẩm.*

Lợi thế cạnh tranh cần xây:
1. **Độ phủ outlet** mà bên so sánh giá không ưu tiên (mỗi món outlet thường là một chiếc duy nhất, tồn tại vài giờ đến vài ngày).
2. **Tốc độ**: cảnh báo ngay khi món khớp bộ lọc xuất hiện. Đây là thứ người săn hàng sẵn sàng trả tiền.
3. **Chuẩn hoá tình trạng hàng** đa ngôn ngữ (open_box, demo, returned, replacement, used...) để so sánh được giữa các nhà bán lẻ.
4. **Lịch sử giá** từng món, chứng minh mức giảm là thật.

## 2. Nguồn dữ liệu và tính hợp pháp

Thứ tự ưu tiên:
1. **Affiliate feed** (Adtraction, Awin, Partner-ads, Tradedoubler): dữ liệu theo hợp đồng, có link hoa hồng sẵn. Sạch nhất về pháp lý và là nguồn doanh thu. Rào cản: phải được từng nhà bán lẻ duyệt, nhiều feed chứa toàn bộ catalogue nên pipeline lọc lại phần outlet (đã làm).
2. **Dữ liệu công khai có cấu trúc** (schema.org JSON-LD trên trang sản phẩm, sitemap): nhà bán lẻ đặt nó ra để máy đọc. Đọc với tần suất thấp, tôn trọng robots.txt, có User-Agent nhận diện, chỉ lấy dữ kiện (tên, giá, tình trạng, link).
3. **HTML công khai** (như Inet Fyndhörnan): chỉ khi 1 và 2 chưa có, cùng các nguyên tắc trên.
4. **Trình duyệt headless** cho trang render bằng JavaScript (Elgiganten/Elkjøp, Komplett): chỉ sau khi đọc điều khoản từng site; ưu tiên xin feed hoặc hợp tác trực tiếp.

Lưu ý pháp lý (không phải tư vấn luật, nên hỏi luật sư trước khi mở rộng):
- EU có quyền sui generis với cơ sở dữ liệu: không sao chép phần "đáng kể" của database một nhà bán lẻ. Chỉ lấy mục outlet, dẫn link về họ, không dựng lại catalogue của họ.
- Điều khoản sử dụng của từng site có thể cấm crawl tự động; affiliate feed giải quyết điều này.
- Hiển thị giá: luôn ghi thời điểm đọc và yêu cầu người dùng kiểm tra tại cửa hàng. "Giá thường" là giá do nhà bán lẻ công bố, không tự tính.
- Không có dữ liệu cá nhân trong pipeline. Khi thêm tài khoản và cảnh báo email cần chính sách GDPR.
- Link affiliate phải được công bố rõ (đã có trong footer).

## 3. Mô hình kinh doanh

| Dòng thu | Khi nào | Ghi chú |
|---|---|---|
| Hoa hồng affiliate | Ngay khi có feed được duyệt | Thu nhập theo đơn hàng; mức hoa hồng khác nhau theo chương trình |
| FyndRadar Pro (thuê bao) | Khi có ~1 000 người dùng quay lại hàng tuần | Cảnh báo tức thì (push/email/Telegram), bộ lọc không giới hạn, lịch sử giá, xuất CSV |
| Gói Reseller | Song song với Pro | Ước tính biên lợi nhuận bán lại so với giá đã bán trên Blocket/Tradera; lọc kiểu "giá vốn dưới 10 000 kr, lãi trên 1 000 kr" theo vùng |
| B2B cho nhà bán lẻ | Khi có lưu lượng đáng kể | Vị trí nổi bật cho hàng tồn outlet, báo cáo xu hướng hàng trả lại theo danh mục |

Gói Reseller là phần anh có lợi thế riêng: anh đã tự đặt tiêu chí arbitrage, nên có thể dùng FyndRadar cho chính mình trước, chứng minh lợi nhuận thật, rồi bán công cụ.

## 4. Kiến trúc hiện tại và lộ trình mở rộng

Giai đoạn 0 (đã xây, 0 kr/tháng): Python thuần thư viện chuẩn, GitHub Actions chạy mỗi 3 giờ, SQLite lưu lịch sử giá, xuất JSON tĩnh, GitHub Pages phục vụ frontend. Không máy chủ, không phí.

Giai đoạn 1 (khi có cảnh báo và tài khoản): Cloudflare Workers + D1 hoặc một VPS nhỏ cho API cảnh báo; crawler giữ nguyên. Tần suất tăng lên mỗi 15 đến 30 phút cho nguồn "nóng".

Giai đoạn 2: worker trình duyệt headless cho các site render bằng JS, khớp sản phẩm theo GTIN giữa các nhà bán lẻ, tìm kiếm full-text phía máy chủ khi vượt ~20 000 listing.

## 5. Lộ trình 90 ngày

1. **Tuần 1**: tạo repo GitHub, bật Pages, chạy crawl thật lần đầu, chỉnh selector Inet/Proshop theo HTML thực tế. Mua tên miền.
2. **Tuần 1 đến 3**: đăng ký publisher Adtraction (SE/NO/DK), Awin, Partner-ads (DK). Xin feed từ nhà bán lẻ có mục outlet.
3. **Tuần 3 đến 6**: cảnh báo email/Telegram cho bộ lọc đã lưu (bản miễn phí giới hạn). Trang SEO theo danh mục và thành phố ("outlet TV Göteborg").
4. **Tuần 6 đến 12**: worker headless cho Elgiganten/Elkjøp/Power nếu điều khoản cho phép; gói Pro/Reseller bản beta; đo tỉ lệ click ra cửa hàng và doanh thu affiliate.

Chỉ số cần theo dõi: số listing đang hoạt động theo nguồn, tỉ lệ crawl thành công (đã có trong meta.json), người dùng quay lại hàng tuần, click ra cửa hàng, doanh thu affiliate trên mỗi nghìn lượt xem.

## 6. Việc cần anh làm (không tự làm thay được)

1. **GitHub**: tạo repo `fyndradar` và đẩy code lên (hoặc cho em quyền push), bật Settings > Pages > Source: GitHub Actions. Site sẽ chạy ở `https://<tên-github>.github.io/fyndradar/`.
2. **Affiliate**: đăng ký tài khoản publisher. Cần thông tin công ty (có thể dùng The Coffee Connections hoặc lập AB mới), website (dùng link GitHub Pages tạm) và tài khoản ngân hàng.
3. **Tên miền**: kiểm tra và mua (ví dụ fyndradar.se, .com, .dk, .no).
4. **Tuỳ chọn**: nếu muốn em chạy crawl thật ngay trong phiên này, cho phép các tên miền nhà bán lẻ trong Settings > Capabilities của Claude.
