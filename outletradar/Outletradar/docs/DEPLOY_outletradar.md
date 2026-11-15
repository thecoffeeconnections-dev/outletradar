# Đưa OutletRadar lên outletradar.se

## 1. GitHub
1. Tạo tài khoản GitHub (nếu chưa có), tạo repo **công khai** tên `outletradar`.
2. Giải nén `fyndradar.zip`, tải toàn bộ nội dung thư mục `fyndradar/` lên repo (Add file > Upload files), commit.
3. Settings > Pages > Source: chọn **GitHub Actions**.
4. Actions > "crawl-and-deploy" > Run workflow. Lần chạy đầu khoảng 5-10 phút.
5. Settings > Pages > Custom domain: nhập `outletradar.se`, Save.

## 2. DNS ở one.com (Kontrollpanel > outletradar.se > DNS-inställningar)
Xoá các bản ghi A / AAAA mặc định của one.com cho `@`, rồi thêm:

| Typ | Värd | Värde |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | TEN-GITHUB-CUA-ANH.github.io |

DNS có thể mất từ vài phút đến 24 giờ. Khi GitHub báo "DNS check successful", tích **Enforce HTTPS**.

## 3. Sau khi trang chạy
- Đăng ký publisher Adtraction và Awin, khai kênh `https://outletradar.se`.
- Feed được duyệt: Settings > Secrets and variables > Actions > New secret (`ADTRACTION_FEED_URL_1`, `AWIN_FEED_URL_1`...).
