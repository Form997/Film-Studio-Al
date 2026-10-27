# Đưa dự án lên GitHub của Form997

**Chưa tạo repository trên GitHub từ bộ phát hành này.** Cần tạo kho mới để tránh đụng các công trình `PCI`, `Vong-co`, `hai-dat-ai-academy`.

Tên đề xuất: `hai-dat-ai-film-studio`

## Máy tính có Git + GitHub CLI

Giải nén và mở terminal trong thư mục chứa README.md:

```bash
git init
git add .
git commit -m "feat: initialize HAI DAT AI Film Studio v0.1"
git branch -M main
gh auth login
gh repo create Form997/hai-dat-ai-film-studio --public --source=. --remote=origin --push
```

Lệnh `gh repo create` yêu cầu GitHub CLI đã cài và tài khoản có quyền tạo repo. Nếu dự án chưa được public, thay `--public` bằng `--private`.

## Không có GitHub CLI

1. Trên github.com, vào `+` → `New repository`; đặt tên `hai-dat-ai-film-studio` và tạo kho **trống** (không tạo README ở trang GitHub vì trong mã đã có).
2. Trong terminal ở thư mục đã giải nén:

```bash
git init
git add .
git commit -m "feat: initial Vietnam-first film studio"
git branch -M main
git remote add origin https://github.com/Form997/hai-dat-ai-film-studio.git
git push -u origin main
```

3. Đọc tab Actions và kết quả `Python CI`. File `data/` và `.env` đã có trong `.gitignore`, không đẩy thông tin cá nhân/khóa API lên GitHub.

## Kiểm định và phát hành

- **Alpha**: cảnh placeholder, tải tài sản, FFmpeg được test tự động.
- **AI workflow**: chỉ ghi `verified` nếu đã chạy trên GPU và lưu checkpoint/version, tệp output + log; model được tải riêng.
- **Public online**: V0.1 KHÔNG nên đưa web server ra công khai vì không có auth cho xem/tải file.
