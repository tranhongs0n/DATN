# QUY TẮC VẼ MERMAID

Chuẩn nhất quán biểu đồ hệ thống.

## 1. Màu sắc (B&W Theme)
- Giao diện Trắng - Đen (chuẩn in ấn).
- Bắt buộc chèn ngay dưới thẻ ` ```mermaid `:
  `%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#000000', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'background': '#ffffff'}}}%%`

## 2. Start / End Nodes
- Mọi Flowchart/Activity Diagram phải có Start/End.
- Dùng hình tròn. Cú pháp: `Start((Bắt đầu))` và `End((Kết thúc))`.
- Cấm hình vuông/oval.

## 3. Tác nhân (Actors)
- Biểu diễn bằng hình người (stickman).
- `sequenceDiagram`: Bắt buộc dùng `actor` (VD: `actor User as Thí sinh`).
- `flowchart` (Use Case): Bắt buộc dùng FontAwesome (VD: `(fa:fa-user Tên Tác Nhân)`).

## 4. Chú thích
- Mọi sơ đồ phải có chú thích in nghiêng ngay dưới. VD: `*Hình 2.1: Sơ đồ kiến trúc*`
